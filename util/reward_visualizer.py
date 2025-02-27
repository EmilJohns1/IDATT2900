import os
from datetime import datetime

import numpy as np

import matplotlib.pyplot as plt

import json


def plot_rewards(episode_rewards):
    # Calculate running mean and std
    running_means = np.cumsum(episode_rewards) / np.arange(1, len(episode_rewards) + 1)
    running_stds = [
        np.std(episode_rewards[: i + 1]) for i in range(len(episode_rewards))
    ]

    # Plot rewards, mean, and standard deviation
    plt.figure(figsize=(10, 6))
    plt.plot(
        range(1, len(episode_rewards) + 1), episode_rewards, label="Rewards", alpha=0.5
    )
    plt.plot(
        range(1, len(running_means) + 1),
        running_means,
        label="Running Mean",
        color="orange",
    )
    plt.fill_between(
        range(1, len(running_means) + 1),
        np.array(running_means) - np.array(running_stds),
        np.array(running_means) + np.array(running_stds),
        color="orange",
        alpha=0.3,
        label="Mean ± Std",
    )
    plt.xlabel("Episode")
    plt.ylabel("Rewards")
    plt.title("Episode Rewards with Running Mean and Std")
    plt.ylim(0, 500)
    plt.legend()
    plt.show()


def plot_multiple_runs(folder_name, title, field, block=True):
    all_rewards = []

    # Load data from all JSON files in the folder
    for filename in os.listdir(folder_name):
        if filename.endswith(".json"):
            with open(os.path.join(folder_name, filename), "r") as f:
                data = json.load(f)
                all_rewards.append(data[field])

    if not all_rewards:
        print("No valid data found in the folder.")
        return

    num_episodes = min(len(rewards) for rewards in all_rewards)
    all_rewards = [
        rewards[:num_episodes] for rewards in all_rewards
    ]  # Trim to the shortest run
    all_rewards = np.array(all_rewards)

    # Calculate mean and std
    mean_rewards = np.mean(all_rewards, axis=0)
    std_rewards = np.std(all_rewards, axis=0)
    running_means = np.cumsum(mean_rewards) / np.arange(1, len(mean_rewards) + 1)
    running_stds = [np.std(mean_rewards[: i + 1]) for i in range(len(mean_rewards))]

    # Plot each run
    plt.figure(figsize=(10, 6))
    for i, rewards in enumerate(all_rewards):
        plt.plot(range(1, num_episodes + 1), rewards, alpha=0.5, label=f"Run {i+1}")

    # Plot mean and standard deviation
    # plt.plot(range(1, num_episodes + 1), mean_rewards, color="black", linewidth=1, label="Mean")
    # plt.fill_between(range(1, num_episodes + 1), mean_rewards - std_rewards, mean_rewards + std_rewards, color="gray", alpha=0.3, label="Mean ± Std")

    # Plot running mean and standard deviation
    plt.plot(
        range(1, len(running_means) + 1),
        running_means,
        label="Running Mean",
        color="black",
    )
    plt.fill_between(
        range(1, len(running_means) + 1),
        np.array(running_means) - np.array(running_stds),
        np.array(running_means) + np.array(running_stds),
        color="black",
        alpha=0.3,
        label="Running Mean ± Std",
    )

    plt.xlabel("Episode")
    plt.ylabel("Rewards")
    plt.title(title)
    plt.ylim(0, 500)
    plt.legend()
    plt.show(block=block)
