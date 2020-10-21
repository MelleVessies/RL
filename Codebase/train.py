import torch
from torch import optim
import numpy as np
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


def compute_targets(action_q, value_q, rewards, next_states, dones, discount_factor):
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
    actions = action_q(next_states).argmax(1)
    return rewards + discount_factor * (1- dones.int()) * compute_q_vals(value_q, next_states, actions.reshape((actions.size()[0], 1))).reshape(dones.size())


def episode_step(state, env, policy, Q, memory, ep_no, eps_min, eps_steps_till_min):
    policy.set_epsilon(get_epsilon(ep_no, eps_min, eps_steps_till_min))
    action = policy.sample_action(Q, state)

    next_state, reward, done, _ = env.step(action)
    memory.push([state, action, reward, next_state, done])

    return done, reward, next_state


def train(Q, memory, action_q, value_q, optimizer, args):

    batch_size, discount_factor, do_not_train, full_gradient, clip_grad = args.batch_size, args.discount_factor, args.do_not_train, args.full_gradient, args.clip_grad

    # don't learn without some decent experience
    if len(memory) < batch_size:
        return None, None

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

    # Note that full gradient in tandem with Double Q learning is a bit wacky.
    # if full_gradient:
    #     target = compute_targets(action_q, value_q, reward, next_state, done, discount_factor)
    # else:
    with torch.no_grad():
        target = compute_targets(action_q, value_q, reward, next_state, done, discount_factor)

    # loss is measured from error between current and newly expected Q values
    loss = F.smooth_l1_loss(q_val, target)

    with torch.no_grad():
        MSTD = F.mse_loss(q_val, target)

    # print(f"TEST: {MSTD}")
    # backpropagation of loss to Neural Network (PyTorch magic)
    if not do_not_train:
        optimizer.zero_grad()
        loss.backward()
        if 0 < clip_grad:
            torch.nn.utils.clip_grad_norm_(Q.parameters(), clip_grad, norm_type=2)
        optimizer.step()

    return loss.item(), MSTD.item()

def get_epsilon(it, eps_min, eps_steps_till_min):
    # print(it, eps_min, eps_steps_till_min)
    # input(max(eps_min, 1 - ((1 - eps_min)/eps_steps_till_min)*it))
    return max(eps_min, 1 - ((1 - eps_min)/eps_steps_till_min)*it)


def run_episodes(train, QWrapper, policy, env, args):

    # optimizer = optim.Adam(Q.parameters(), args.stepsize)

    ep_no = 0
    global_steps = 0
    episode_durations = []
    episode_returns = []
    starting_positions = []
    MSTD_per_update = []

    for i in range(args.num_episodes):
        state = env.reset()
        starting_positions.append(state.tolist())
        all_rewards = []
        steps = 0
        while True:
            Q, optimizer, memory, action_q, value_q = QWrapper.wrapper_magic()
            QWrapper.update_target(global_steps)

            done, reward, state = episode_step(state, env, policy, Q, memory, ep_no, args.eps_min, args.eps_steps_till_min)
            loss, MSTD = train(Q, memory, action_q, value_q, optimizer, args)
            all_rewards.append(reward)
            if MSTD is not None:
                MSTD_per_update.append(MSTD)


            steps += 1
            global_steps += 1

            if done:
                ep_no += 1
                returns = sum(all_rewards)
                episode_durations.append(steps)
                if i == 0:
                    print("Episode {0} finished with return: {1}."
                          .format(i, returns))
                elif i % 10 == 0:
                    print("Episode {0}, running average return : {1}, The running avg MSTD error is {2}"
                          .format(i, np.mean(episode_returns[-10:]), np.mean(MSTD_per_update[-10:])))
                episode_returns.append(returns)
                break
    return episode_durations, episode_returns, starting_positions, MSTD_per_update
