import os 
os.system("sudo ip link set wlan0 promisc on")
os.system("cd /usr/local/ISSS/ ; sudo python3 Evaluation_Engine.py & sudo python3 Isulator_Engine.py")
