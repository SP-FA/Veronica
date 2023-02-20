from processSupervisor import Supervisor
import setproctitle


def runSupervisor():
    super = Supervisor()
    super.supervise()


if __name__ == "__main__":
    setproctitle.setproctitle("super@super")
    runSupervisor()
