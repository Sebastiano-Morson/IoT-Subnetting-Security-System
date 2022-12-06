#leggo il contenuto del file csv 
#se compare una entry la leggo e determino:
#	se si tratta di un'operazione di blocco o di sblocco guardando il primo campo
#	l'indirizzo mac coinvolto dall'operazione, guardando il secondo campo
#se la richiesta è di sblocco allora eseguo lo sblocco
#se la richiesta è di blocco allora eseguo il blocco

import csv
import time
import signal, os   

import sqlite3
from datetime import datetime
import csv

#creo il file su cui ascolterò i dati
file = open('/usr/local/ISSS/lock-unlock-list.csv','a+')
file.close()

# Connect to your database (or create it if it was not there)
db = sqlite3.connect('/usr/local/ISSS/ISSS_DB.db')
cur = db.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS locked_devices (timestamp, mac, author)")
cur.execute("CREATE TABLE IF NOT EXISTS granted_devices (mac)")


with open('/usr/local/ISSS/lock-unlock-list.csv') as csv_file:
    while True:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            
            #se una riga viene inserita all'interno del file:
            print('\tAction:',row[0],' -- MAC: ',row[1],', -- Author:',row[2],' -- Time: ',row[3],')')
            #verifico l'azione che si intende intraprendere. Può essere solo "LOCK" o "UNLOCK"
            if (row[0] == 'LOCK'):
                
                #controllo se il mac address è presente nella lista dei dispositivi autorizzati
                sel_com = "select count(*) FROM granted_devices WHERE mac='"+row[1]+"'"
                result = cur.execute(sel_com).fetchall()
                
                if (result[0][0] == 0): #se non è un dispositivo autorizzato allora procedo con l'isolamento

                    #controllo se il dispositivo era già isolato
                    sel_com = "select count(*) FROM locked_devices WHERE mac='"+row[1]+"'"
                    result = cur.execute(sel_com).fetchall()
                    #se non è già isolato lo isolo e aggiungo la entry nella tabella
                    if (result[0][0] == 0):
                        rule = "sudo iptables -A INPUT -m mac --mac-source "+row[1]+" -j DROP"
                        os.system(rule)
                        ins_com = "insert into locked_devices values ('"+row[3]+"','"+row[1]+"','"+row[2]+"')"
                        #print(ins_com)
                        cur.execute(ins_com)
                        db.commit()

            else: #è un'operazione di UNLOCK
                #controllo se il dispositivo era isolato
                sel_com = "select count(*) FROM locked_devices WHERE mac='"+row[1]+"'"
                result = cur.execute(sel_com).fetchall()
                if (result[0][0] != None):

                    #tolgo dall'isolamento il dispositivo 
                    rule = "sudo iptables -D INPUT -m mac --mac-source "+row[1]+" -j DROP"
                    os.system(rule)
                    #rimuovo la entry
                    del_com = "DELETE FROM locked_devices WHERE mac='"+row[1]+"'"
                    #print(del_com)
                    cur.execute(del_com)
                    db.commit()
    
db.close()
            
        

