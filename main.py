from dotenv import load_dotenv

from Agents import VirusCell, HostCell, Ribosome
from Plot import PlotBuilder
from Scheduler import Scheduler


def main():
    load_dotenv()
    full_list = []
    for i in range(3):
        full_list.append(VirusCell())
    for i in range(2):
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
    animation = PlotBuilder().animate()


if __name__ == '__main__':
    with open("log.txt", "w") as f:
        f.write("")
    main()
