from AllLibraries import *
from GetToOddscorp import get_fork_info


CHEK = True


class ForkScaner(QObject, object):
    finished = pyqtSignal()
    progress = pyqtSignal(list)


    def get_forks_from_oddscorp(self):
        while (CHEK):
            sleep(1)
            self.progress.emit(get_fork_info())
            if CHEK == False:
                self.finished.emit()
        self.finished.emit()

    def finish(self, str):
        logging.info(str)