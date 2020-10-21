from matplotlib import animation
import matplotlib.pyplot as plt

"""
Ensure you have imagemagick installed with
sudo apt-get install imagemagick
Open file in CLI with:
xgd-open <filelname>

Credits:
https://gist.github.com/botforge/64cbb71780e6208172bbf03cd9293553

"""
def frames_to_animation(frames):
    plt.figure(figsize=(frames[0].shape[1] / 72.0, frames[0].shape[0] / 72.0), dpi=72)

    patch = plt.imshow(frames[0])
    t = plt.text(5, 20, "Step: 0")

    def animate(i, t, frame_iter):
        t.set_text(f"Step: {next(frame_iter)}")
        patch.set_data(frames[i])

    return animation.FuncAnimation(plt.gcf(), animate, frames=len(frames), fargs=[t, iter(range(0, len(frames) +1))], interval=50)


def create_animation(env, policy, Q, max_episode_steps):
    state = env.reset()
    frames = []
    r = []
    for t in range(max_episode_steps):
        # Render to frames buffer
        frames.append(env.render(mode="rgb_array"))
        action = policy.sample_action(Q, state)
        state, reward, done, _ = env.step(action)
        r.append(reward)
        if done:
            break
    env.close()
    print(f"return obtained: {sum(r)}")
    return frames_to_animation(frames)
