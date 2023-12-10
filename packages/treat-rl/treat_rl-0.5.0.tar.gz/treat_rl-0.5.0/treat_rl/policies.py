import numpy as np

class StandardOfCare:
    """A state-agnostic greedy policy that selects the treatment with the highest remission probability."""
    def __init__(self, env, alpha=0.5):
        self.env = env
        self.alpha = alpha  # Learning rate for updating estimates
        self.remission_reward = env.remission_reward
        self.Q_values = self._initialize_Q_values()

    def _initialize_Q_values(self):
        # Initialize Q-values using the expected value across the population as a prior
        Q_values = {}
        for treatment in range(self.env.n_treatments):
            expected_value = 0
            cost = self.env.treatments[f"Treatment_{treatment}"]['base_cost']
            for d, disease in enumerate(self.env.diseases.values()):
                remission_prob = disease['remission_probs'].get(treatment, 0)
                expected_value += (remission_prob * self.remission_reward - cost) * self.env.stationary_distribution[d]
            Q_values[treatment] = expected_value

        
        return Q_values

    def get_treatment(self, current_disease=None, current_step=None):
        # Select the treatment with the highest Q-value
        return max(self.Q_values, key=self.Q_values.get)

    def update(self, treatment, reward):
        # Update the Q-value for the chosen treatment based on the reward received
        self.Q_values[treatment] = (1 - self.alpha) * self.Q_values[treatment] + self.alpha * reward

    def step(self, observation):
        # Select a treatment based on the highest Q-value
        treatment = self.get_treatment()
        
        return treatment

    def reset(self):
        # Reset Q-values to initial state
        self.Q_values = self._initialize_Q_values()


class ClinicalTrial:
    """Policy for Thompson sampling that probabilistically selects the treatment with the highest remission probability.
    This is intended to imitate a Sequential Multiple Assignment Randomized Trial (SMART) ."""
    def __init__(self, env, verbose=False):
        self.env = env
        self.verbose = verbose
        self.remission_reward = env.remission_reward
        self.avg_remission_probs = self._calculate_average_remission_probs()
        self.treatment_weights = self._calculate_treatment_weights()

    def _calculate_average_remission_probs(self):
        remission_probs = {}
        for t in range(self.env.n_treatments):
            total_prob = 0
            for d, disease in enumerate(self.env.diseases.values()):
                # Multiply the remission probability by the stationary distribution of the disease
                total_prob += disease['remission_probs'].get(t, 0) * self.env.stationary_distribution[d] 
            # Only add to the dictionary if the remission probability is not zero
            if total_prob > 0:
                remission_probs[t] = total_prob
        return remission_probs

    def _calculate_treatment_weights(self):
        weights = {}
        for treatment, remission_prob in self.avg_remission_probs.items():
            cost = self.env.treatments[f"Treatment_{treatment}"]['base_cost']
            weights[treatment] = self.remission_reward * remission_prob - cost
        return weights

    def get_treatment(self, current_disease, current_step):
        available_treatments = list(self.treatment_weights.keys())
        return np.random.choice(available_treatments, p=self._normalize_weights(available_treatments))

    def _normalize_weights(self, available_treatments):
        weights = [self.treatment_weights[t] for t in available_treatments]
        # Use softmax to convert weights to probabilities
        return np.exp(weights) / np.sum(np.exp(weights), axis=0)

    def reset(self):
        pass

class Random:
    """Policy for Thompson sampling that probabilistically selects the treatment with the highest remission probability.
    This is intended to imitate a Sequential Multiple Assignment Randomized Trial (SMART) ."""
    def __init__(self, env, verbose=False):
        self.env = env

    def get_treatment(self, current_disease, current_step):
        available_treatments = np.arange(self.env.n_treatments)
        return np.random.choice(available_treatments)

    def reset(self):
        pass
    
class Oracle:
    """A state-aware greedy policy that selects the treatment with the highest expected reward.
    This is intended to represent a near-optimal policy."""
    def __init__(self, env):
        self.env = env  # The environment instance
        self.remission_reward = env.remission_reward
    
    def select_action(self, current_disease):
        # Check if the current disease is in remission
        if current_disease == "Remission":
            return None  # No action required
        
        # Retrieve the disease's data from the environment
        disease_info = self.env.diseases[current_disease]

        # Find the expected reward of each treatment (remission probability * reward - cost)
        expected_rewards = {}
        for treatment, remission_prob in disease_info['remission_probs'].items():
            cost = self.env.treatments[f"Treatment_{treatment}"]['base_cost']
            expected_rewards[treatment] = remission_prob * self.env.remission_reward - cost

        # Find the treatment with the highest expected reward
        best_treatment = max(expected_rewards, key=expected_rewards.get)
        
        return best_treatment

    def step(self, observation):
        current_disease = self.env.current_disease  # Directly accessing the current disease state (which is "cheating")
        
        # Select the action (treatment) with the highest remission probability
        action = self.select_action(current_disease)
        
        return action