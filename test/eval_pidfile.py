# -*- coding: utf-8 -*-
""" Test ProcessIDFile """

import sys
import time
import logging

from commonutil_fileio_runtimerecord.processid import ProcessIDFile

_DEFAULT_PIDFILE = "/tmp/pidfile-test-1"

_log = logging.getLogger(__name__)


def get_options():
	pidfile_path = _DEFAULT_PIDFILE
	wait_before_remove = 3
	for arg in sys.argv[1:]:
		try:
			v = int(arg)
			wait_before_remove = v
			continue
		except Exception:
			pass
		pidfile_path = arg
	return (pidfile_path, wait_before_remove)


def main():
	logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
	pidfile_path, wait_before_remove = get_options()
	_log.info("PID file: %r (wait_before_remove=%d)", pidfile_path, wait_before_remove)
	pid_fp = ProcessIDFile(pidfile_path)
	v_nocheck = pid_fp.fetch()
	v_checked = pid_fp.fetch(check_running=True)
	_log.info("fetch: %r (no-check), %r (checked)", v_nocheck, v_checked)
	is_running = pid_fp.is_running()
	_log.info("is-running: %r", is_running)
	pid_fp.save()
	_log.info("save-ed ! waitt %d seconds before remove.", wait_before_remove)
	for cnt in xrange(wait_before_remove):
		tnc = wait_before_remove - cnt
		sys.stdout.write("\033[2K\rwaiting: %d." % (tnc, ))
		sys.stdout.flush()
		time.sleep(1)
	sys.stdout.write("\033[2K\rwait: 0.\n")
	pid_fp.remove()
	sys.stdout.write("\nExit.\n")


if __name__ == '__main__':
	main()
