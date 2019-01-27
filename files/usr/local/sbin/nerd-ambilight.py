#!/usr/bin/python
# --------------------------------------------------------------------------
# Script executed by systemd service nerd-alarmclock.service
#
# Please edit /etc/nerd-alarmclock.conf to configure this script.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/nerd-alarmclock
#
# --------------------------------------------------------------------------

import select, os, sys, syslog, signal, time, locale
import ConfigParser, threading

import ncolors

# --- helper class for logging to syslog/stderr   --------------------------

class Msg(object):
  """ Very basic message writer class """

  # --- constructor   ------------------------------------------------------

  def __init__(self,debug):
    """ Constructor """
    self._debug = debug
    self._lock = threading.Lock()
    try:
      if os.getpgrp() == os.tcgetpgrp(sys.stdout.fileno()):
        self._syslog = False
        self._debug  = "1"
      else:
        self._syslog = True
    except:
      self._syslog = True

    if self._syslog:
      syslog.openlog("nerda")

  def msg(self,text):
    """ write message to the system log """
    if self._debug == '1':
      with self._lock:
        if self._syslog:
          syslog.syslog(text)
        else:
          sys.stderr.write(text)
          sys.stderr.write("\n")
          sys.stderr.flush()

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

# ---initialize objects   --------------------------------------------------

def init(parser):
  """ Initialize objects """

  settings     = ncolors.Settings.Settings(parser)
  settings.log = Msg(settings.get_value('GLOBAL','debug',0))
  settings.load()
  return settings

# --- start all threads   --------------------------------------------------

def start_threads(settings):
  """ Start all threads """

  threads = []

  if settings.get_value('WEB','active','1') != '0':
    webThread = ncolors.WebThread.WebThread(settings)
    threads.append(webThread)

  streamThread = ncolors.PiVideoStream.PiVideoStream(settings)
  threads.append(streamThread)
  screenThread = ncolors.ScreenThread.ScreenThread(settings, streamThread)
  threads.append(screenThread)
  dominantColorThread = ncolors.DominantColorThread.DominantColorThread(settings, streamThread, screenThread)
  threads.append(dominantColorThread)
  ledControllerThread = ncolors.LedControllerThread.LedControllerThread(settings)
  threads.append(ledControllerThread)

  map(threading.Thread.start, threads)
  return threads

# --- stop all threads   ---------------------------------------------------

def stop_threads(settings,threads):
  """ Stop all threads """

  # send event to all threads
  settings.stop_event.set()

  # wait for threads to terminate
  map(threading.Thread.join, threads)

# --------------------------------------------------------------------------

def signal_handler(_signo, _stack_frame):
  """ Signal-handler to cleanup threads """

  global threads, settings
  settings.log.msg("interrupt %d detected, exiting" % _signo)
  stop_threads(settings,threads)
  settings.save(wait=False)
  sys.exit(0)

# --- main program   ------------------------------------------------------

# set local to default from environment
locale.setlocale(locale.LC_ALL, '')

# read configuration
parser = ConfigParser.RawConfigParser()
parser.optionxform = str
parser.read('/etc/nerd-colors.conf')

# initialize system
settings = init(parser)

# setup signal handlers
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# create and start threads
threads = start_threads(settings)

# --- main loop   ---------------------------------------------------------

signal.pause()
