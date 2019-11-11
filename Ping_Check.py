import os,sys, subprocess
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

### Ver1.2 ###

########################################################
class colors:
	HEADER = '\033[95m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	RED = '\033[31m'
	GREEN = '\033[32m'
	YELLOW = '\033[33m'
	BLUE = '\033[34m'
	RESET = '\033[0m'
########################################################

def Ping_test_from_NETADM(Hostname):
	cmd = ['ping','-c','5',Hostname]
	f_popen = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
	data = f_popen.read().strip()
	f_popen.close()

	D = data.split('\n')
	for i in D:
		if ' packet loss,' in i:
			if ' 100% packet loss, ' in i:
				print(colors.RED)
				print('Network Unreachable!!!\nEscalate to Tier2')
				print(colors.RESET)
			else:
				print(colors.GREEN)
				print('Network Reachable!!!\nIgnore this alarm')
				print(colors.RESET)
