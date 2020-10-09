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

def episode_step(state, env, policy, memory, global_steps, eps_min, eps_steps_till_min):
    policy.set_epsilon(get_epsilon(global_steps, eps_min, eps_steps_till_min))
    action = policy.sample_action(state)

    next_state, reward, done, _ = env.step(action)
    memory.push([state, action, reward, next_state, done])

    return done, reward, next_state


def train(Q, memory, optimizer, batch_size, discount_factor, do_train, full_gradient, clip_grad):
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
        with torch.no_grad():
            target = compute_targets(Q, reward, next_state, done, discount_factor)

    # loss is measured from error between current and newly expected Q values
    loss = F.smooth_l1_loss(q_val, target)

    # backpropagation of loss to Neural Network (PyTorch magic)
    if do_train:
        optimizer.zero_grad()
        loss.backward()
        if 0 < clip_grad:
            torch.nn.utils.clip_grad_norm_(Q.parameters(), clip_grad, norm_type=2)
        optimizer.step()

    return loss.item()

def get_epsilon(it, eps_min, eps_steps_till_min):
    v = max(eps_min, 1 - ((1 - eps_min)/eps_steps_till_min)*it)
    return max(eps_min, 1 - ((1 - eps_min)/eps_steps_till_min)*it)


def run_episodes(train, Q, policy, memory, env, args):

    optimizer = optim.Adam(Q.parameters(), args.stepsize)

    global_steps = 0  # Count the steps (do not reset at episode start, to compute epsilon)
    episode_durations = []  #
    episode_returns = []
    starting_positions = []

    for i in range(args.num_episodes):
        state = env.reset()
        starting_positions.append(state.tolist())
        all_rewards = []

        steps = 0
        state = env.reset()
        while True:
            done, reward, state = episode_step(state, env, policy, memory, global_steps, args.eps_min, args.eps_steps_till_min)
            train(Q, memory, optimizer, args.batch_size, args.discount_factor, args.do_train, args.full_gradient, args.clip_grad)
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
