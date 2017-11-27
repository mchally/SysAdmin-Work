import sys, commands, getopt
from socket import *
from daemon import daemonize

def mysocket(port=7888):
	s = socket(AF_INET, SOCK_DGRAM)

	try:
		s.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
	except NameError:
		s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

	s.bind(('', port))

	return s

def main():
	try:
		opts,args = getopt.getopt(sys.argv[1:], 'd')

	except getopt.GetoptError:
		print 'usage: %s [-d]' % sys.argv[0]
		sys.exit(1)

	for o,a in opts:
		if o == '-d': daemonize()

	s = mysocket()
	r = socket(AF_INET, SOCK_DGRAM)

	while 1:
		buf = ''
		data,addr = s.recvfrom(65536)

		if data == 'rusers':
			users = set()
			for l in commands.getoutput('who').split('\n'):
				try:
					users.add(l.split()[0])
				except IndexError:
					pass

			rv = '%s:   ' % gethostname()
			for u in users:
				rv += '%s ' % u

			#print rv

		s.sendto(rv, addr)

if __name__ == '__main__':
	main()
