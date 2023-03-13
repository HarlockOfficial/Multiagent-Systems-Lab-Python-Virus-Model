import threading


class Scheduler(threading.Thread):
    def __init__(self, agents: list):
        super().__init__()
        self.agents = agents

    def run(self):
        for agent in self.agents:
            agent.start()

        for agent in self.agents:
            agent.join()

    def stop(self):
        for agent in self.agents:
            agent.stop()
