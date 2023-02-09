import logging
import logging.handlers
import datetime
import os
import sys
import time
import json, urllib
import threading
local_task = threading.local()


class SafeRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False, atTime=None):
        logging.handlers.TimedRotatingFileHandler.__init__(self, filename, when, interval, backupCount, encoding, delay,
                                                           utc, atTime)

    """
    Override doRollover
    lines commanded by "##" is changed by cc
    """

    def doRollover(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.

        Override,   1. if dfn not exist then do rename
                    2. _open with "a" model
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        dfn = self.baseFilename + "." + time.strftime(self.suffix, timeTuple)
        if not os.path.exists(dfn) and os.path.exists(self.baseFilename):
            os.rename(self.baseFilename, dfn)
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        if not self.delay:
            self.mode = "a"
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        # If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:  # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt


class SocketIOHandler(logging.Handler, object):

    def __init__(self, name, socket, **kwargs):
        logging.Handler.__init__(self)
        self.socket = socket

    def emit(self, record):
        if self.socket is None: return
        from flask_socketio import emit
        try:
            msg = self.format(record)
            with self.socket.app_context():
                emit('log', {'data': msg}, broadcast=True, namespace="/")
        except Exception:
            self.handleError(record)

_pywebview_window = None

def log2pywebview(level, ts, msg, task_id=0):
    global _pywebview_window
    if _pywebview_window is None: return
    json_str = urllib.parse.quote(msg)
            # print("eval js", json_str)
    js_str = f"""
                        window.rpa_log('{level}', '{ts}', '{json_str}', '{task_id}')
                    """
    _pywebview_window.evaluate_js(js_str)


class PywebviewHandler(logging.Handler, object):
    def __init__(self, name, window, **kwargs):
        logging.Handler.__init__(self)
        self.window = window

    def emit(self, record:logging.LogRecord):
        if self.window is None: return
        try:
            # msg = self.format(record)
            msg = record.getMessage()
            ts = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            log2pywebview(record.levelname, ts, msg, local_task.taskid)
        except Exception:
            self.handleError(record)

class QueueHandler(logging.Handler, object):
    def __init__(self, name, queue, **kwargs):
        logging.Handler.__init__(self)
        self.name = name
        self.queue = queue

    def emit(self, record):
        if self.queue is None: return
        try:
            msg = self.format(record)
            ts = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            self.queue.put(
                {
                    "id": self.name,
                    "level": record.levelname,
                    "ts": ts,
                    "msg": msg
                }
            )
        except Exception:
            self.handleError(record)

logger = None
from threading import Thread
import multiprocessing as mp
queue = mp.Queue()
def sub_queeu():
    global queue
    while True:
        try:
            q = queue.get(block=True)
            log2pywebview(q["level"], q["ts"], q["msg"], q["id"])
            time.sleep(0.05)
        except Exception as e:
            logger.error(e)

def setup_logging():
    global logger
    logger = logging.getLogger('rpa')
    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(stream_handler)
    # if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    file_handler = SafeRotatingFileHandler('rpa.log', when='midnight', interval=1, backupCount=7,
                                           atTime=datetime.time(0, 0, 0, 0))
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(file_handler)

    thread = Thread(target=sub_queeu, daemon=True)
    thread.start()

setup_logging()

def handle_exception(exc_type, exc_value, exc_traceback):
    global logger
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception

def add_socket_handler(socket):
    handler = SocketIOHandler("socket", socket)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)


def add_pywebview_handler(window):
    global _pywebview_window
    _pywebview_window = window
    handler = PywebviewHandler("pywebview", window)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)

def add_process_queue_handler(taskid, log_queue):
    handler = QueueHandler(f"{taskid}", log_queue)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    sys.excepthook = handle_exception