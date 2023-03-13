import json

import numpy as np

import logger
from Plot import Player


def plot():
    with open('log.txt') as f:
        lines = f.readlines()
    virus_cells = dict()
    host_cells = dict()
    ribosomes = dict()
    animation_list = dict()
    for line in lines:
        line = line.strip()
        if line.startswith("virus cell"):
            virus = line.split(";")[1:]
            logger.log(str(virus))
            virus_cells[virus[0]] = virus[1]
        elif line.startswith("host cell"):
            host = line.split(";")[1:]
            host_cells[host[0]] = host[1]
        elif line.startswith("ribosome"):
            ribosome = line.split(";")[1:]
            ribosomes[ribosome[0]] = ribosome[1]
        elif line.startswith("move"):
            move = line.split(";")[1:]
            if move[0] not in animation_list:
                animation_list[move[0]] = []
            animation_list[move[0]].append(json.loads(move[1]))

    virus_cells = {k: json.loads(v) for k, v in virus_cells.items()}
    host_cells = {k: json.loads(v) for k, v in host_cells.items()}
    ribosomes = {k: json.loads(v) for k, v in ribosomes.items()}

    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    virus_cells_gui = dict()

    for k, v in virus_cells.items():
        virus, = ax.plot(xs=[], ys=[], zs=[], c='r', marker='o')
        virus.set_data([v[0]], [v[1]])
        virus.set_3d_properties([v[2]], 'z')
        virus_cells_gui[k] = virus

    def get_cube():
        phi = np.arange(1, 10, 2) * np.pi / 4
        Phi, Theta = np.meshgrid(phi, phi)

        x = np.cos(Phi) * np.sin(Theta)
        y = np.sin(Phi) * np.sin(Theta)
        z = np.cos(Theta) / np.sqrt(2)
        return x, y, z

    for k, v in host_cells.items():
        cube_x, cube_y, cube_z = get_cube()
        cube_x = cube_x * 2 + v[0]
        cube_y = cube_y * 2 + v[1]
        cube_z = cube_z * 2 + v[2]
        cube = ax.plot_wireframe(cube_x, cube_y, cube_z, color='b')

    for k, v in ribosomes.items():
        u, w = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
        x = v[0] + np.cos(u) * np.sin(w) / 3
        y = v[1] + np.sin(u) * np.sin(w) / 3
        z = v[2] + np.cos(w) / 3
        sphere = ax.plot_wireframe(x, y, z, color='g')

    def update(i):
        keys = list(animation_list.keys())
        for k in keys:
            if len(animation_list[k]) <= i:
                return
        for k in keys:
            pos = animation_list[k][i]
            virus_cells_gui[k].set_data(pos[0], pos[1])
            virus_cells_gui[k].set_3d_properties(pos[2], 'z')
    length = min([len(animation_list[k]) for k in animation_list.keys()])
    player = Player(fig, update, maxi=length, interval=1000)
    player.save('test.gif', dpi=80)
    plt.show()


if __name__ == "__main__":
    plot()
