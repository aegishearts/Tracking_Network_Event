#!/usr/local/bin/python3.7
import os,sys, getpass, re
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

from Running_Script import Query_DB as DB

import Interface_Status_Checker as PORT
import Ping_Check as PING
import CPU_Check as CPU
import BGP_Status_Checker as BGP
import OSPF_Status_Checker as OSPF
#### Ver1.2 ####

########################################################
ALL_Regex = re.compile(r'[bB][bB]+\d*-[a-zA-Z]+\d+-[a-zA-Z]+\d*|[aA][cC][cC]+\d+-[a-zA-Z]+\d+-[a-zA-Z]+\d*|[aA][gG][gG]+\d+-[a-zA-Z]+\d+-[a-zA-Z]+\d*|[rR][mM][cC]+\d+-[a-zA-Z]+\d+-[a-zA-Z]+\d*|mng+\d+-[a-zA-Z]+\d+-[a-zA-Z]+\d*|oob+\d+-[a-zA-Z]+\d+-[a-zA-Z]+\d*|sod+\d+-[a-zA-Z]+\d+-[a-zA-Z]+\d*|ssd+\d+-[a-zA-Z]+\d+-[a-zA-Z]+\d*|stk+\d+-[a-zA-Z]+\d+-[a-zA-Z]+\d*')

class color:
        HEADER = '\033[95m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        RED = '\033[31m'
        GREEN = '\033[32m'
        YELLOW = '\033[33m'
        BLUE = '\033[34m'
        RESET = '\033[0m'
########################################################

if __name__ == "__main__":
	Hostname = sys.argv[1]
	Event_Type = sys.argv[2]
	Vendor,POP = DB.Search_Host_NIDB(Hostname)
	if ALL_Regex.match(Hostname):
		Username = raw_input(color.RED+"Enter KSS username: "+color.RESET)
		Passwd = getpass.getpass(color.RED+"Enter KSS password: "+color.RESET)
	else:
		Username = raw_input(color.RED+"Enter CNC account username: "+color.RESET)
		Passwd = getpass.getpass(color.RED+"Enter CNC account password: "+color.RESET)
	if Event_Type == 'Port':
		if len(sys.argv) == 4:
			Event_Value = sys.argv[3]
			PORT.Status_Checker(Hostname, Vendor, Event_Value, Username, Passwd)
		else:
			print(color.RED+"Please Enter Port number!!!\n"+color.RESET)
	elif Event_Type == 'Ping':
		PING.Ping_test_from_NETADM(Hostname)
	elif Event_Type == 'CPU':
		CPU.CPU_Check(Hostname, Vendor, Username, Passwd)
	elif Event_Type == 'BGP':
		if len(sys.argv) == 4:
			Event_Value = sys.argv[3]
			BGP.PEER_Status_Checker(Hostname, Vendor, Event_Value, Username, Passwd)
		else:
			print(color.RED+"Please Enter BGP peer IP!!!\n"+color.RESET)
	elif Event_Type == 'OSPF':
		if len(sys.argv) == 4:
			Event_Value = sys.argv[3]
			OSPF.PEER_Status_Checker(Hostname, Vendor, Event_Value, Username, Passwd)
		else:
			print(color.RED+"Please Enter OSPF neighbor IP!!!\n"+color.RESET)
	else:
		print(color.RED)
		print('##### \''+Event_Type+'\' issue Checker #####')
		print('Need to create new script for this Event')
		print('Current support Type: Port / Ping / CPU / BGP / OSPF')
		print(color.RESET)
