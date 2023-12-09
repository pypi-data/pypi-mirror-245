from typing import Optional, Sequence, Tuple, Dict, List, Literal
from abc import ABC, abstractmethod, abstractproperty

import torch
import numpy as np

from ..stochastic_matrix import TransitionMatrix, ProbabilityVector # type: ignore
from ..utils import FittedModel,ContextualVariables, ConvergenceHandler, Observations, log_normalize, sequence_generator, DECODERS, INFORM_CRITERIA # type: ignore


class BaseHMM(ABC): 
    """
    Base Abstract Class for HMM
    ----------
    Base Class of Hidden Markov Models (HMM) class that provides a foundation for building specific HMM models.
    """

    def __init__(self,
                 n_states: int,
                 params_init: bool = False,
                 alpha: float = 1.0,
                 seed: Optional[int] = None,
                 device: Optional[torch.device] = None):

        self.n_states = n_states
        self.alpha = alpha
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') if device is None else device
        if params_init:
            self._initial_vector, self._transition_matrix = self.sample_chain_params(self.alpha,seed)

    @property
    def transition_matrix(self) -> TransitionMatrix:
        return self._transition_matrix

    @transition_matrix.setter
    def transition_matrix(self, matrix:torch.Tensor):
        assert (self.n_states,self.n_states) == matrix.shape, 'Matrix dimensions differ from HMM model'
        if isinstance(matrix, TransitionMatrix):
            self._transition_matrix = matrix
        elif isinstance(matrix, torch.Tensor):
            self._transition_matrix = TransitionMatrix(n_states=self.n_states,
                                                       matrix=matrix,
                                                       device=self.device)
        else:
            raise NotImplementedError('Matrix type not supported')

    @property
    def initial_vector(self) -> ProbabilityVector:
        return self._initial_vector

    @initial_vector.setter
    def initial_vector(self, vector:torch.Tensor):
        assert (self.n_states,) == vector.shape, 'Matrix dimensions differ from HMM model'
        if isinstance(vector, ProbabilityVector):
            self._initial_vector = vector
        elif isinstance(vector, torch.Tensor):
            self._initial_vector = ProbabilityVector(n_states=self.n_states, 
                                                     vector=vector,
                                                     device=self.device)
        else:
            raise NotImplementedError('Matrix type not supported')
        
    @property    
    def view_params(self):
        """Print the model parameters."""
        for param in self.params.values():
            param.view()
            print('\n')
        
    @property
    def _check_params(self):
        """Check if the model parameters are set."""
        return self.params
    
    @abstractproperty
    def __str__(self):
        pass

    @abstractproperty
    def params(self) -> Dict[str, torch.Tensor]:
        """Returns the parameters of the model."""
        pass

    @abstractproperty   
    def n_fit_params(self) -> Dict[str, int]:
        """Return the number of trainable model parameters."""
        pass
    
    @abstractproperty
    def dof(self) -> int:
        """Returns the degrees of freedom of the model."""
        pass

    @abstractmethod
    def _update_B_params(self, X:List[torch.Tensor], log_gamma:List[torch.Tensor], theta:Optional[ContextualVariables]):
        """Update the emission parameters."""
        pass

    @abstractmethod
    def check_sequence(self, sequence:torch.Tensor) -> torch.Tensor:
        """Get emission probabilities for a given sequence of observations."""
        pass

    @abstractmethod
    def map_emission(self, x:torch.Tensor) -> torch.Tensor:
        """Get emission probabilities for a given sequence of observations."""
        pass

    @abstractmethod
    def sample_B_params(self, X:Optional[torch.Tensor]=None, seed:Optional[int]=None):
        """Sample the emission parameters."""
        pass
        
    def sample_chain_params(self, alpha:float, seed:Optional[int]=None) -> Tuple[ProbabilityVector, TransitionMatrix]:
        """Initialize the model parameters."""
        return (ProbabilityVector(self.n_states, rand_seed=seed, alpha=alpha, device=self.device), 
                TransitionMatrix(self.n_states, rand_seed=seed, alpha=alpha, device=self.device))

    def to_observations(self, X:torch.Tensor, lengths:Optional[List[int]]=None) -> Observations:
        """Convert a sequence of observations to an Observations object."""
        X_valid = self.check_sequence(X)
        n_samples = X_valid.shape[0]
        seq_lenghts = [n_samples] if lengths is None else lengths
        X_vec = list(torch.split(X_valid, seq_lenghts))

        log_probs = []
        for seq in X_vec:
            log_probs.append(self.map_emission(seq))
        
        return Observations(n_samples,X_vec,log_probs,seq_lenghts,len(seq_lenghts))  
    
    def check_theta(self, theta:torch.Tensor, X:Observations) -> ContextualVariables:
        """Returns the parameters of the model."""
        if (n_dim:=theta.ndim) != 2:
            raise ValueError(f'Context must be 2-dimensional. Got {n_dim}.')
        elif theta.shape[1] not in (1, X.n_samples):
            raise ValueError(f'Context must have shape (context_vars, 1) for time independent context or (context_vars,{X.n_samples}) for time dependent. Got {theta.shape}.')
        else:
            n_context, n_observations = theta.shape
            time_dependent = n_observations == X.n_samples
            adj_theta = torch.vstack((theta, torch.ones(size=(1,n_observations),
                                                        dtype=torch.float64,
                                                        device=self.device)))
            if not time_dependent:
                adj_theta = adj_theta.expand(n_context+1, X.n_samples)

            context_matrix = list(torch.split(adj_theta,X.lengths,1))
            return ContextualVariables(n_context, context_matrix, time_dependent) 

    def fit(self,
            X:torch.Tensor,
            tol:float=1e-2,
            max_iter:int=20,
            n_init:int=1,
            post_conv_iter:int=3,
            ignore_conv:bool=False,
            sample_B_from_X:bool=False,
            verbose:bool=True,
            plot_conv:bool=False,
            lengths:Optional[List[int]]=None,
            theta:Optional[torch.Tensor]=None) -> Dict[int, FittedModel]:
        """Fit the model to the given sequence using the EM algorithm."""
        if sample_B_from_X:
            self.sample_B_params(X)
        X_valid = self.to_observations(X,lengths)
        valid_theta = self.check_theta(theta,X_valid) if theta is not None else None

        self.conv = ConvergenceHandler(tol=tol,
                                       max_iter=max_iter,
                                       n_init=n_init,
                                       post_conv_iter=post_conv_iter,
                                       device=self.device,
                                       verbose=verbose)

        self._check_params
        distinct_models = {}
        for rank in range(n_init):
            if rank > 0:
                self._initial_vector, self._transition_matrix = self.sample_chain_params(self.alpha)
            
            self.conv.push_pull(sum(self._compute_log_likelihood(X_valid)),0,rank)
            for iter in range(1,self.conv.max_iter+1):
                # EM algorithm step
                self._update_model(X_valid, valid_theta)

                # remap emission probabilities after update of B
                X_valid.log_probs = [self.map_emission(x) for x in X_valid.X]
                
                curr_log_like = sum(self._compute_log_likelihood(X_valid))
                converged = self.conv.push_pull(curr_log_like,iter,rank)
                if converged and not ignore_conv:
                    print(f'Model converged after {iter} iterations with log-likelihood: {curr_log_like:.2f}')
                    break

            distinct_models[rank] = FittedModel(self.__str__(),
                                                self.n_fit_params, 
                                                self.dof,
                                                converged,
                                                curr_log_like, 
                                                self.ic(X,lengths),
                                                self.params)
        
        if plot_conv:
            self.conv.plot_convergence()

        return distinct_models

    def predict(self, 
                X:torch.Tensor, 
                lengths:Optional[List[int]] = None,
                algorithm:Literal['map','viterbi'] = 'viterbi') -> Tuple[float, Sequence[torch.Tensor]]:
        """Predict the most likely sequence of hidden states."""
        self._check_params
        if algorithm not in DECODERS:
            raise ValueError(f'Unknown decoder algorithm {algorithm}')
        
        decoder = {'viterbi': self._viterbi,
                   'map': self._map}[algorithm]
        
        X_valid = self.to_observations(X, lengths)
        log_score = sum(self._compute_log_likelihood(X_valid))
        decoded_path = decoder(X_valid)

        return log_score, decoded_path

    def score(self, X:torch.Tensor, lengths:Optional[List[int]]=None) -> float:
        """Compute the joint log-likelihood"""
        return sum(self._score_observations(X,lengths))
    
    def score_samples(self, X:torch.Tensor, lengths:Optional[List[int]]=None) -> List[float]:
        """Compute the log-likelihood for each sequence"""
        return self._score_observations(X,lengths)

    def ic(self, 
           X:torch.Tensor, 
           lengths:Optional[List[int]] = None, 
           criterion:Literal['AIC','BIC','HQC'] = 'AIC') -> float:
        """Calculates the information criteria for a given model."""
        log_likelihood = self.score(X, lengths)
        if criterion not in INFORM_CRITERIA:
            raise NotImplementedError(f'{criterion} is not a valid information criterion. Valid criteria are: {INFORM_CRITERIA}')
        
        criterion_compute = {'AIC': lambda log_likelihood, dof: -2.0 * log_likelihood + 2.0 * dof,
                             'BIC': lambda log_likelihood, dof: -2.0 * log_likelihood + dof * np.log(X.shape[0]),
                             'HQC': lambda log_likelihood, dof: -2.0 * log_likelihood + 2.0 * dof * np.log(np.log(X.shape[0]))}[criterion]
        
        return criterion_compute(log_likelihood, self.dof)
    
    def _forward(self, X:Observations) -> List[torch.Tensor]:
        """Forward pass of the forward-backward algorithm."""
        alpha_vec = []
        for seq_len,_,log_probs in sequence_generator(X):
            log_alpha = torch.zeros(size=(seq_len,self.n_states), 
                                    dtype=torch.float64,
                                    device=self.device)
            
            log_alpha[0] = self._initial_vector + log_probs[0]
            for t in range(1,seq_len):
                log_alpha[t] = torch.logsumexp(log_alpha[t-1].reshape(-1,1) + self._transition_matrix, dim=0) + log_probs[t]

            alpha_vec.append(log_alpha)

        return alpha_vec
    
    def _backward(self, X:Observations) -> List[torch.Tensor]:
        """Backward pass of the forward-backward algorithm."""
        beta_vec = []
        for seq_len,_,log_probs in sequence_generator(X):
            log_beta = torch.zeros(size=(seq_len,self.n_states), 
                               dtype=torch.float64,
                               device=self.device)
            
            for t in reversed(range(seq_len-1)):
                log_beta[t] = torch.logsumexp(self._transition_matrix + log_probs[t+1] + log_beta[t+1], dim=1)
            
            beta_vec.append(log_beta)

        return beta_vec
    
    def _gamma(self, log_alpha:List[torch.Tensor], log_beta:List[torch.Tensor]) -> List[torch.Tensor]:
        """Compute the log-Gamma variable in Hidden Markov Model."""
        gamma_vec = []
        for alpha,beta in zip(log_alpha,log_beta):
            gamma_vec.append(log_normalize(alpha+beta,1))

        return gamma_vec
    
    def _xi(self, X:Observations, log_alpha:List[torch.Tensor], log_beta:List[torch.Tensor]) -> List[torch.Tensor]:
        """Compute the log-Xi variable in Hidden Markov Model."""
        xi_vec = []
        for (seq_len,_,log_probs),alpha,beta in zip(sequence_generator(X),log_alpha,log_beta):
            log_xi = torch.zeros(size=(seq_len-1, self.n_states, self.n_states),
                                 dtype=torch.float64, 
                                 device=self.device)
            
            for t in range(seq_len-1):
                log_xi[t] = alpha[t].reshape(-1,1) + self._transition_matrix + log_probs[t+1] + beta[t+1]

            log_xi -= alpha[-1].logsumexp(dim=0)
            xi_vec.append(log_xi)

        return xi_vec
    
    def _compute_fwd_bwd(self, X:Observations) -> Tuple[List[torch.Tensor],List[torch.Tensor]]:
        log_alpha = self._forward(X)
        log_beta = self._backward(X)
        return log_alpha, log_beta

    def _compute_posteriors(self, X:Observations) -> Tuple[List[torch.Tensor], List[torch.Tensor]]:
        """Execute the forward-backward algorithm and compute the log-Gamma and log-Xi variables."""
        log_alpha, log_beta = self._compute_fwd_bwd(X)
        log_gamma = self._gamma(log_alpha,log_beta)
        log_xi = self._xi(X,log_alpha,log_beta)
        return log_gamma, log_xi
    
    def _accum_pi(self, log_gamma:List[torch.Tensor]) -> torch.Tensor:
        """Accumulate the statistics for the initial vector."""
        log_pi = torch.zeros(size=(self.n_states,),
                             dtype=torch.float64, 
                             device=self.device)

        for gamma in log_gamma:
            log_pi += gamma[0].exp()
        
        return log_normalize(log_pi.log(),0)

    def _accum_A(self, log_xi:List[torch.Tensor]) -> torch.Tensor:
        """Accumulate the statistics for the transition matrix."""
        log_A = torch.zeros(size=(self.n_states,self.n_states),
                             dtype=torch.float64, 
                             device=self.device)
        
        for xi in log_xi:
            log_A += xi.exp().sum(dim=0)

        return log_normalize(log_A.log(),1)
    
    def _update_model(self, X:Observations, theta:Optional[ContextualVariables]) -> float:
        """Compute the updated parameters for the model."""
        log_gamma, log_xi = self._compute_posteriors(X)

        self._initial_vector.matrix.copy_(self._accum_pi(log_gamma))
        self._transition_matrix.matrix.copy_(self._accum_A(log_xi))
        self._update_B_params(X.X,log_gamma,theta)

        return sum(self._compute_log_likelihood(X))
    
    def _viterbi(self, X:Observations) -> Sequence[torch.Tensor]:
        """Viterbi algorithm for decoding the most likely sequence of hidden states."""
        viterbi_path_list = []
        for seq_len,_,log_probs in sequence_generator(X):
            viterbi_path = torch.empty(size=(seq_len,), 
                                       dtype=torch.int32,
                                       device=self.device)
            
            viterbi_prob = torch.empty(size=(self.n_states, seq_len), 
                                       dtype=torch.float64,
                                       device=self.device)
            psi = viterbi_prob.clone()

            # Initialize t=1
            viterbi_prob[:,0] = self._initial_vector + log_probs[0]
            for t in range(1,seq_len):
                trans_seq = viterbi_prob[:,t-1] + log_probs[t]
                trans_seq = self._transition_matrix + trans_seq.reshape((-1, 1))
                viterbi_prob[:,t] = torch.max(trans_seq, dim=0).values
                psi[:,t] = torch.argmax(trans_seq, dim=0)

            # Backtrack the most likely sequence
            viterbi_path[-1] = torch.argmax(viterbi_prob[:,-1])
            for t in reversed(range(seq_len-1)):
                viterbi_path[t] = psi[viterbi_path[t+1],t+1]

            viterbi_path_list.append(viterbi_path)

        return viterbi_path_list
    
    def _map(self, X:Observations) -> List[torch.Tensor]:
        """Compute the most likely (MAP) sequence of indiviual hidden states."""
        map_paths = []
        gamma_vec,_ = self._compute_posteriors(X)
        for gamma in gamma_vec:
            map_paths.append(torch.argmax(gamma, dim=1))
        return map_paths

    def _score_observations(self, X:torch.Tensor, lengths:Optional[List[int]]=None) -> List[float]:
        """Compute the log-likelihood for each sample sequence."""
        self._check_params
        return self._compute_log_likelihood(self.to_observations(X, lengths))

    def _compute_log_likelihood(self, X:Observations) -> List[float]:
        """Compute the log-likelihood of the given sequence."""
        scores = []
        for alpha in self._forward(X):
            scores.append(alpha[-1].logsumexp(dim=0).item())

        return scores
