import logging
import signal
import threading
import time

from cloud_tpu_diagnostics.src.stack_trace import disable_stack_trace_dumping
from cloud_tpu_diagnostics.src.stack_trace import enable_stack_trace_dumping

# flag to signal daemon thread to exit gracefully
_exit_flag = threading.Event()
_exit_flag.clear()
_daemon_thread = None
logger = logging.getLogger(__name__)


def start_debugging(debug_config):
  """Context manager to debug and identify errors."""
  global _daemon_thread
  _exit_flag.clear()
  if (
      debug_config.stack_trace_config is not None
      and debug_config.stack_trace_config.collect_stack_trace
  ):
    _daemon_thread = threading.Thread(
        target=send_user_signal,
        daemon=True,
        args=(debug_config.stack_trace_config.stack_trace_interval_seconds,),
    )
    _daemon_thread.start()  # start a daemon thread
    enable_stack_trace_dumping(debug_config.stack_trace_config)


def stop_debugging(debug_config):
  """Context manager to debug and identify errors."""
  if (
      debug_config.stack_trace_config is not None
      and debug_config.stack_trace_config.collect_stack_trace
  ):
    _exit_flag.set()
    # wait for daemon thread to complete
    if _daemon_thread is not None:
      logger.info(
          "Waiting for completion of stack trace collection daemon thread."
      )
      _daemon_thread.join()
      logger.info("Stack trace collection daemon thread completed.")
    disable_stack_trace_dumping(debug_config.stack_trace_config)
  _exit_flag.clear()


def send_user_signal(stack_trace_interval_seconds):
  """Send SIGUSR1 signal to main thread after every stack_trace_interval_seconds seconds."""
  while not _exit_flag.is_set():
    time.sleep(stack_trace_interval_seconds)
    if not _exit_flag.is_set():
      signal.pthread_kill(threading.main_thread().ident, signal.SIGUSR1)
