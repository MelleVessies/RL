import torch
from torch import optim
import torch.nn.functional as F

def compute_q_vals(Q, states, actions):
    """
    This method returns Q values for given state action pairs.

    Args:
        Q: Q-net
        states: a tensor of states. Shape: batch_size x obs_dim
        actions: a tensor of actions. Shape: Shape: batch_size x 1

    Returns:
        A torch tensor filled with Q values. Shape: batch_size x 1.
    """
    return torch.gather(Q(states), 1, actions)


def compute_targets(Q, rewards, next_states, dones, discount_factor):
    """
    This method returns targets (values towards which Q-values should move).

    Args:
        Q: Q-net
        rewards: a tensor of actions. Shape: Shape: batch_size x 1
        next_states: a tensor of states. Shape: batch_size x obs_dim
        dones: a tensor of boolean done flags (indicates if next_state is terminal) Shape: batch_size x 1
        discount_factor: discount
    Returns:
        A torch tensor filled with target values. Shape: batch_size x 1.
    """
    return rewards + discount_factor * (1- dones.int()) * Q(next_states).max(1)[0].reshape(dones.size())

def episode_step(state, env, policy, memory, global_steps):
    policy.set_epsilon(get_epsilon(global_steps))
    action = policy.sample_action(state)

    next_state, reward, done, _ = env.step(action)
    memory.push([state, action, reward, next_state, done])

    return done, reward, next_state


def train(Q, memory, optimizer, batch_size, discount_factor, do_train=True, full_gradient=False):
    # DO NOT MODIFY THIS FUNCTION

    # don't learn without some decent experience
    if len(memory) < batch_size:
        return None

    # random transition batch is taken from experience replay memory
    transitions = memory.sample(batch_size)

    # transition is a list of 4-tuples, instead we want 4 vectors (as torch.Tensor's)
    state, action, reward, next_state, done = zip(*transitions)

    # convert to PyTorch and define types
    state = torch.tensor(state, dtype=torch.float)
    action = torch.tensor(action, dtype=torch.int64)[:, None]  # Need 64 bit to use them as index
    next_state = torch.tensor(next_state, dtype=torch.float)
    reward = torch.tensor(reward, dtype=torch.float)[:, None]
    done = torch.tensor(done, dtype=torch.uint8)[:, None]  # Boolean

    # compute the q value
    q_val = compute_q_vals(Q, state, action)

    if full_gradient:
        target = compute_targets(Q, reward, next_state, done, discount_factor)
    else:
        with torch.no_grad():  # Don't compute gradient info for the target (semi-gradient)
            target = compute_targets(Q, reward, next_state, done, discount_factor)

    # loss is measured from error between current and newly expected Q values
    loss = F.smooth_l1_loss(q_val, target)

    # backpropagation of loss to Neural Network (PyTorch magic)
    if do_train:
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    return loss.item()  # Returns a Python scalar, and releases history (similar to .detach())

def get_epsilon(it):
    return max(0.005, 1 - it * 0.000095)

def run_episodes(train, Q, policy, memory, env, num_episodes, batch_size, discount_factor, learn_rate, do_train=True):

    optimizer = optim.Adam(Q.parameters(), learn_rate)

    global_steps = 0  # Count the steps (do not reset at episode start, to compute epsilon)
    episode_durations = []  #
    episode_returns = []
    starting_positions = []

    for i in range(num_episodes):
        state = env.reset()
        starting_positions.append(state.tolist())
        all_rewards = []

        steps = 0
        state = env.reset()
        while True:
            done, reward, state = episode_step(state, env, policy, memory, global_steps)
            train(Q, memory, optimizer, batch_size, discount_factor, do_train)

            all_rewards.append(reward)

            global_steps += 1
            steps += 1

            if done:
                if i % 10 == 0:
                    print("{2} Episode {0} finished after {1} steps"
                          .format(i, steps, '\033[92m' if steps >= 195 else '\033[99m'))
                episode_durations.append(steps)
                episode_returns.append(sum(all_rewards))
                break
    return episode_durations, episode_returns, starting_positions
