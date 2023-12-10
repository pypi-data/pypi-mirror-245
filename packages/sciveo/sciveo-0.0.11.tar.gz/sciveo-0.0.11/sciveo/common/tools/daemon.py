import threading
import time

from sciveo.common.tools.logger import *
from sciveo.common.tools.synchronized import ListQueue


class DaemonBase:
  def __init__(self, period=0):
    self.is_running = False
    self.is_started = False
    self.period = period

  def start(self):
    if self.is_started:
      return

    self.is_running = True
    self.is_started = True
    self.thread = threading.Thread(target = self.safe_run)
    self.thread.setDaemon(True)
    self.thread.start()

  def stop(self):
    self.is_running = False

  def finalise(self):
    pass

  def join(self):
    self.thread.join()

  def loop(self):
    pass

  def run(self):
    while(self.is_running):
      try:
        self.loop()
      except Exception as e:
        error(type(self).__name__, e)
      time.sleep(self.period)

  def safe_run(self):
    try:
      self.run()
    except Exception as e:
      error(type(self).__name__, e)


class TasksDaemon(DaemonBase):
  current = None
  queue = ListQueue("tasks")

  def loop(self):
    debug(type(self).__name__, "task waiting...")
    task = TasksDaemon.queue.pop()
    debug(type(self).__name__, "run task")
    task()
