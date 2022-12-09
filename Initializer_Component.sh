#!/bin/bash

#per prima cosa copio il contenuto della cartella all'interno della directory /usr/local/
#mi servirà per poter creare il servizio per il Run-Time_Component
cp -r ../ISSS/ /usr/local/ISSS/ 

echo "alias BanNotifierEngine='/usr/local/ISSS/Ban_Notifier_Engine.py'" >>/home/pi/.bashrc


apt install -y hostapd

systemctl unmask hostapd
systemctl enable hostapd

apt install -y dnsmasq

DEBIAN_FRONTEND=noninteractive apt install -y netfilter-persistent iptables-persistent

echo "Select access point ip address (default 192.168.10.1): "
read ip

if [[ ! $ip ]]
then 
        ip="192.168.10.1"
fi

echo "Select netmask (default 255.255.255.0): "
read netmask
if [[ ! $netmask ]]
then 
        netmask="255.255.255.0"
fi

echo "Select ip range (default 20, min 3, max 254): "
read range
if [[ ! $range ]]
then 
        range="20"
fi

echo "interface wlan0" 				>> /etc/dhcpcd.conf
echo "	static ip_address=$ip/24" 	>> /etc/dhcpcd.conf
echo "	nohook wpa_supplicant" 			>> /etc/dhcpcd.conf

#abilito l'instradamento su
echo "# Enable IPv4 routing" >> /etc/sysctl.d/routed-ap.conf
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.d/routed-ap.conf

iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

netfilter-persistent save

mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig

echo "interface=wlan0 # Listening interface" 			>> /etc/dnsmasq.conf
echo "dhcp-range=192.168.10.2,192.168.10.$range,$netmask,24h" 	>> /etc/dnsmasq.conf
echo "                # Pool of IP addresses served via DHCP" 	>> /etc/dnsmasq.conf
echo "domain=wlan     # Local wireless DNS domain" 		>> /etc/dnsmasq.conf
echo "address=/gw.wlan/$ip"	 				>> /etc/dnsmasq.conf
echo "                # Alias for this router" 			>> /etc/dnsmasq.conf

rfkill unblock wlan

echo "Select country code (defalt GB): "
read cc
if [[ ! $cc ]]
then 
        cc="GB"
fi
echo "Select SSID name (default ISSS_SecuredAccessPoint): " 
read ssid
if [[ ! $ssd ]]
then 
        ssid="ISSS_SecuredAccessPoint"
fi
echo "Select AP password: " 
read passwd

echo ""						>/etc/hostapd/hostapd.conf #in questo modo sovrascrivo le impostazioni precedenti
echo "country_code=$cc" 			>>/etc/hostapd/hostapd.conf
echo "interface=wlan0" 				>>/etc/hostapd/hostapd.conf
echo "ssid=$ssid"	 			>>/etc/hostapd/hostapd.conf
echo "hw_mode=g" 				>>/etc/hostapd/hostapd.conf
echo "channel=7" 				>>/etc/hostapd/hostapd.conf
echo "macaddr_acl=0" 				>>/etc/hostapd/hostapd.conf
echo "auth_algs=1" 				>>/etc/hostapd/hostapd.conf
echo "ignore_broadcast_ssid=0" 			>>/etc/hostapd/hostapd.conf
echo "wpa=2" 					>>/etc/hostapd/hostapd.conf
echo "wpa_passphrase=$passwd"		 	>>/etc/hostapd/hostapd.conf
echo "wpa_key_mgmt=WPA-PSK" 			>>/etc/hostapd/hostapd.conf
echo "wpa_pairwise=TKIP" 			>>/etc/hostapd/hostapd.conf
echo "rsn_pairwise=CCMP" 			>>/etc/hostapd/hostapd.conf

#installo le librerie del tool NFStream

apt-get update
apt-get upgrade


echo "Starting installation of required dependencies"
while read p; do
        echo "installing $p ..."
        apt-get install -y $p
done <"./requirements.txt"

while read p; do
	echo "installing $p ..."
	pip3 install $p
done <"./pip_requirements.txt"

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

echo "Rebooting system ..."

systemctl reboot
