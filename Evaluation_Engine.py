from nfstream import NFStreamer
from termcolor import colored
import pandas
import joblib
import sqlite3
from datetime import datetime
import csv

# Connect to your database (or create it if it was not there)
db = sqlite3.connect('ISSS_DB.db')
cur = db.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS allerts_table (timestamp, ip, mac,count)")
cur.execute("DROP TABLE IF EXISTS settings")
cur.execute("CREATE TABLE IF NOT EXISTS settings (option, value)")
cur.execute("INSERT INTO settings VALUES ('delay',10)") 
cur.execute("INSERT INTO settings VALUES ('max_allerts', 2)")

my_streamer = NFStreamer(
                         source="/home/pi/pcap_scenario/mirai.pcap", #or network interface
                         #source="wlan0",
                         #decode_tunnels=True,
                         #bpf_filter=None,
                         promiscuous_mode=True,
                         #snapshot_length=1536,
                         #idle_timeout=120,
                         #active_timeout=1800,
                         #accounting_mode=0,
                         #udps=True,
                         #n_dissections=0,
                         statistical_analysis=True
                         #splt_analysis=10,
                         #n_meters=0,
                         #max_nflows=10,
                         #performance_report=True,
                         #system_visibility_mode=0,
                         #system_visibility_poll_ms=100
)

      
# load the model
model = joblib.load("./random_forest.joblib")
print("")
print("::::::::::::::::::::::::::::::::::::::::::::::::::::::CATTURE::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
i=0
for flow in my_streamer:
    data = {
            'src_port' :flow.src_port,
            'dst_port' : flow.dst_port,
            'protocol' : flow.protocol,
            'ip_version' : flow.ip_version,
            'vlan_id' : flow.vlan_id,
            'tunnel_id' : flow.tunnel_id,
            'bidirectional_duration_ms': flow.bidirectional_duration_ms ,
            'bidirectional_packets': flow.bidirectional_packets,
            'bidirectional_bytes': flow.bidirectional_bytes, 
            'src2dst_packets': flow.src2dst_packets, 
            'src2dst_bytes': flow.src2dst_bytes,
            'dst2src_duration_ms': flow.dst2src_duration_ms, 
            'dst2src_packets': flow.dst2src_packets, 
            'dst2src_bytes': flow.dst2src_bytes,
            'bidirectional_min_ps': flow.bidirectional_min_ps, 
            'bidirectional_mean_ps': flow.bidirectional_mean_ps,
            'bidirectional_stddev_ps': flow.bidirectional_stddev_ps, 
            'src2dst_mean_ps': flow.src2dst_mean_ps, 
            'src2dst_stddev_ps': flow.src2dst_stddev_ps,
            'src2dst_max_ps': flow.src2dst_max_ps, 
            'dst2src_min_ps': flow.dst2src_min_ps, 
            'dst2src_mean_ps': flow.dst2src_mean_ps,
            'bidirectional_min_piat_ms' : flow.bidirectional_min_piat_ms, 
            'bidirectional_mean_piat_ms': flow.bidirectional_mean_piat_ms,
            'bidirectional_stddev_piat_ms': flow.bidirectional_stddev_piat_ms, 
            'bidirectional_max_piat_ms': flow.bidirectional_max_piat_ms,
            'src2dst_min_piat_ms': flow.src2dst_min_piat_ms, 
            'src2dst_mean_piat_ms': flow.src2dst_mean_piat_ms, 
            'src2dst_stddev_piat_ms': flow.src2dst_stddev_piat_ms,
            'dst2src_min_piat_ms': flow.dst2src_min_piat_ms, 
            'dst2src_mean_piat_ms': flow.dst2src_mean_piat_ms, 
            'dst2src_stddev_piat_ms': flow.dst2src_stddev_piat_ms,
            'dst2src_max_piat_ms': flow.dst2src_max_piat_ms, 
            'bidirectional_syn_packets': flow.bidirectional_syn_packets,
            'bidirectional_cwr_packets': flow.bidirectional_cwr_packets, 
            'bidirectional_ece_packets': flow.bidirectional_ece_packets,
            'bidirectional_urg_packets' : flow.bidirectional_urg_packets, 
            'bidirectional_ack_packets' : flow.bidirectional_ack_packets,
            'bidirectional_psh_packets' : flow.bidirectional_psh_packets , 
            'bidirectional_rst_packets' : flow.bidirectional_rst_packets ,
            'bidirectional_fin_packets' : flow.bidirectional_fin_packets , 
            'src2dst_syn_packets' : flow.src2dst_syn_packets ,
            'src2dst_ece_packets' : flow.src2dst_ece_packets , 
            'src2dst_psh_packets' : flow.src2dst_psh_packets , 
            'src2dst_rst_packets' : flow.src2dst_rst_packets ,
            'dst2src_syn_packets' : flow.dst2src_syn_packets , 
            'dst2src_cwr_packets' : flow.dst2src_cwr_packets , 
            'dst2src_ece_packets' : flow.dst2src_ece_packets ,
            'dst2src_urg_packets' : flow.dst2src_urg_packets , 
            'dst2src_psh_packets' : flow.dst2src_psh_packets , 
            'dst2src_rst_packets' : flow.dst2src_rst_packets ,
            'application_is_guessed' : flow.application_is_guessed , 
            'application_confidence' : flow.application_confidence
            }
    data = pandas.DataFrame(data, index=[0])
    value = data.values
    prediction = model.predict(value) 
    if prediction[0] == 1:
        # ricavo la data e il tempo
        dt = datetime.now()
        # ricavo il timestamp
        ts = datetime.timestamp(dt)

        #ricavo ip, mac di sorgente e destinatario del flusso
        src_ip = flow.src_ip
        dst_ip = flow.dst_ip 
        src_mac = flow.src_mac
        dst_mac = flow.dst_mac
        counter_limit = cur.execute("select value from settings where option='max_allerts'").fetchall() #numero massimo di segnalazioni prima del ban
        counter_limit = counter_limit[0][0]
        time_limit = cur.execute("select value from settings where option='delay'").fetchall() #numero di secondi prima che due segnalazioni vengano viste come casi isolati
        time_limit=time_limit[0][0]

        #EFFETTUO LE VERIFICHE PER IL DISPOSITIVO SORGENTE
        #verifico il timestamp e il counter associati al mac del dispositivo
        sel_com = "select timestamp,count, count(*) FROM allerts_table WHERE mac='"+src_mac+"'"
        result = cur.execute(sel_com).fetchall()

        i+=1
        print(colored("---------------------------------------------------------------------------------------------------------------------------------",'red'))
        print(colored(str(str(i)+" ×××××                                          MALICIOUS FLOW                                                          ×××××"), 'red'))
        print(colored(str("             src_ip: "+src_ip+" src_mac: "+ src_mac+" dst_ip: "+ dst_ip+" dst_mac: "+dst_mac+ "      " ), 'red'))
        #print("---------------------------------------------------------------------------------------------------------------------------------")
        #print(i," ×××××                                           MALICIOUS FLOW                                                         ×××××")
        #print("         src_ip:",src_ip," --  src_mac:", src_mac," --  dst_ip:", dst_ip," --  dst_mac:",dst_mac, "       " )

        #se non è presente nessuna entry associata a quell'indirizzo mac-ip aggiungo la nuova entry
        if (result[0][2] == 0):
            ins_com = "insert into allerts_table values ('"+str(dt)+"','"+src_ip+"','"+src_mac+"',"+str(1)+")"
            #print("sorgente: ",ins_com)
            cur.execute(ins_com)
            db.commit()
        
        #altrimenti, se è presente
        else:
            for row in result:
                last_change = datetime.timestamp(datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f"))
                count = row[1]
                if (ts - last_change < time_limit ): #aspetto 3 min tra una segnalazione e un'altra
                    if (count > counter_limit): #lascio solo 2 possibilità
                        fields = ['action', 'mac', 'author', 'time']
                        with open('./lock-unlock-list.csv', mode='a+') as csv_file:
                            writer = csv.DictWriter(csv_file, fieldnames=fields)
                            #aggiungo le info sul flusso malevolo in modo che venga bloccato dall'isulator engine
                            flow_info = {
                                'action':'LOCK',
                                'mac':src_mac,
                                'author':'EVALUATOR',
                                'time': str(dt)
                            }

                            writer.writerow(flow_info)
                            csv.DictWriter(csv_file, fieldnames=fields)

                            # close the file
                            csv_file.close()
                    else:
                        upd_com = "update allerts_table set count="+str(count+1)+", timestamp='"+str(dt)+"' where mac ='"+src_mac+"'"
                        cur.execute(upd_com)
                        db.commit()
                else:
                    upd_com = "update allerts_table set count="+str(1)+", timestamp='"+str(dt)+"' where mac ='"+src_mac+"'"
                    cur.execute(upd_com)
                    db.commit()

            
        #EFFETTUO LE VERIFICHE PER IL DISPOSITIVO DESTINATARIO
        #verifico il timestamp e il counter associati al mac del dispositivo
        sel_com = "select timestamp,count, count(*) FROM allerts_table WHERE mac='"+dst_mac+"'"
        result = cur.execute(sel_com).fetchall()

        #se non è presente nessuna entry associata a quell'indirizzo mac-ip aggiungo la nuova entry
        if (result[0][2] == 0):
            ins_com = "insert into allerts_table values ('"+str(dt)+"','"+dst_ip+"','"+dst_mac+"',"+str(1)+")"
            #print("destination: ",ins_com)
            cur.execute(ins_com)
            db.commit()
        
        #altrimenti, se è presente
        else:
            for row in result:
                if len(row)!=4:
                    continue
                last_change = datetime.timestamp(datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f"))
                count = row[1]
                if (ts - last_change < time_limit ): #aspetto 3 min tra una segnalazione e un'altra
                    if (count > counter_limit): #lascio solo 2 possibilità
                    

                        with open('./lock-unlock-list.csv', mode='a+') as csv_file:
                            fields = ['action', 'mac', 'author', 'time']
                        
                            writer = csv.DictWriter(csv_file, fieldnames=fields)
                            #aggiungo le info sul flusso malevolo in modo che venga bloccato dall'isulator engine
                            flow_info = {
                                'action':'LOCK',
                                'mac':dst_mac,
                                'author':'EVALUATOR',
                                'time': str(dt)
                            }

                            writer.writerow(flow_info)
                            csv.DictWriter(csv_file, fieldnames=fields)

                            # close the file
                            csv_file.close()
                    else:
                        upd_com = "update allerts_table set count="+str(count+1)+", timestamp='"+str(dt)+"' where mac ='"+dst_mac+"'"
                        cur.execute(upd_com)
                        db.commit()
                else:
                    upd_com = "update allerts_table set count="+str(1)+", timestamp='"+str(dt)+"' where mac ='"+dst_mac+"'"
                    cur.execute(upd_com)
                    db.commit()

    else:
        i+=1
        print("---------------------------------------------------------------------------------------------------------------------------------")
        print(i," +++++                                            NORMAL FLOW                                                           +++++")
#safely close the db connection
db.close()
print("*******")


#valuto il flusso

#se il flusso è benigno riprendo da capo
#se il flusso è malevolo estrapolo gli indirizzi ip dei flussi e gli indirizzi mac
#verifico l'ultima modifica della tabella delle anomalie
#se 
#	l'ultima modifica per la entry con quell'indirizzo ip è maggiore di un tempo x 
#
#allora porto azzero il contatore e lo pongo a 1. Dopodichè ggiorno il timestamp
#
#altrimenti
#se 
#	l'utlima modifica per la entry con quell'indirizzo il è minore di un tempo x
#	il contatore è minore di un certo valore y 
#allora incremento il contatore e aggiorno il timestamp
#altrimenti
#cancello la entry per quell'ip
#ricavo l'indirizzo mac per quel dispositivo dalle
#
#scrivo le info sul flusso in formato csv su un file che verrà letto dall'isulator engine
#{'action':'LOCK', {'mac', '[MAC ADDRESS]', 'author':'EVALUATOR', 'timestamp':'[timestamp]'}

