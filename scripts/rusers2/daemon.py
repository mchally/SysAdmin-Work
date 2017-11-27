import os, sys, time

def daemonize():
	try:
		pid = os.fork()
		if pid > 0:
			id,status = os.waitpid(pid, 0)
			sys.exit(0)

	except OSError, e:
		print >> sys.stderr, 'fork() ERROR:', e.errno, e.strerror
		sys.exit(1)

	os.chdir('/')
	os.setsid()
	os.umask(0)

	try:
		pid = os.fork()
		if pid > 0:
			time.sleep(0.2)

			id,status = os.waitpid(pid, os.WNOHANG)
			if id == 0: sys.exit(0)

			print '-->', id,status
			print 'WCOREDUMP', os.WCOREDUMP(status)
			print 'WIFCONTINUED', os.WIFCONTINUED(status)
			print 'WIFSTOPPED', os.WIFSTOPPED(status)
			print 'WIFSIGNALED', os.WIFSIGNALED(status)
			print 'WIFEXITED', os.WIFEXITED(status)
			print 'WEXITSTATUS', os.WEXITSTATUS(status)
			print 'WSTOPSIG', os.WSTOPSIG(status)
			print 'WTERMSIG', os.WTERMSIG(status)

			sys.exit(0)
	except OSError, e:
		print >> sys.stderr, 'fork() ERROR:', e.errno, e.strerror
		sys.exit(1)

	pid = os.getpid()
	print 'River daemon pid', pid

	os.close(0)
	os.close(1)
	os.close(2)

	sys.stdin.close()
	sys.stdout.close()
	sys.stderr.close()

	fd = os.open('/dev/null', os.O_RDWR)
	fd = os.open('/tmp/river_%d.log' % pid, os.O_RDWR | os.O_CREAT, 0644)
	os.dup2(1, 2)

	sys.stdin = os.fdopen(0)
	sys.stdout = os.fdopen(1, 'a')
	sys.stderr = sys.stdout

	print '--- River daemon started  ---'
	sys.stdout.flush()

