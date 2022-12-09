# IoT-Subnetting-Security-System

## Descrizione dello strumento
ISSS è uno strumento di protezione dagli attacchi informatici dedicato ai dispositivi IoT. 
Lo strumento sfrutta un modello di machine learning per analizzare i flussi di rete generati. Individuato un flusso malevolo vengono individuati gli attori coinvolti nella comunicazione e aggiunta una regola di firewalling per tali dispositivi così da isolarli dalla rete.

## Architetture compatibili
Lo strumento è configurabile sulle schede Raspberry Pi 3b+ e 4.

## Dipendenze necessarie
Lo strumento necessita la presenza di Python versioni >3.9.2.

## Installazione
Per poter installare lo strumento è sufficiente eseguire il comando sudo ./Initializer_Component.sh. La fase di installazione può durare diversi minuti e prevede l'installazione di tutte le dipendenze necessarie al corretto funzionamento dello strumento.
Una volta installato correttamente lo strumento verrà riavviato e ad ogni avvio successivo si renderà disponibile l'accesso all'access-point con nome ISSS_SecuredAccessPoint.
## Configurazione
Una volta installato lo strumento si può procedere alla modifica dei parametri imposti di default.
Per modificare il nome dell'SSID e la password della rete è sufficiente accedere al file di configurazione /etc/hostapd/hostapd.conf e modificare le righe 3 e 10.
## Opzioni disponibili

## Descrizione delle opzioni

![](https://github.com/Sebastiano-Morson/IoT-Subnetting-Security-System/blob/main/readme_folder/ezgif.com-gif-maker.gif)
