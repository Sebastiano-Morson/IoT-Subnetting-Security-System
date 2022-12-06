#!/bin/bash

#per prima cosa copio il contenuto della cartella all'interno della directory /usr/local/
#mi servirà per poter creare il servizio per il Run-Time_Component
cp -r ../ISSS/ /usr/local/ISSS/ 

export PATH="/usr/local/ISSS/:$PATH"

apt install -y hostapd

systemctl unmask hostapd
systemctl enable hostapd

apt install -y dnsmasq

DEBIAN_FRONTEND=noninteractive apt install -y netfilter-persistent iptables-persistent

echo "interface wlan0" 				>> /etc/dhcpcd.conf
echo "	static ip_address=192.168.10.1/24" 	>> /etc/dhcpcd.conf
echo "	nohook wpa_supplicant" 			>> /etc/dhcpcd.conf

#abilito l'instradamento su
echo "# Enable IPv4 routing" >> /etc/sysctl.d/routed-ap.conf
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.d/routed-ap.conf

iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

netfilter-persistent save

mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig

echo "interface=wlan0 # Listening interface" 			>> /etc/dnsmasq.conf
echo "dhcp-range=192.168.10.2,192.168.10.20,255.255.255.0,24h" 	>> /etc/dnsmasq.conf
echo "                # Pool of IP addresses served via DHCP" 	>> /etc/dnsmasq.conf
echo "domain=wlan     # Local wireless DNS domain" 		>> /etc/dnsmasq.conf
echo "address=/gw.wlan/192.168.10.1" 				>> /etc/dnsmasq.conf
echo "                # Alias for this router" 			>> /etc/dnsmasq.conf

rfkill unblock wlan

echo ""						>/etc/hostapd/hostapd.conf #in questo modo sovrascrivo le impostazioni precedenti
echo "country_code=IT" 				>>/etc/hostapd/hostapd.conf
echo "interface=wlan0" 				>>/etc/hostapd/hostapd.conf
echo "ssid=NameOfNetwork" 			>>/etc/hostapd/hostapd.conf
echo "hw_mode=g" 				>>/etc/hostapd/hostapd.conf
echo "channel=7" 				>>/etc/hostapd/hostapd.conf
echo "macaddr_acl=0" 				>>/etc/hostapd/hostapd.conf
echo "auth_algs=1" 				>>/etc/hostapd/hostapd.conf
echo "ignore_broadcast_ssid=0" 			>>/etc/hostapd/hostapd.conf
echo "wpa=2" 					>>/etc/hostapd/hostapd.conf
echo "wpa_passphrase=123stella" 	>>/etc/hostapd/hostapd.conf
echo "wpa_key_mgmt=WPA-PSK" 			>>/etc/hostapd/hostapd.conf
echo "wpa_pairwise=TKIP" 			>>/etc/hostapd/hostapd.conf
echo "rsn_pairwise=CCMP" 			>>/etc/hostapd/hostapd.conf

#installo le librerie del tool NFStream
apt-get update
apt-get upgrade
apt-get install -y git 
apt-get install -y python3-dev autoconf automake libtool pkg-config flex bison gettext libjson-c-dev
apt-get install -y libusb-1.0-0-dev libdbus-glib-1-dev libbluetooth-dev libnl-genl-3-dev
pip3 install opencv-python 
apt-get install -y libcblas-dev
apt-get install -y libhdf5-dev
apt-get install -y libhdf5-serial-dev
apt-get install -y libatlas-base-dev
apt-get install -y libjasper-dev 
apt-get install -y libqtgui4 
apt-get install -y sqlite3
apt-get install -y python3-scipy python3-sklearn 
pip3 install NFStream
pip3 install scikit-learn==1.0.2
pip3 install joblib==1.2.0
pip install termcolor
pip install tabulate
#configuro il Run-Time_Component come demone di sistema da avviare al boot
touch /lib/systemd/system/ISSS_RunTimeComponent.service
echo "[Unit]"								>>/lib/systemd/system/ISSS_RunTimeComponent.service
echo "Description=ISSS RunTime_Component Service" 			>>/lib/systemd/system/ISSS_RunTimeComponent.service
echo "After=multi-user.target"						>>/lib/systemd/system/ISSS_RunTimeComponent.service
echo ""									>>/lib/systemd/system/ISSS_RunTimeComponent.service
echo "[Service]"							>>/lib/systemd/system/ISSS_RunTimeComponent.service
echo "Type=idle"							>>/lib/systemd/system/ISSS_RunTimeComponent.service
echo "ExecStart=/usr/bin/python3 /usr/local/ISSS/RunTime_Component.py"	>>/lib/systemd/system/ISSS_RunTimeComponent.service
echo ""									>>/lib/systemd/system/ISSS_RunTimeComponent.service
echo "[Install]"							>>/lib/systemd/system/ISSS_RunTimeComponent.service
echo "WantedBy=multi-user.target"					>>/lib/systemd/system/ISSS_RunTimeComponent.service
chmod 644 /lib/systemd/system/ISSS_RunTimeComponent.service

systemctl daemon-reload
systemctl enable ISSS_RunTimeComponent.service



systemctl reboot
