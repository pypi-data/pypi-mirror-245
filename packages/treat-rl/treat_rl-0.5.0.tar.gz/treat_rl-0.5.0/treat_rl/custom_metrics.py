# EXAMPLE: https://github.com/ray-project/ray/blob/master/rllib/examples/custom_metrics_and_callbacks.py

from ray.rllib.algorithms.callbacks import DefaultCallbacks
from ray.rllib.evaluation import Episode
import numpy as np

class DiseaseTreatmentCallbacks(DefaultCallbacks):
    def __init__(self):
        self.remission_rewards = []
        self.state_based_rewards = []
        self.treatment_based_rewards = []
        self.symptom_based_rewards = []
        self.times_to_remission = []
        self.achieved_remission = []

    def on_episode_end(
        self, *, worker, base_env, policies, episode: Episode, env_index, **kwargs
    ):
        # Extract metrics from the environment
        env = base_env.get_unwrapped()[0]
        reward_components, time_to_remission = env.get_metrics()

        # Append the metrics to the lists
        self.remission_rewards.append(reward_components['remission'])
        self.state_based_rewards.append(reward_components['state_based'])
        self.treatment_based_rewards.append(reward_components['treatment_based'])
        self.symptom_based_rewards.append(reward_components['symptom_based'])
        self.times_to_remission.append(time_to_remission)
        self.achieved_remission.append(reward_components['remission'] != 0)

    def on_train_result(self, *, algorithm, result: dict, **kwargs):
        # Calculate and log aggregated metrics

        # mean
        result["custom_metrics"]["remission_reward_mean"] = np.mean(self.remission_rewards)
        result["custom_metrics"]["state_based_reward_mean"] = np.mean(self.state_based_rewards)
        result["custom_metrics"]["treatment_based_reward_mean"] = np.mean(self.treatment_based_rewards)
        result["custom_metrics"]["symptom_based_reward_mean"] = np.mean(self.symptom_based_rewards)
        result["custom_metrics"]["time_to_remission_mean"] = np.mean([t for t in self.times_to_remission if t != -1])

        # std
        result["custom_metrics"]["remission_reward_std"] = np.std(self.remission_rewards)
        result["custom_metrics"]["state_based_reward_std"] = np.std(self.state_based_rewards)
        result["custom_metrics"]["treatment_based_reward_std"] = np.std(self.treatment_based_rewards)
        result["custom_metrics"]["symptom_based_reward_std"] = np.std(self.symptom_based_rewards)
        result["custom_metrics"]["time_to_remission_std"] = np.std([t for t in self.times_to_remission if t != -1])

        # remission rate
        result["custom_metrics"]["remission_rate"] = np.mean(self.achieved_remission)

        # Reset lists for the next training iteration
        self.remission_rewards = []
        self.state_based_rewards = []
        self.treatment_based_rewards = []
        self.symptom_based_rewards = []
        self.times_to_remission = []
        self.achieved_remission = []
