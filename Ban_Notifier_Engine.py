#!/usr/bin/python3

import time
import signal, os   

import sqlite3
from datetime import datetime
import csv
import argparse
from tabulate import tabulate
# Connect to your database (or create it if it was not there)
db = sqlite3.connect('/usr/local/ISSS/ISSS_DB.db')
cur = db.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS granted_devices (mac)")
cur.execute("CREATE TABLE IF NOT EXISTS settings (option, value)")

parser = argparse.ArgumentParser(description="Ban Notifier Engine Interface",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-l", "--list",           action="store_true",    help="list locked devices")
parser.add_argument("-s", "--show-logs",      action="store_true",    help="show history of locking and unlocking")
parser.add_argument("-a", "--show-allerts",   action="store_true",    help="mostra gli allert registrati dall'Evaluation_Engine ")
parser.add_argument("--show-granted-devices", action="store_true",    help="mostra la lista dei dispositivi autorizzati")
parser.add_argument("-d", "--allerts-delay",  type=int,               help="imposta l'intervallo di tempo tra due o più allerts prima del ban")
parser.add_argument("-m", "--max-allerts",     type=int,               help="imposta il numero massimo di allerts prima del ban") 
parser.add_argument("-o", "--show-options",   action="store_true",    help="mostra le impostazioni dell'Evaluation_Engine attualmente in uso")
group = parser.add_mutually_exclusive_group()
group.add_argument("--lock-device",           type=str,               help="lock a device")
group.add_argument("--unlock-device",         type=str,               help="unlock a device")
group.add_argument("--grant-device",          type=str,               help="autorizza il dispositivo")
group.add_argument("--remove-grant",          type=str,               help="rimuovi l'autorizzazione")

args = parser.parse_args()
config = vars(args)

if args.unlock_device:  ##UNLOCK DEVICE
    dt = datetime.now()
    fields = ['action', 'mac', 'author', 'time']

    with open('/usr/local/ISSS/lock-unlock-list.csv', mode='a+') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        #aggiungo le info sul flusso malevolo in modo che venga bloccato dall'isulator engine
        flow_info = {
            'action':'UNLOCK',
            'mac':args.unlock_device,
            'author':'USER',
            'time': str(dt)
        }

        writer.writerow(flow_info)
        csv.DictWriter(csv_file, fieldnames=fields)

        # close the file
        csv_file.close()

elif args.lock_device:  ###LOCK DEVICE
    dt = datetime.now()
    fields = ['action', 'mac', 'author', 'time']

    with open('/usr/local/ISSS/lock-unlock-list.csv', mode='a+') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        #aggiungo le info sul flusso malevolo in modo che venga bloccato dall'isulator engine
        flow_info = {
            'action':'LOCK',
            'mac':args.lock_device,
            'author':'USER',
            'time': str(dt)
        }

        writer.writerow(flow_info)
        csv.DictWriter(csv_file, fieldnames=fields)

        # close the file
        csv_file.close()
elif args.grant_device:
    #richiedo all'isulator_engine di sbloccare il dispositivo
    dt = datetime.now()
    fields = ['action', 'mac', 'author', 'time']

    with open('/usr/local/ISSS/lock-unlock-list.csv', mode='a+') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        #aggiungo le info sul flusso malevolo in modo che venga bloccato dall'isulator engine
        flow_info = {
            'action':'UNLOCK',
            'mac':args.grant_device,
            'author':'USER',
            'time': str(dt)
        }

        writer.writerow(flow_info)
        csv.DictWriter(csv_file, fieldnames=fields)

        # close the file
        csv_file.close()

    #inserisco il dispositivo nella lista dei dispositivi autorizzati
    ins_com = "INSERT INTO granted_devices VALUES ('"+args.grant_device+"')"
    cur.execute(ins_com)
    db.commit()

elif args.remove_grant:
    #controllo se il mac address è presente nella lista dei dispositivi autorizzati
    sel_com = "SELECT count(*) FROM granted_devices WHERE mac='"+(args.remove_grant)+"'"
    result = cur.execute(sel_com).fetchall()
    if (result[0][0] != 0): #se è un dispositivo autorizzato allora rimuovo la sua autorizzazione
        rem_com = "DELETE FROM granted_devices WHERE mac='"+args.remove_grant+"'"
        cur.execute(rem_com)
        db.commit()


elif args.list: ##mostra la lista dei dispositivi bloccati
    result = cur.execute("SELECT * FROM locked_devices")
    print("::::::::::::::::: LOCKED DEVICES LIST ::::::::::::::::::")
    
    print(tabulate(result, headers=['TIME', 'MAC ADDRESS', 'AUTHOR'], tablefmt="rst"))
    print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::")

elif args.show_logs:
    os.system("less /usr/local/ISSS/lock-unlock-list.csv")

elif args.show_granted_devices:
    sel_com = "SELECT * FROM granted_devices"
    result = cur.execute(sel_com)
    print("GRANTED DEVICES LIST")
    print(tabulate(result, headers=['MAC'], tablefmt="rst"))
    print("::::::::::::::::::::")

    
elif args.show_allerts:
    sel_com = "SELECT * FROM allerts_table"
    result = cur.execute(sel_com)
    print("::::::::::::::::::::::::::::::: ALLERTS ::::::::::::::::::::::::::::::::")
    print(tabulate(result, headers=['TIME', 'IP ADDRESS', 'MAC ADDRESS', 'COUNTER'], tablefmt="rst"))
    print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")


elif args.allerts_delay:
    update_com = "UPDATE settings SET value="+str(args.allerts_delay)+" WHERE option='delay'" 
    cur.execute(update_com)
    db.commit()
    print("                ++++ delay succesfully update ++++")

elif args.max_allerts:
    update_com = "UPDATE settings SET value="+str(args.max_allerts)+" WHERE option='max_allerts'" 
    cur.execute(update_com)
    db.commit()
    print("                ++++ max allerts succesfully updated ++++")

elif args.show_options:
    sel_com = "SELECT * FROM settings"
    result = cur.execute(sel_com)
    print("::::: SETTINGS :::::")
    print(tabulate(result, headers=["NAME", "VALUE"], tablefmt="rst"))
    print("::::::::::::::::::::")

else:
   print("Error: Unknown option")

db.close()

