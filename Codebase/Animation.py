from matplotlib import animation
import matplotlib.pyplot as plt
from Codebase.train import episode_step

"""
Ensure you have imagemagick installed with 
sudo apt-get install imagemagick
Open file in CLI with:
xgd-open <filelname>

Credits: 
https://gist.github.com/botforge/64cbb71780e6208172bbf03cd9293553

"""
def save_frames_as_gif(frames, path='./', filename='gym_animation.gif'):
    plt.figure(figsize=(frames[0].shape[1] / 72.0, frames[0].shape[0] / 72.0), dpi=72)

    patch = plt.imshow(frames[0])
    plt.axis('off')

    def animate(i):
        patch.set_data(frames[i])

    anim = animation.FuncAnimation(plt.gcf(), animate, frames = len(frames), interval=50)
    anim.save(path + filename, writer='imagemagick', fps=60)

def create_animation(env, policy, savePath = None):
    state = env.reset()
    frames = []
    for t in range(1000):
        # Render to frames buffer
        frames.append(env.render(mode="rgb_array"))
        action = policy.sample_action(state)
        state, reward, done, _ = env.step(action)
        if done:
            break
    env.close()
    save_frames_as_gif(frames)