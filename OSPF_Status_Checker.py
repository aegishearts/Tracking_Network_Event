import os,sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

from Running_Script import Run_Command as RUN
import Interface_Status_Checker as PORT
import re, socket

### Ver1.2 ###

########################################################
CMD_OSPF_Neighbor = {
        'cisco-nx':'sh ip ospf neighbors',
        'cisco':'sh ip ospf neighbor',
        'ubiquoss':'show ip ospf neighbor',
        'huawei':'display ospf peer brief | no-more',
        'juniper':'show ospf neighbor | no-more',
        'foundry':'show ospf neighbor',
        'brocade_fabric':'show ip ospf neighbor | nomore',
        'dell':'show ip ospf neighbor | no-more',
        'arista':'show ip ospf neighbor | no-more',
}

Regex_IPv4_Host = re.compile('(([2][5][0-5]\.)|([2][0-4][0-9]\.)|([0-1]?[0-9]?[0-9]\.)){3}'+'(([2][5][0-5])|([2][0-4][0-9])|([0-1]?[0-9]?[0-9]))')
Regex_IPv6_Host = re.compile(r'\d{1,4}:{0,2}\d{0,4}:{0,2}\d{0,4}:{0,2}\d{0,4}:{0,2}\d{0,4}:{0,2}\d{0,4}:{0,2}\d{0,4}:{0,2}\d{0,4}:{0,2}')

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

def NXOS_OSPF_Nei_List(HOST, VD, Username, Password):
        UP_List = {}
        DOWN_List = {}
        CMD = CMD_OSPF_Neighbor[VD]
        Result = RUN.Run_Command(HOST, VD, CMD, Username, Password)
        for i in Result:
                RL = str(i)
                if Regex_IPv4_Host.search(RL):
                        Status = RL.split()[2]
                        Interface = RL.split()[-1]
                        Neighbor = RL.split()[-2]
                        if 'FULL' in Status:
                                UP_List[Neighbor] = Interface 
			else:	
                                DOWN_List[Neighbor] = Interface
        return UP_List, DOWN_List

def IOS_OSPF_Nei_List(HOST, VD, Username, Password):
        UP_List = {}
        DOWN_List = {}
        CMD = CMD_OSPF_Neighbor[VD]
        Result = RUN.Run_Command(HOST, VD, CMD, Username, Password)
        for i in Result:
                RL = str(i)
                if Regex_IPv4_Host.search(RL):
                        Status = RL.split()[2]
                        Interface = RL.split()[-1]
                        Neighbor = RL.split()[0]
                        if 'FULL' in Status:
                                UP_List[Neighbor] = Interface 
			else:	
                                DOWN_List[Neighbor] = Interface
        return UP_List, DOWN_List

def EOS_OSPF_Nei_List(HOST, VD, Username, Password):
        UP_List = {}
        DOWN_List = {}
        CMD = CMD_OSPF_Neighbor[VD]
        Result = RUN.Run_Command(HOST, VD, CMD, Username, Password)
        for i in Result:
                RL = str(i)
                if Regex_IPv4_Host.search(RL):
                        Status = RL.split()[3]
                        Interface = RL.split()[-1]
                        Neighbor = RL.split()[0]
                        if 'FULL' in Status:
                                UP_List[Neighbor] = Interface 
			else:	
                                DOWN_List[Neighbor] = Interface
        return UP_List, DOWN_List

def JUNOS_OSPF_Nei_List(HOST, VD, Username, Password):
        UP_List = {}
        DOWN_List = {}
        CMD = CMD_OSPF_Neighbor[VD]
        Result = RUN.Run_Command(HOST, VD, CMD, Username, Password)
        for i in Result:
                RL = str(i)
                if Regex_IPv4_Host.search(RL) or Regex_IPv6_Host.match(RL):
                        Status = RL.split()[2]
                        Interface = RL.split()[1]
                        Neighbor = RL.split()[0]
                        if 'Full' in Status:
                                UP_List[Neighbor] = Interface 
			else:	
                                DOWN_List[Neighbor] = Interface
        return UP_List, DOWN_List

def Foundry_OSPF_Nei_List(HOST, VD, Username, Password):
        UP_List = {}
        DOWN_List = {}
        CMD = CMD_OSPF_Neighbor[VD]
        Result = RUN.Run_Command(HOST, VD, CMD, Username, Password)
        for i in Result:
                RL = str(i)
                if Regex_IPv4_Host.search(RL):
                        Status = RL.split()[3]
                        Interface = RL.split()[0]
                        Neighbor = RL.split()[4]
                        if 'FULL' in Status:
                                UP_List[Neighbor] = Interface 
			else:	
                                DOWN_List[Neighbor] = Interface
        return UP_List, DOWN_List

def Huawei_OSPF_Nei_List(HOST, VD, Username, Password):
        UP_List = {}
        DOWN_List = {}
        CMD = CMD_OSPF_Neighbor[VD]
        Result = RUN.Run_Command(HOST, VD, CMD, Username, Password)
        for i in Result:
                RL = str(i)
                if Regex_IPv4_Host.search(RL):
                        Status = RL.split()[-1]
                        Interface = RL.split()[1]
                        Neighbor = RL.split()[2]
                        if 'Full' in Status:
                                UP_List[Neighbor] = Interface 
			else:	
                                DOWN_List[Neighbor] = Interface
        return UP_List, DOWN_List

def Brocade_OSPF_Nei_List(HOST, VD, Username, Password):
        UP_List = {}
        DOWN_List = {}
        CMD = CMD_OSPF_Neighbor[VD]
        Result = RUN.Run_Command(HOST, VD, CMD, Username, Password)
        for i in Result:
                RL = str(i)
                if Regex_IPv4_Host.search(RL):
                        Status = RL.split()[3]
                        Interface = RL.split()[0:2]
                        Neighbor = RL.split()[4]
                        if 'FULL' in Status:
                                UP_List[Neighbor] = Interface 
			else:	
                                DOWN_List[Neighbor] = Interface
        return UP_List, DOWN_List

def Dell_OSPF_Nei_List(HOST, VD, Username, Password):
        UP_List = {}
        DOWN_List = {}
        CMD = CMD_OSPF_Neighbor[VD]
        Result = RUN.Run_Command(HOST, VD, CMD, Username, Password)
        for i in Result:
                RL = str(i)
                if Regex_IPv4_Host.search(RL):
                        Status = RL.split()[2]
			if len(RL.split()) == 8:
                        	Interface = RL.split()[-3][15:]+' '+RL.split()[-2]
			elif len(RL.split()) == 9:
				Interface = ' '.join(RL.split()[-3:-1])
                        Neighbor = RL.split()[0]
                        if 'FULL' in Status:
                                UP_List[Neighbor] = Interface 
			else:	
                                DOWN_List[Neighbor] = Interface
        return UP_List, DOWN_List

def OSPF_Neighbor_List(HOST, VD, Username, Password):
	if VD == 'cisco-nx':
		UL, DL = NXOS_OSPF_Nei_List(HOST, VD, Username, Password)
	elif VD == 'cisco' or VD == 'ubiquoss':
		UL, DL = IOS_OSPF_Nei_List(HOST, VD, Username, Password)
	elif VD == 'arista':
		UL, DL = EOS_OSPF_Nei_List(HOST, VD, Username, Password)
	elif VD == 'juniper':
		UL, DL = JUNOS_OSPF_Nei_List(HOST, VD, Username, Password)
	elif VD == 'foundry':
		UL, DL = Foundry_OSPF_Nei_List(HOST, VD, Username, Password)
	elif VD == 'huawei':
		UL, DL = Huawei_OSPF_Nei_List(HOST, VD, Username, Password)
	elif VD == 'brocade_fabric':
		UL, DL = Brocade_OSPF_Nei_List(HOST, VD, Username, Password)
	elif VD == 'dell':
		UL, DL = Dell_OSPF_Nei_List(HOST, VD, Username, Password)
        print(DL)
        print(UL)
        return UL, DL

def PEER_Status_Checker(Hostname, Vendor, Neighbor, Username, Password):
	print(color.BLUE)
	print('##### OSPF issue Checker #####')
        print('##### Issue Device : '+Hostname+' #####')
        print('##### Issue Neighbor IP : '+Neighbor+' #####')
	print(color.RESET)

	OSPF_FULL_List, OSPF_DOWN_List = OSPF_Neighbor_List(Hostname, Vendor, Username, Password)
	if Neighbor in OSPF_DOWN_List:
		PORT = OSPF_DOWN_List[Neighbor]
		print(color.RED)
		print('##### OSPF Session is Down #####')
		print('##### Neighbor IP : '+Neighbor+' / Interface : '+PORT+' #####')
		print('##### Start to check interface status #####')
		print(color.RESET)
		PORT_Status = PORT.Query_Interface_Information(Hostname, Vendor, PORT, Username, Password)['LS']
		if PORT_Status == 'Up' or PORT_Status == 'up':
			print(color.RED)
			print('##### Need to check detail. Please Escalate to Tier2 #####')
			print(color.RESET)
			### Need to add provide port information (PORT_Status)
			#print(PORT_Status)
		else:
			print(color.RED)
			print('##### Interface fault issue. Need to check interface status #####')
			print(color.RESET)
			PORT.Status_Checker(Hostname, Vendor, PORT, Username, Password)
	elif Neighbor in OSPF_FULL_List:
		print(color.GREEN)
                print('### OSPF Session is Full, Ignore Alarm ###')
		print(color.RESET)
