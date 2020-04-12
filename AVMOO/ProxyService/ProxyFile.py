import threading
import time
import os
from AVMOO.ProxyService.Observabal.Sub import Subject


class ProxyFileWatcher(Subject):
    def __init__(self):
        # self.FilePath = settings.get('PROXY_FILE_PATH')
        self.FilePath = os.path.abspath("./proxies.json")
        self.FileHolder = FileContentHolder(self.FilePath)
        # self.TimeOut = settings.get('FRESH_FREQUENCY')
        self.TimeOut = 5
        self._work_thread = threading.Thread(target=self._watch, args=[self.TimeOut, ], daemon=True)
        self._flag = True
        self.start()

    def _watch(self, frequency):
        while self._flag:
            if self.FileHolder.has_change() is True:
                self.notify(self.FileHolder.FileContentRecord)
            time.sleep(frequency)

    def start(self):
        self._flag = True
        self._work_thread.start()

    def stop(self):
        self._flag = False


class FileContentHolder(object):
    def __init__(self, file_path):
        self.FilePath = file_path
        self.FileContentRecord = ""
        with open(self.FilePath, 'r') as f:
            self.FileContentRecord = f.read()

    def has_change(self):
        with open(self.FilePath, 'r') as f:
            file_content = f.read()

        if file_content != self.FileContentRecord:
            self.FileContentRecord = file_content
            return True
        else:
            return False


if __name__ == "__main__":
    a = ProxyFileWatcher()