import os,sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

from Running_Script import Run_Command as RUN
import re

### Ver1.2 ###

########################################################
CMD_BGP_Session = {
        'cisco-nx':'sh ip bgp sum | no-more',
        'cisco':'sh ip bgp sum',
        'ubiquoss':'show ip bgp sum',
        'huawei':'display bgp peer',
        'juniper':'sh bgp sum | no-more',
        'foundry':'sh ip bgp sum',
        'brocade_fabric':'sh ip bgp sum | nomore',
        'dell':'sh ip bgp sum | no-more',
        'arista':'sh ip bgp sum | no-more',
}

Regex_IPv4_Host = re.compile(r'^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')
Regex_IPv6_Host = re.compile(r'^\d{1,4}:{0,2}\d{0,4}:{0,2}\d{0,4}:{0,2}\d{0,4}:{0,2}\d{0,4}:{0,2}\d{0,4}:{0,2}\d{0,4}:{0,2}\d{0,4}:{0,2}')

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

def JUNOS_BGP_Session_List(HOST, VD, Username, Password):
	UP_List = {}
	DOWN_List = {}
	CMD = CMD_BGP_Session[VD]
	Result = RUN.Run_Command(HOST, VD, CMD, Username, Password)
	for i in Result:
		RL = str(i)
		LEN = len(RL.split())
		if Regex_IPv4_Host.match(RL) or Regex_IPv6_Host.match(RL):
			if 'Establ' in RL or 'Connect' in RL or 'Idle' in RL or 'Active' in RL or 'OpenConfirm' in RL or 'OpenSent' in RL:
				Status = RL.split()[-1]
				PEER = RL.split()[0]
				if LEN == 8:
					Flap_Time = RL.split()[-2]
				elif LEN == 9:
					Flap_Time = ' '.join(RL.split()[-3:-1])
			else:		
				Status = 'Establ'
				PEER = RL.split()[0]
				if LEN == 9:
					Flap_Time = RL.split()[-3]
				elif LEN == 10:
					Flap_Time = ' '.join(RL.split()[-4:-2])
			if Status == 'Connect' or Status == 'Idle' or Status == 'Active' or Status == 'OpenConfirm' or Status == 'OpenSent':
				DOWN_List[PEER] = Flap_Time 
			else:
				UP_List[PEER] = Flap_Time
	return UP_List, DOWN_List

def EOS_BGP_Session_List(HOST, VD, Username, Password):
	UP_List = {}
	DOWN_List = {}
	CMD = CMD_BGP_Session[VD]
	Result = RUN.Run_Command(HOST, VD, CMD, Username, Password)
	for i in Result:
		RL = str(i)
		if 'Connect' in RL or 'Idle' in RL or 'Active' in RL:
			Status = RL.split()[8]
			Flap_Time = RL.split()[7]
			PEER = RL.split()[0]
			DOWN_List[PEER] = Flap_Time 
		elif 'Estab' in RL:
			Status = RL.split()[8]
			Flap_Time = RL.split()[7]
			PEER = RL.split()[0]
			UP_List[PEER] = Flap_Time
	return UP_List, DOWN_List

def Huawei_BGP_Session_List(HOST, VD, Username, Password):
	UP_List = {}
	DOWN_List = {}
	CMD = CMD_BGP_Session[VD]
	Result = RUN.Run_Command(HOST, VD, CMD, Username, Password)
	for i in Result:
		RL = str(i)
		if 'Connect' in RL or 'Idle' in RL or 'Active' in RL:
			Status = RL.split()[8]
			Flap_Time = RL.split()[7]
			PEER = RL.split()[0]
			DOWN_List[PEER] = Flap_Time 
		elif 'Estab' in RL:
			Status = RL.split()[8]
			Flap_Time = RL.split()[7]
			PEER = RL.split()[0]
			UP_List[PEER] = Flap_Time
	return UP_List, DOWN_List

def IOS_BGP_Session_List(HOST, VD, Username, Password):
	UP_List = {}
	DOWN_List = {}
	CMD = CMD_BGP_Session[VD]
	Result = RUN.Run_Command(HOST, VD, CMD, Username, Password)
	for i in Result:
		RL = str(i)
		if Regex_IPv4_Host.match(RL) and 'never' in RL:
			Status = RL.split()[9]
			Flap_Time = RL.split()[8]
			PEER = RL.split()[0]
			DOWN_List[PEER] = Flap_Time 
		elif Regex_IPv4_Host.match(RL):
			Status = 'Established'
			Flap_Time = RL.split()[8]
			PEER = RL.split()[0]
			UP_List[PEER] = Flap_Time
	return UP_List, DOWN_List

def Foundry_BGP_Session_List(HOST, VD, Username, Password):
	UP_List = {}
	DOWN_List = {}
	CMD = CMD_BGP_Session[VD]
	Result = RUN.Run_Command(HOST, VD, CMD, Username, Password)
	for i in Result:
		RL = str(i)
		if 'CONN' in RL or 'ADMDN' in RL or 'IDLE' in RL:
			Status = RL.split()[2]
			Flap_Time = ' '.join(RL.split()[3:5])
			PEER = RL.split()[0]
			DOWN_List[PEER] = Flap_Time 
		elif 'ESTAB' in RL:
			Status = RL.split()[2]
			Flap_Time = ' '.join(RL.split()[3:5])
			PEER = RL.split()[0]
			UP_List[PEER] = Flap_Time
	return UP_List, DOWN_List

def Ping_Checker(HOST, VD, PEER, Username, Password):
	print(color.BLUE)
	print('### Start Ping Check!!!! ###')
	print(color.RESET)
	if VD == 'juniper':
		CMD = 'ping '+PEER+' count 3 wait 1'
	elif VD == 'arista' or VD == 'cisco':
		CMD = 'ping '+PEER+' repeat 3 timeout 1'
	elif VD == 'huawei':
		CMD = 'ping -c 1 '+PEER
	elif VD == 'dell' or VD == 'cisco-nx' or VD == 'brocade_fabric':
		CMD = 'ping '+PEER+' count 3 timeout 1'
	elif VD == 'ubiquoss':
		CMD = 'ping ip '+PEER+' repeat 3 timeout 1'
	elif VD == 'foundry':
		CMD = 'ping '+PEER+' count 3 timeout 1000'
	Result = '\n'.join(RUN.Run_Command(HOST, VD, CMD, Username, Password))
	if '100% packet loss' in Result or ' rate is 0 percent ' in Result or '100.00% packet loss' in Result or 'No reply from remote host.' in Result:
		print(color.RED)
		print('### Peer is unreachable!!!!!!!!!  ###')
		print(color.RESET)
		return False
	else:
		print(color.GREEN)
		print('### Peer is reachable!!!!!!!!!  ###')
		print(color.RESET)
		return True

def BGP_Session_List(HOST,VD, Username, Password):
	if VD == 'juniper':
		UL, DL = JUNOS_BGP_Session_List(HOST, VD, Username, Password)		
	elif VD == 'arista':
		UL, DL = EOS_BGP_Session_List(HOST, VD, Username, Password)		
	elif VD == 'huawei':
		UL, DL = Huawei_BGP_Session_List(HOST, VD, Username, Password)		
	elif VD == 'dell' or VD == 'cisco' or VD == 'ubiquoss' or VD == 'cisco-nx':
		UL, DL = IOS_BGP_Session_List(HOST, VD, Username, Password)		
	elif VD == 'foundry' or VD == 'brocade_fabric':
		UL, DL = Foundry_BGP_Session_List(HOST, VD, Username, Password)		
	print(DL)
	print(UL)
	return UL, DL

def Chase_PeerDownIssue(HOST, VD, PEER, Username, Password):
	print(color.BLUE)
	print('##### Check network reachability with Neighbor\'s IP!!! #####')
	print(color.RESET)
	PR = Ping_Checker(HOST, VD, PEER, Username, Password)
	if PR:
		print(color.RED)
		print('##### Need to check Detail. Please Escalate to Tier2  #####')
		print(color.RESET)
		### Need to display BGP log(limit max-prefix / MD5 mismatch)
	else:
		print(color.RED)
		print('##### Need to check network connectibity with Peer. Please Escalate to Tier2  #####')
		print(color.RESET)
		### Need to display detail (BGP config / session information-IX/Internal/ISP)

def Check_FlapTime(Time):
	if 'w' in Time or 'd' in Time:
		return False
	else:
		return True

def PEER_Status_Checker(Hostname, Vendor, Peer, Username, Password):
	print(color.BLUE)
        print('##### BGP issue Checker #####')
        print('##### Issue Device : '+Hostname+' #####')
        print('##### Issue PEER IP : '+Peer+' #####')
	print(color.RESET)

	BGP_UP_List, BGP_DOWN_List = BGP_Session_List(Hostname, Vendor, Username, Password)
	if Peer in BGP_UP_List:
		Flap_Status = Check_FlapTime(BGP_UP_List[Peer])
		if Flap_Status:
			print(color.RED)
			print('##### BGP Session was flapped. Please Escalate to Tier2 #####')
			print(color.RESET)
		else:
			print(color.GREEN)
			print('##### Session was not down. Ignore Alarm #####')
			print(color.RESET)
		
	elif Peer in BGP_DOWN_List:
		Flap_Status = Check_FlapTime(BGP_DOWN_List[Peer])
		print(color.RED)
		print('##### Peer is down #####\n##### Peer Down time #####\n'+BGP_DOWN_List[Peer])
		print(color.RESET)
		if Flap_Status:
			Chase_PeerDownIssue(Hostname,Vendor,Peer, Username, Password)
		else:
			print(color.RED)
			print('##### Unused session or old config. Need to clear. Please Escalate to Tier2 #####')
			print(color.RESET)
