import matplotlib.pyplot as plt
from time import sleep



x = []
y = []

fig = plt.figure()

fig.show()
fig.canvas.draw()


for i in range(1,100):
    x.append(i)
    y.append(1/i)
    sleep(.02)
    fig.clear()
    plt.plot(x,y)
    #plt.draw()
    fig.canvas.draw()
