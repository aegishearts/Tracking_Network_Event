import os,sys
from datetime import date
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

from Running_Script import Run_Command as RUN
import re

### Ver1.2 ###

########################################################

Foundry_Port_Number_Regex = re.compile(r'\d{1,2}/\d{1,2}/{0,1}\d{0,2}')

CMD_Target_Port = {
	'cisco-nx':'show int ',
	'cisco':'show int ',
	'ubiquoss':'show interface ',
	'huawei':'display interface ',
	'juniper':'sh int ',
	'foundry':'sh int ',
	'brocade_fabric':'show int ',
	'dell':'show int ',
	'arista':'sh int ',
}
CMD_Target_Optic = {
	'cisco-nx':'sh int ',
	'cisco':'sh int ',
	'ubiquoss':'show interface transceiver detail | in ',
	'huawei':'display interface ',
	'juniper':'sh interfaces diagnostics optics ',
	'foundry':'show optic ',
	'brocade_fabric':'show media interface ',
	'dell':'show int ',
	'arista':'show int ',
}

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

def JUNOS_Interface_Check(Hostname, VD, PT, Username, Password):
	if 'Te' in PT:
		PT = PT.replace('Te','xe-')
	elif 'et' in PT:
		PT = PT.replace('et','et-')
	elif 'gi' in PT:
		PT = PT.replace('gi','ge-')
	elif 'Gi' in PT:
		PT = PT.replace('Gi','ge-')
	CMD = CMD_Target_Port[VD]+PT+' | no-more'
	Result = RUN.Run_Command(Hostname,VD,CMD, Username, Password)
	DIC = {}
	for i in Result:
		RL = str(i)
		if 'Physical interface:' in RL:
			LS = RL.split()[-1]
			DIC['LS'] = str(LS)
		elif 'Description' in RL:
			DSC = RL.split()[-1]
			DIC['DSC'] = str(DSC)
		elif 'Bit errors' in RL:
			IE = RL.split()[-1]
			DIC['IE'] = IE
			DIC['OE'] = str(None)
		elif 'Errored blocks' in RL:
			CRC = RL.split()[-1]
			DIC['CRC'] = str(CRC)
		elif 'Hardware address:' in RL:
			MAC = RL.split()[-1]
			DIC['MAC'] = str(MAC)
		elif 'Input packets :' in RL:
			IP = RL.split()[-1]
			DIC['IP'] = str(IP)	
		elif 'Output packets:' in RL:
			OP = RL.split()[-1]
			DIC['OP'] = str(OP)	
		elif 'Input rate ' in RL:
			IB = RL.split()[-4]
			DIC['IB'] = str(IB)	
		elif 'Output rate ' in RL:
			OB = RL.split()[-4]
			DIC['OB'] = str(OB)	
		elif 'Last flapped' in RL:
			FT = ' '.join(RL.split()[-3:])[1:-5]
			DIC['FT'] = str(FT)
	return DIC

def CISCO_IOS_Interface_Check(Hostname, VD, PT, Username, Password):
	CMD = CMD_Target_Port[VD]+PT
	Result = RUN.Run_Command(Hostname,VD,CMD, Username, Password)
	DIC = {}
	for i in Result:
		RL = str(i)
		if 'line protocol is ' in RL:
			if 'down' in RL or 'notpresent' in RL:
				DIC['LS'] = 'down'
			else:
				DIC['LS'] = 'up'
		elif 'Description' in RL:
			DSC = RL.split()[1]
			DIC['DSC'] = DSC
		elif 'input errors,' in RL:
			IE = RL.split()[0]
			CRC = RL.split()[3]
			DIC['IE'] = IE
			DIC['CRC'] = CRC
		elif 'output errors,' in RL:
			OE = RL.split()[0]
			DIC['OE'] = OE
		elif 'Hardware is ' in RL and 'address is ' in RL:
			MAC = RL.split()[-3]
			DIC['MAC'] = MAC
		#elif 'packets input,' in RL:
		#	IP = RL.split()[0]
		#elif 'packets output,' in RL:
		#	OP = RL.split()[0]
	CMD = 'sh dtp interface '+PT
        Result = RUN.Run_Command(Hostname,VD,CMD, Username, Password)
	for i in Result:
		RL = str(i)
		if 'last link down on ' in RL:
			FT = ' '.join(RL.split()[8:])
			DIC['FT'] = FT
	if not 'FT' in DIC.keys():
		DIC['FT'] = None
	return DIC
	
def CISCO_NXOS_Interface_Check(Hostname, VD, PT, Username, Password):
	CMD = CMD_Target_Port[VD]+PT
	Result = RUN.Run_Command(Hostname,VD,CMD, Username, Password)
	DIC = {}
	for i in Result:
		RL = str(i)
		if ' is up' in RL or ' is down' in RL:
			LS = RL.split()[2]
			DIC['LS'] = LS
		elif 'Description' in RL:
			DSC = RL.split()[1]
			DIC['DSC'] = DSC
		elif 'input error' in RL:
			IE = RL.split()[0]
			DIC['IE'] = IE
		elif 'output error' in RL:
			OE = RL.split()[0]
			DIC['OE'] = OE
		elif 'CRC' in RL:
			CRC = RL.split()[4]
			DIC['CRC'] = CRC
		elif 'Hardware:' in RL and 'address:' in RL:
			MAC = RL.split()[-3]
			DIC['MAC'] = MAC
		#elif 'input packets' in RL:
		#	IP = RL.split()[0]
		#elif 'output packets' in RL:
		#	OP = RL.split()[0]
		elif 'Last link flapped' in RL:
			FT = ' '.join(RL.split()[3:])
			DIC['FT'] = FT
	return DIC

def UBIQ_Interface_Check(Hostname, VD, PT, Username, Password):
	CMD = CMD_Target_Port[VD]+PT
	Result = RUN.Run_Command(Hostname,VD,CMD, Username, Password)
	DIC = {}
	for i in Result:
		RL = str(i)
		if 'line protocol is ' in RL:
			if 'down' in RL or 'notpresent' in RL:
				DIC['LS'] = 'down'
			else:
				DIC['LS'] = 'up'
		elif 'Description' in RL:
			DSC = RL.split()[1]
			DIC['DSC'] = DSC
		elif 'Current HW addr:' in RL:
			MAC = RL.split()[-1]
			DIC['MAC'] = MAC
		elif 'CRC,' in RL:
			CRC = RL.split()[0]
			DIC['IE'] = None
			DIC['OE'] = None
			DIC['CRC'] = CRC
		#elif ' packets input,' in RL:
		#	IP = RL.split()[0]
		#elif ' packets output,' in RL:
		#	OP = RL.split()[0]
	DIC['FT'] = None
	return DIC

def Foundry_Interface_Check(Hostname, VD, PT, Username, Password):
	CMD = CMD_Target_Port[VD]+PT
	Result = RUN.Run_Command(Hostname,VD,CMD, Username, Password)
	DIC = {}
	for i in Result:
		RL = str(i)
		if 'line protocol is ' in RL:
			if 'down' in RL or 'notpresent' in RL:
				DIC['LS'] = 'down'
			else:
				DIC['LS'] = 'up'
		elif 'Port name is ' in RL:
			DSC = RL.split()[-1]
			DIC['DSC'] = DSC
		elif 'input errors,' in RL:
			IE = RL.split()[0]
			CRC = RL.split()[3]
			DIC['IE'] = IE
			DIC['CRC'] = CRC
		elif 'output errors,' in RL:
			OE = RL.split()[0]
			DIC['OE'] = OE
		elif 'Hardware is ' in RL and 'address is ' in RL:
			MAC = RL.split()[-3]
			DIC['MAC'] = MAC
		#elif 'packets input,' in RL:
		#	IP = RL.split()[0]
		#elif 'packets output,' in RL:
		#	OP = RL.split()[0]
	DIC['FT'] = None
	return DIC

def Brocade_Interface_Check(Hostname, VD, PT, Username, Password):
	PTNo = Foundry_Port_Number_Regex.findall(PT)[0]
	PTTy = re.findall("[a-zA-Z]+",PT)[0]
	CMD = CMD_Target_Port[VD]+PTTy+' '+PTNo
	print(CMD)
	Result = RUN.Run_Command(Hostname,VD,CMD, Username, Password)
	DIC = {}
	for i in Result:
		RL = str(i)
		if 'line protocol is ' in RL:
			if 'down' in RL or 'notpresent' in RL:
				DIC['LS'] = 'down'
			else:
				DIC['LS'] = 'up'
		elif 'Description:' in RL:
			DSC = RL.split()[-1]
			DIC['DSC'] = DSC
		elif 'CRC' in RL:
			CRC = RL.split()[-3].split(',')[0]
			DIC['CRC'] = CRC
		elif 'Hardware is ' in RL and 'address is ' in RL:
			MAC = RL.split()[-1]
			DIC['MAC'] = MAC
		elif 'Time since last interface status change:' in RL:
			FT = RL.split()[-1]
			DIC['FT'] = FT
	IE = str(Result[Result.index(u'Receive Statistics:')+7]).split()[1]
	DIC['IE'] = IE
	OE = str(Result[Result.index(u'Transmit Statistics:')+4]).split()[1]
	DIC['OE'] = OE
	#IP = str(Result[Result.index(u'Receive Statistics:')+1]).split()[0]
	#OP = str(Result[Result.index(u'Transmit Statistics:')+1]).split()[0]
	return DIC

def Dell_Interface_Check(Hostname, VD, PT, Username, Password):
	CMD = CMD_Target_Port[VD]+PT+' | no-more'
	Result = RUN.Run_Command(Hostname,VD,CMD, Username, Password)
	DIC = {}
	for i in Result:
		RL = str(i)
		if 'line protocol is ' in RL:
			if 'down' in RL or 'notpresent' in RL:
				DIC['LS'] = 'down'
			else:
				DIC['LS'] = 'up'
		elif 'Description:' in RL:
			DSC = RL.split()[-1]
			DIC['DSC'] = DSC
		#elif 'input errors,' in RL:
		#	IE = RL.split()[0]
		#	print('\n###Input errors###\n'+IE)
		#elif 'output errors,' in RL:
		#	OE = RL.split()[0]
		#	print('\n###Output errors###\n'+OE)
		elif 'CRC,' in RL:
			CRC = RL.split()[0]
			DIC['CRC'] = CRC
		elif 'Hardware is ' in RL and 'address is ' in RL:
			MAC = RL.split()[-1]
			DIC['MAC'] = MAC
		elif 'Time since last interface status change:' in RL:
			FT = RL.split()[-1]
			DIC['FT'] = FT
	DIC['IE'] = None
	DIC['OE'] = None
	#IP = str(Result[Result.index(u'Input Statistics:')+1]).split()[0]
	#OP = str(Result[Result.index(u'Output Statistics:')+1]).split()[0]
	return DIC

def EOS_Interface_Check(Hostname, VD, PT, Username, Password):
	CMD = CMD_Target_Port[VD]+PT
	Result = RUN.Run_Command(Hostname,VD,CMD, Username, Password)
	DIC = {}
	for i in Result:
		RL = str(i)
		RL = str(i)
		if 'line protocol is ' in RL:
			if 'down' in RL or 'notpresent' in RL:
				DIC['LS'] = 'down'
			else:
				DIC['LS'] = 'up'
		elif 'Description:' in RL:
			DSC = RL.split()[-1]
			DIC['DSC'] = DSC
		elif 'input errors,' in RL:
			IE = RL.split()[0]
			CRC = RL.split()[3]
			DIC['IE'] = IE
			DIC['CRC'] = CRC
		elif 'output errors,' in RL:
			OE = RL.split()[0]
			DIC['OE'] = OE
		elif 'Hardware is ' in RL and 'address is ' in RL:
			MAC = RL.split()[-1]
			DIC['MAC'] = MAC
		elif 'Up' in RL and 'days' in RL:
			FT = ' '.join(RL.split()[1:])
			DIC['FT'] = FT
		elif 'Down' in RL and 'days' in RL:
			FT = ' '.join(RL.split()[1:])
			DIC['FT'] = FT
		#elif 'packets input,' in RL:
		#	IP = RL.split()[0]
		#elif 'packets output,' in RL:
		#	OP = RL.split()[0]
	return DIC

def Huawei_Interface_Check(Hostname, VD, PT, Username, Password):
	if 'Fg' in PT:
		PT = PT.replace('Fg','40GE')
	elif 'Te' in PT:
		PT = PT.replace('Te','10GE')
	CMD = CMD_Target_Port[VD]+PT
	Result = RUN.Run_Command(Hostname,VD,CMD, Username, Password)
	DIC = {}
	for i in Result:
		RL = str(i)
		if PT+' current state : ' in RL:
			if 'UP' in RL:
				DIC['LS'] = 'up'
			else:
				DIC['LS'] = 'down'
		elif 'Description:' in RL:
			if len(RL.split()) == 1:
				DSC = None
			else:
				DSC = RL.split()[-1]
			DIC['DSC'] = DSC
		elif 'Total Error:' in RL:
			IE = RL.split()[-1]
			OE = None
			DIC['IE'] = IE
			DIC['OE'] = OE
		elif 'CRC:' in RL:
			CRC = RL.split()[1].split(',')[0]
			DIC['CRC'] = CRC
		elif 'Hardware address is ' in RL:
			MAC = RL.split()[-1]
			DIC['MAC'] = MAC
		#elif 'Input,' in RL and 'packets' in RL:
		#	IP = RL.split()[4]
		#elif 'Output,' in RL and 'packets' in RL:
		#	OP = RL.split()[4]
		elif 'Last physical down time : ' in RL:
			FT = ' '.join(RL.split()[-2:])
			DIC['FT'] = FT
	return DIC

def JUNOS_Optical_Check(Hostname, VD, PT, Username, Password):
	Optic_status = {}
	Out_P = ''
	In_P = ''
	CMD = CMD_Target_Optic[VD]+PT+' | no-more'
	Result = RUN.Run_Command(Hostname,VD,CMD, Username, Password)
	for i in Result:
		RL = str(i)
		if 'Laser output power' in RL and 'high' not in RL and 'low' not in RL:
			Out_P = RL.split()[7]
		if 'Laser output power high warning threshold' in RL:
			Out_H = RL.split()[10]
		if 'Laser output power low warning threshold' in RL:
			Out_L = RL.split()[10]
		elif 'Laser rx power' in RL and 'high' not in RL and 'low' not in RL:
			In_P = RL.split()[7]
		elif 'Receiver signal average optical power' in RL:
			In_P = RL.split()[9]
		elif 'Laser rx power high warning threshold' in RL:
			In_H = RL.split()[10]
		elif 'Laser rx power low warning threshold' in RL:
			In_L = RL.split()[10]
	if Out_P == '':
		print('No optical port or not support power checker')
	elif In_P == '':
		print('No optical port or not support power checker')
	else:
		Optic_status[PT] = [Out_P, Out_H, Out_L, In_P, In_H, In_L]
                Output_power = float(Out_P)
                Output_high_limit = float(Out_H)
                Output_low_limit = float(Out_L)
                Input_power = float(In_P)
                Input_high_limit = float(In_H)
                Input_low_limit = float(In_L)
                if Output_power < Output_high_limit and Output_power > Output_low_limit:
			Input_error = False			
		else:
			Input_error = True
		Optic_status[PT].append(Input_error)
		if Input_power < Input_high_limit and Input_power > Input_low_limit:
			Output_error = False			
		else:
			Output_error = True
		Optic_status[PT].append(Output_error)
		if Input_error and Output_error:
                	print('Output/Input optical power is normal')
                else:
                	print('Optical issue!!! Need to check physical port and cable!!')

	return Optic_status

def CISCO_IOS_Optical_Check(Hostname, VD, PT, Username, Password):
	Optic_status = {}
	CMD = CMD_Target_Optic[VD]+PT+' transceiver details'
	Result = RUN.Run_Command(Hostname,VD,CMD, Username, Password)
	print(Result)
	for i in Result:
		RL = str(i)
		if 'Tx Power' in RL:
			OP = ' '.join(RL.split()[2:3])
			print('\n###Send Power###\n'+OP)
		elif 'Rx Power' in RL:
			RP = ' '.join(RL.split()[2:3])
			print('\n###Receive Power###\n'+RP)
	Optic_status[PT] = [OP, RP]
	return Optic_status

def CISCO_NXOS_Optical_Check(Hostname, VD, PT, Username, Password):
	Optic_status = {}
	CMD = CMD_Target_Optic[VD]+PT+' transceiver details'
	Result = RUN.Run_Command(Hostname,VD,CMD, Username, Password)
	for i in Result:
		RL = str(i)
		if 'Tx Power' in RL:
			OP = ' '.join(RL.split()[2:4])
			print('\n###Send Power###\n'+OP)
		elif 'Rx Power' in RL:
			RP = ' '.join(RL.split()[2:4])
			print('\n###Receive Power###\n'+RP)
	Optic_status[PT] = [OP, RP]
	return Optic_status

def Ubi_Optical_Check(Hostname, VD, PT, Username, Password):
	Optic_status = {}
	CMD = CMD_Target_Optic[VD]+PT
	Result = RUN.Run_Command(Hostname,VD,CMD, Username, Password)
	OP = Result[-2].split()[1]
	RP = Result[-1].split()[1]
	print('\n###Send Power###\n'+OP)
	print('\n###Receive Power###\n'+RP)
	Optic_status[PT] = [OP, RP]
	return Optic_status

def Foundry_Optical_Check(Hostname, VD, PT, Username, Password):
	Optic_status = {}
	Slot = Foundry_Port_Number_Regex.findall(PT)[0]
	CMD = CMD_Target_Optic[VD]+Slot.split('/')[0]
	Result = RUN.Run_Command(Hostname,VD,CMD, Username, Password)
	for i in Result:
		RL = str(i)
		if Slot in RL:
			OP = ' '.join(RL.split()[3:5])
			RP = ' '.join(RL.split()[5:7])
			print('\n###Send Power###\n'+OP)
			print('\n###Receive Power###\n'+RP)
	Optic_status[PT] = [OP, RP]
	return Optic_status

def Brocade_Optical_Check(Hostname, VD, PT, Username, Password):
	Optic_status = {}
	CMD = CMD_Target_Optic[VD]+Slot.split('/')[0]
	Result = RUN.Run_Command(Hostname,VD,CMD, Username, Password)
	for i in Result:
		RL = str(i)
		if Slot in RL:
			OP = ' '.join(RL.split()[3:5])
			RP = ' '.join(RL.split()[5:7])
			print('\n###Send Power###\n'+OP)
			print('\n###Receive Power###\n'+RP)
	Optic_status[PT] = [OP, RP]
	return Optic_status

def Dell_Optical_Check(Hostname, VD, PT, Username, Password):
	Optic_status = {}
	CMD = CMD_Target_Optic[VD]+PT+' transceiver | no-more'
	Result = RUN.Run_Command(Hostname,VD,CMD, Username, Password)
	for i in Result:
		RL = str(i)
		if 'Tx Power' in RL and 'Alarm' not in RL and 'Threshold' not in RL and 'Warning' not in RL:
			OP = RL.split()[-1]
			print('\n###Send Power###\n'+OP)
		elif 'Rx Power' in RL and 'Alarm' not in RL and 'Threshold' not in RL and 'Warning' not in RL:
			RP = RL.split()[-1]
			print('\n###Receive Power###\n'+RP)
	Optic_status[PT] = [OP, RP]
	return Optic_status

def EOS_Optical_Check(Hostname, VD, PT, Username, Password):
	Optic_status = {}
	CMD = CMD_Target_Optic[VD]+PT+' transceiver'
	Result = RUN.Run_Command(Hostname,VD,CMD, Username, Password)
	for i in Result:
		RL = str(i)
		if PT in RL:
			OP = RL.split()[4]
			print('\n###Send Power###\n'+OP)
			RP = RL.split()[5]
			print('\n###Receive Power###\n'+RP)
	Optic_status[PT] = [OP, RP]
	return Optic_status

def Huawei_Optical_Check(Hostname, VD, PT, Username, Password):
	Optic_status = {}
	CMD = CMD_Target_Optic[VD]+PT+' transceiver verbose'
	Result = RUN.Run_Command(Hostname,VD,CMD, Username, Password)
	for i in Result:
		RL = str(i)
		if 'Current RX Power (dBm)' in RL:
			OP = RL.split()[-1]
			print('\n###Send Power###\n'+OP)
		elif 'Current TX Power (dBm)' in RL:
			RP = RL.split()[-1]
			print('\n###Receive Power###\n'+RP)
	Optic_status[PT] = [OP, RP]
	return Optic_status

def Query_Interface_Optic(Hostname, VD, PT, Username, Password):
	if VD == 'juniper':
		OS = JUNOS_Optical_Check(Hostname, VD, PT, Username, Password)
	elif VD == 'cisco':
		OS = CISCO_IOS_Optical_Check(Hostname, VD, PT, Username, Password)
	elif VD == 'cisco-nx':
		OS = CISCO_NXOS_Optical_Check(Hostname, VD, PT, Username, Password)
	elif VD == 'ubiquoss':
		OS = Ubi_Optical_Check(Hostname, VD, PT, Username, Password)
	elif VD == 'foundry':
		OS = Foundry_Optical_Check(Hostname, VD, PT, Username, Password)
	elif VD == 'brocade_fabric':
		OS = Brocade_Optical_Check(Hostname, VD, PT, Username, Password)
	elif VD == 'dell':
		OS = Dell_Optical_Check(Hostname, VD, PT, Username, Password)
	elif VD == 'arista':
		OS = EOS_Optical_Check(Hostname, VD, PT, Username, Password)
	elif VD == 'huawei':
		OS = Huawei_Optical_Check(Hostname, VD, PT, Username, Password)
	return OS

def Check_Flap_Time(VD, T):
	today = date.today()
	if T == None:
		### Vendor don't support to show Flap time. List(Foundry / Ubiqouss)
		return False
	else:	
		if VD == 'juniper':
			if 'w' in T:
				W = re.findall("[0-9]{0,9}w",T)[0].split('w')[0]
			else:
				W = 0
			if 'd' in T:
				D = re.findall("[0-6]d",T)[0].split('d')[0]
			else:
				D = 0
			HM = re.findall("[0-2][0-9]:[0-5][0-9]",T)[0]
			H = HM.split(':')[0]
			m = HM.split(':')[1]
			if W == 0 and D == 0:
				return True
			else:
				return False
		elif VD == 'brocade_fabric' or VD == 'dell':
			W = re.findall("[0-9]{0,9}w",T)[0].split('w')[0]
			D = re.findall("[0-6]d",T)[0].split('d')[0]
			H = re.findall("[0-9]{0,2}h",T)[0].split('h')[0]
			if W == 0 and D == 0:
				return True
			else:
				return False
		elif VD == 'arista':
			D = re.findall("[0-9]{0,9}\ days,",T)[0].split()[0]
			H = re.findall("[0-9]{0,2}\ hours,",T)[0].split()[0]
			if D == 0:
				return True
			else:
				return False
		elif VD == 'cisco':
			M = T.split()[0]
			D = T.split()[1]
			Y = T.split()[2].split(',')[0]
			H = T.split()[3].split(':')[0]
			m = T.split()[3].split(':')[1]
			if Y == today.year and M == today.strftime('%b') and D == today.day:
				return True
			else:
				return False 
		elif VD == 'huawei':
			Y = T.split()[0].split('-')[0]
			M = T.split()[0].split('-')[1]
			D = T.split()[0].split('-')[2]
			H = T.split()[1].split(':')[0]
			m = T.split()[1].split(':')[1]
			if Y == today.year and M == today.month and D == today.day:
				return True
			else:
				return False 
		elif VD == 'cisco-nx':
			W = re.findall("[0-9]{0,9}week",T)[0].split('week')[0]
			D = re.findall("[0-6]day",T)[0].split('day')[0]
			if W == 0 and D == 0:
				return True
			else:
				return False

def Check_Port_Error(In, Out, CRC):
	if In == '0' or In == None:
		if Out == '0' or Out == None:
			if CRC == '0':
				return False
			else:
				return True
		else:
			return True
	else:
		return True

def Status_Checker(Hostname, VD, PT, Username, Password):
	PS = Query_Interface_Information(Hostname, VD, PT, Username, Password)
	if PS['LS'] == 'Up' or PS['LS'] == 'up':
		Flap_Status = Check_Flap_Time(VD, PS['FT'])
		if Flap_Status:
			print(color.RED)
			print('##### Port was flapped. Please Escalate to Tier2 #####')
			print(color.RESET)
		else:
			print(color.GREEN)
			print('##### Port was not down. Ignore Alarm #####')	
			print(color.RESET)
	else:
		print(color.BLUE)
		print('##### Start to check port error #####')
		print(color.RESET)
		Error_Status = Check_Port_Error(PS['IE'], PS['OE'], PS['CRC'])
		if Error_Status:
			if 'BDR' in PS['DSC']:
				ASN = PS['DSC'].split(':')[4]
				CID = PS['DSC'].split(':')[-1]
				print(color.RED)
				print('##### Circuit down issue. Please contact to ISP #####')
				print('##### ASN: '+ASN+' / Circuit ID: '+CID+' #####')
				print(color.RESET)
			else:
				print(color.RED)
				print('##### Need to replace cable and Port connectivity #####')
				print(color.RESET)
		else:
			print(color.RED)
			print('##### Need to check detail. Please escalate to Tier2 #####')
			print(color.RESET)

def Query_Interface_Information(Hostname, VD, PT, Username, Password):
	print(color.BLUE)
	print('##### Interface issue Checker #####')
	print('##### Issue Device : '+Hostname+' #####')
	print('##### Issue Port number : '+PT+' #####')
	print(color.RESET)
	if VD == 'juniper':
		PS = JUNOS_Interface_Check(Hostname, VD, PT, Username, Password)
	elif VD == 'cisco':
		PS = CISCO_IOS_Interface_Check(Hostname, VD, PT, Username, Password)
	elif VD == 'cisco-nx':
		PS = CISCO_NXOS_Interface_Check(Hostname, VD, PT, Username, Password)
	elif VD == 'ubiquoss':
		PS = UBIQ_Interface_Check(Hostname, VD, PT, Username, Password)
	elif VD == 'foundry':
		PS = Foundry_Interface_Check(Hostname, VD, PT, Username, Password)
	elif VD == 'brocade_fabric':
		PS = Brocade_Interface_Check(Hostname, VD, PT, Username, Password)
	elif VD == 'dell':
		PS = Dell_Interface_Check(Hostname, VD, PT, Username, Password)
	elif VD == 'arista':
		PS = EOS_Interface_Check(Hostname, VD, PT, Username, Password)
	elif VD == 'huawei':
		PS = Huawei_Interface_Check(Hostname, VD, PT, Username, Password)
	return PS
