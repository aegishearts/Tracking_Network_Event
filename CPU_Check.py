import os,sys, subprocess, re
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

from Running_Script import Run_Command as RUN

### Ver1.2 ###

########################################################
CMD_CPU = {
        'cisco-nx':'show system resources | no-more',
        'cisco':'show processes cpu',
        'ubiquoss':'show processes cpu',
        'huawei':'display cpu | no-more',
        'juniper':'show chassis routing-engine | no-more',
        'foundry':'show cpu-utilization',
        'brocade_fabric':'show process cpu summary | nomore',
        'dell':'show processes cpu | no-more',
        'arista':'show processes top once | no-more',
}

class colors:
	HEADER = '\033[95m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	RED = '\033[31m'
	GREEN = '\033[32m'
	YELLOW = '\033[33m'
	BLUE = '\033[34m'
	RESET = '\033[0m'

CPU_Value = re.compile(r'\d{1,3}.{0,1}\d{0,2}')
########################################################

def NXOS_CPU_Check(Host, VD, User, pwd):
	CMD = CMD_CPU[VD]
	Result = RUN.Run_Command(Host, VD, CMD, User, pwd)
	for i in Result:
		RL = str(i)
		if 'CPU states ' in RL:
			Value = RL.split()[-2]
	RT = float(CPU_Value.findall(Value)[0])
	return RT

def IOS_CPU_Check(Host, VD, User, pwd):
	CMD = CMD_CPU[VD]
	Result = RUN.Run_Command(Host, VD, CMD, User, pwd)
	for i in Result:
		RL = str(i)
		if 'CPU utilization ' in RL:
			Value = RL.split()[-1]
	RT = float('100')-float(Value.split('%')[0])
	return RT

def Ubi_CPU_Check(Host, VD, User, pwd):
	CMD = CMD_CPU[VD]
	Result = RUN.Run_Command(Host, VD, CMD, User, pwd)
	for i in Result:
		RL = str(i)
		if 'CPU states:' in RL:
			Value = RL.split()[-2]
	RT = float(CPU_Value.findall(Value)[0])
	return RT

def Foundry_CPU_Check(Host, VD, User, pwd):
	CMD = CMD_CPU[VD]
	Result = RUN.Run_Command(Host, VD, CMD, User, pwd)
	for i in Result:
		RL = str(i)
		if 'CPU utilization ' in RL:
			Value = RL.split()[-4]
	RT = float('100')-float(CPU_Value.findall(Value)[0].split('%')[0])
	return RT

def JUNOS_CPU_Check(Host, VD, User, pwd):
	RT = []
	CMD = CMD_CPU[VD]
	Result = RUN.Run_Command(Host, VD, CMD, User, pwd)
	for i in Result:
		RL = str(i)
		if 'Idle ' in RL:
			RT.append(float(RL.split()[-2]))
	return RT 

def EOS_CPU_Check(Host, VD, User, pwd):
	CMD = CMD_CPU[VD]
	Result = RUN.Run_Command(Host, VD, CMD, User, pwd)
	for i in Result:
		RL = str(i)
		if '%Cpu(s):' in RL:
			RT = float(RL.split()[7])
	return RT 

def Dell_CPU_Check(Host, VD, User, pwd):
	CMD = CMD_CPU[VD]
	Result = RUN.Run_Command(Host, VD, CMD, User, pwd)
	for i in Result:
		RL = str(i)
		if 'Overall' in RL:
			RT = float(RL.split()[-1])
	RT = float('100')-RT
	return RT 

def Bro_CPU_Check(Host, VD, User, pwd):
	CMD = CMD_CPU[VD]
	Result = RUN.Run_Command(Host, VD, CMD, User, pwd)
	for i in Result:
		RL = str(i)
		if 'Current:' in RL:
			RT = float(RL.split()[1].split('%')[0])
	RT = float('100')-RT
	return RT 

def Huawei_CPU_Check(Host, VD, User, pwd):
	CMD = CMD_CPU[VD]
	Result = RUN.Run_Command(Host, VD, CMD, User, pwd)
	for i in Result:
		RL = str(i)
		if 'CPU utilization for ' in RL:
			RT = float(RL.split()[-1].split('%')[0])
	RT = float('100')-RT
	return RT 

def CPU_Check(Hostname, Vendor, User, pwd):
	if Vendor == 'cisco-nx':
		IDLE_CPU = NXOS_CPU_Check(Hostname, Vendor, User, pwd)
	elif Vendor == 'cisco':
		IDLE_CPU = IOS_CPU_Check(Hostname, Vendor, User, pwd)
	elif Vendor == 'ubiquoss':
		IDLE_CPU = Ubi_CPU_Check(Hostname, Vendor, User, pwd)
	elif Vendor == 'foundry':
		IDLE_CPU = IOS_CPU_Check(Hostname, Vendor, User, pwd)
	elif Vendor == 'juniper':
		IDLE_CPU = JUNOS_CPU_Check(Hostname, Vendor, User, pwd)
	elif Vendor == 'arista':
		IDLE_CPU = EOS_CPU_Check(Hostname, Vendor, User, pwd)
	elif Vendor == 'dell':
		IDLE_CPU = Dell_CPU_Check(Hostname, Vendor, User, pwd)
	elif Vendor == 'brocade_fabric':
		IDLE_CPU = Bro_CPU_Check(Hostname, Vendor, User, pwd)
	elif Vendor == 'huawei':
		IDLE_CPU = Huawei_CPU_Check(Hostname, Vendor, User, pwd)
	Status = ''
	if Vendor == 'juniper':
		if IDLE_CPU == []:
			Status = 'NoData'
		else:
			for i in IDLE_CPU:
				if i < float('10.00'):
					Status = 'Issue'
	else:
		if IDLE_CPU == '':
			Status = 'NoData'
		else:
			if IDLE_CPU < float('10.00'):
				Status = 'Issue'
	if Status == 'Issue':
		print(colors.RED)
		print('CPU Usage issue!!!\n'+'Idle CPU:')
		print(IDLE_CPU)
		print('Escalate to Tier2')
		print(colors.RESET)
	elif Status == 'NoData':
		print(colors.RED)
		print('You fail to get information from device. Check your Account is correct or device is working')
		print(colors.RESET)
	else:
		print(colors.GREEN)
		print('False Alarm!!!\n'+'Idle CPU:')
		print(IDLE_CPU)
		print('Ignore this alarm')
		print(colors.RESET)
