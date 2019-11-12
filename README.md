Tracking network event and give a guide for next action

[Purpose]
 - This script help NOC operator can check network event without network acknowledge
 - Script check current status and show how to do
    - Case1) : False alarm. Real event was not occurred
    - Case2) : Escalate event to Tier2 engineer. NOC cannot handle event directly.
    - Case3) : Take Tier1 operation to fix simple issue. (Cable replacement, contact to DC/ISP,...so on)
 - Engineer can collect related information with one execution command. Don't need to login device by their hands.
 (BGP/OSPF session status, Port IO error/CRC/IO rate/optical power, CPU usage,....so on)

[Function]
 - Support option by this version V1.2
    - Port Flap
    - BGP
    - OSPF
    - CPU usage
    - Ping unreachable
    
[Manual]
 - how to run script and input option 
 
    Network_Alarm_Checker.py [host] [Event Type] [Event value]
    
        [host]                      # Switch/Router IP or hostname
        
        [Event Type]                # Event Type to check
            Port            : Check Port flap event
            Ping            : Ping is unreachable
            CPU             : CPU usage event
            BGP             : BGP session up/down event
            OSPF            : OSPF session up/down event
            
        [Event value]               # Some event type need more information
            Port number     : Port Event require this value
            BGP neighbor    : BGP neighbor IP - BGP Event require this value
            OSPF neighbor   : OSPF neighbor IP - OSPF Event require this value
            
[Requirement]
 - Python Version higher than 3.0
 - Running_Script Repository
 
[Supported Vendor]
 - Juniper EX/QFX/MX series with JUNOS
 - Cisco Catalyst series with IOS
 - Cisco Nexus series with NXOS
 - Arista with EOS
 - Ubiquoss
 - Huawei
 - Foundry & Broucade
 - Dell
