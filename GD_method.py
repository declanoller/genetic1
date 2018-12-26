import torch
import numpy as np
import matplotlib.pyplot as plt
import sys
from math import sqrt
sys.path.append('../IndividualClasses')
from Brachistochrone import Brachistochrone
import torch.optim as optim
import FileSystemTools as fst
import subprocess

def plotFF(ax, best_FF):

    ax.clear()
    ax.set_xlabel('# generations')
    ax.set_ylabel('fitness function')
    ax.plot(best_FF, label='best', color='dodgerblue')
    ax.legend()
    ax.text(0.6*len(best_FF), 0.8*max(best_FF), 'best: {:.3f}'.format(best_FF[-1]))


def fitnessFunction(y_no_end_pts, height):

    g = 9.8
    N_segments = len(y_no_end_pts) + 1
    N = N_segments
    N_pts = N+1
    width = 1.0
    delta_x = width/N_segments
    #So if the next point is lower than the previous one, d will be *positive* (i.e., the y axis is down, opposite with the plot axis.)
    #d = -np.array([y[i+1] - y[i] for i in range(N_segments)])

    y = torch.cat((torch.tensor([height]), y_no_end_pts, torch.tensor([0.0])), dim=0)

    d = torch.stack([-(y[i+1] - y[i]) for i in range(N_segments)])

    #Be careful with signs and indices!
    #v = sqrt(2*g)*np.sqrt([0.0] + [sum(d[:(i+1)]) for i in range(len(d))])
    temp = torch.stack([torch.tensor(0.0)] + [sum(d[:(i+1)]) for i in range(len(d))])
    v = sqrt(2*g)*torch.sqrt(temp)

    #v = np.sqrt([0] + [sum(d[:(i+1)]) for i in range(len(d))])
    v = v[:-1]
    t = (torch.sqrt(v**2 + 2*g*d) - v)/(g*d/torch.sqrt(d**2 + delta_x**2))

    return(sum(t))

date_string = fst.getDateString()
base_name = f'GD_Brach__{date_string}'

N_gif_frames = 100
gif_dir = fst.combineDirAndFile('gifs', base_name)
print(gif_dir)
subprocess.check_call(['mkdir', gif_dir])
make_gif = True

fig, axes = plt.subplots(2,1,figsize=(6,8))
ax_FF = axes[0]
ax_state = axes[1]

show_plot = False

if show_plot:
    plt.show(block=False)

N = 30
height = 1.3
b = Brachistochrone(N=N, height=height)

y = torch.tensor(b.state[1:-1], requires_grad=True)

#adam_optimizer = optim.Adam([y])
adam_optimizer = optim.RMSprop([y])

best = []

t_range = 3000
for t in range(t_range):

    J = fitnessFunction(y, height)

    best.append(J.item())

    b.state[1:-1] = y.detach().tolist()
    ax_FF.clear()
    ax_state.clear()
    plotFF(ax_FF, best)
    b.plotState(ax_state, color='tomato', plot_sol=True, plot_label=True)

    if show_plot:
        fig.canvas.draw()

    if make_gif:
        if t==0 or (t%max(1, int(t_range/N_gif_frames))==0):
            plt.savefig(f'{gif_dir}/{t+1}.png')

    if t%int(t_range/20)==0:
        print('iteration {}, loss: {:.3f}'.format(t, J.item()))

    adam_optimizer.zero_grad()
    J.backward()
    adam_optimizer.step()


plt.savefig(f'misc_runs/{base_name}.png')

if make_gif:
    gif_name = fst.gifFromImages(gif_dir, base_name, ext='.png', delay=20)
    gif_basename = fst.fnameFromFullPath(gif_name)
    subprocess.check_call(['mv', gif_name, fst.combineDirAndFile('misc_runs', gif_basename)])
    subprocess.check_call(['rm', '-rf', gif_dir])




exit(0)




#
