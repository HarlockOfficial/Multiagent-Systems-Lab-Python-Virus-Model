from Agents import VirusCell, HostCell, Ribosome
from Plot import PlotBuilder
from Scheduler import Scheduler


def main():
    full_list = []
    for i in range(10):
        full_list.append(VirusCell())
    for i in range(3):
        hc = HostCell()
        ribosome = Ribosome(parent_cell=hc)
        full_list.append(hc)
        full_list.append(ribosome)
    scheduler = Scheduler(full_list)
    scheduler.start()
    try:
        scheduler.join()
    except KeyboardInterrupt:
        scheduler.stop()
        scheduler.join()
    PlotBuilder().animate()


if __name__ == '__main__':
    main()
