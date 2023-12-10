from map import Map, plt
from agent import Agent


def setup_axes(ax, map):
    """Set up axes to be correct size and range between each matplotlib clear"""
    ax.set_xlim(0, map.environment.WIDTH)
    ax.set_ylim(0, map.environment.HEIGHT)
    ax.figure.set_size_inches(5, 5)
    ax.set_xticks([])  # Remove x-axis numbers
    ax.set_yticks([])  # Remove y-axis numbers


def interactive_simulation(config: dict, hz: int = 10):
    """Main loop for simulation that handles drawing and user input

    :param env: Environment configuration to simulate
    :param hz: Frame rate per second of the loop, defaults to 10
    """
    fig, ax = plt.subplots()
    plt.ion()
    map = Map(config, ax)
    agent = Agent(
        config,
        ax,
        map,
    )

    objects = [map, agent]

    def click(event):
        if event.inaxes != ax:
            return
        for obj in objects:
            obj.click(event.xdata, event.ydata)

    fig.canvas.mpl_connect("button_press_event", click)

    while True:
        ax.cla()
        setup_axes(ax, map)

        for obj in objects:
            obj.tick()
            obj.plot()

        plt.draw()
        plt.pause(1 / hz)
