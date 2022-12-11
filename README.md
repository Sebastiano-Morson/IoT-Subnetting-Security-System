# IoT-Subnetting-Security-System

## Descrizione dello strumento
ISSS è uno strumento di protezione dagli attacchi informatici dedicato ai dispositivi IoT. 
Lo strumento sfrutta un modello di machine learning per analizzare i flussi di rete generati. Individuato un flusso malevolo vengono individuati gli attori coinvolti nella comunicazione e aggiunta una regola di firewalling per tali dispositivi così da isolarli dalla rete.


## Architetture compatibili
Lo strumento è configurabile sulle schede Raspberry Pi 3b+ e 4.

## Dipendenze necessarie
Le librerie e i programmi di cui necessita lo strumento sono presenti all'interno dei file requirements.txt e pip_requirements.txt e vengono automaticamente installati avviando lo script Initializer_Component.sh.
Lo strumento necessita inoltre Python versione >3.9.2 che non viene automaticamente installato durante l'esecuzione dell'Initializer Component.

## Installazione
Per installare lo strumento è necessario:
1. Scaricare la cartella tramite il comando

```
  sudo git clone https://github.com/Sebastiano-Morson/IoT-Subnetting-Security-System.git
```

2. Accedere alla cartella ISSS
3. Eseguire il comando per installare il tool

```
sudo ./Initializer_Component.sh
```

La fase di installazione può durare diversi minuti duranti i quali saranno chieste alcune informazioni come SSID name, password e ip associati alla sottorete. Prevede inoltre l'installazione di tutte le dipendenze necessarie al corretto funzionamento dello strumento e listate all'interno dei file pip_requirements.txt e requirements.txt .
Una volta installato, lo strumento eseguirà il reboot. Se tutto è proseguito correttamente sarà visibile il nuovo AP con ssid stabilito durante la fase di installazione. Sarà inoltre presente un nuovo servizio che verrà automaticamente eseguito ad ogni boot del dispositivo.

Di default durante l'installazione i file sono copiati nella cartella /usr/local/. È possibile modificare la cartella di installazione accedendo al file Initializer_Component.sh e modificando la stringa 
```
cp -r ../ISSS/ /usr/local/ISSS/ 
```


## Configurazione

### Configurazione di rete
Per modificare il nome dell'SSID e la password della rete è sufficiente accedere al file di configurazione /etc/hostapd/hostapd.conf e modificare le righe 3 e 10.

### Configurazione dei parametri di cattura
L'Evaluation_Engine utilizza la libreria NFStream per catturare i pacchetti circolanti sulla rete. Per modificare i parametri di cattura è quindi necessario fare riferimento alla documentazione del tool NFStream.

### Configurazione del modello di machine learning 
Per modificare l'algoritmo di machine learning utilizzato è necessario ricercare all'interno dello script Evaluation_Engine.py la stringa 
```
model = joblib.load("./random_forest.joblib")
```
sostituendo il percorso "./random_forest.joblib" con il path in cui è presente il nuovo modello.

## Ban_Notifier_Engine
Il Ban_Notifier_Engine rappresenta l'interfaccia tra utente e l'ISSS ed è richiamabile attraverso il comando
```
Ban_Notifier_Engine.py [-h] [-l] [-s] [-a] [--show-granted-devices] [-d ALLERTS_DELAY] [-m MAX_ALLERTS] [-o]
                              [--lock-device LOCK_DEVICE | --unlock-device UNLOCK_DEVICE | --grant-device GRANT_DEVICE | --remove-grant REMOVE_GRANT]
```

Attraverso il Ban_Notifier_Engine è possibile visualizzare lo stato corrente dell'Evaluation_Engine e dell'Isulator_Engine.

Lo script Ban_Notifier_Engine.py mette a disposizione diverse opzioni per controllare e modificare il funzionamento dello strumento.
| Option | Description |
| :---: | :---: |
| -l, --list | mostra la lista dei dispositivi posti in isolamento |
| -s, --show-logs | mostra la lista delle operazioni di locking e unlocking |
| -a, --show-allerts | mostra la lista dei dispositivi che sono stati rilevati sospetti dall'Evaluation Engine |
| --show-granted-devices | mostra la lista dei dispositivi autorizzati e che non verranno sottoposti a misure di isolamento |
| -d ALLERTS_DELAY, --allerts-delay ALLERTS_DELAY | permette di modificare l'intervallo di tempo in cui due o più valutazioni negative sono ritenute legate tra loro |
| -m MAX_ALLERTS, --max-allerts MAX_ALLERTS | permette di modificare il numero di allerts necessari a bannare la connessione |
| -o, --show-options | mostra le attuali impostazioni utilizzate dall'Evaluation Engine |
| --lock-device LOCK_DEVICE | permette di bloccare un dispositivo |
| --unlock-device UNLOCK_DEVICE | permette di sbloccare un dispositivo |
| --grant-device GRANT_DEVICE | permette di autorizzare un dispositivo |
| --remove-grant REMOVE_GRANT | permette di rimuovere l'autorizzazione a un dispositivo |


## Descrizione delle opzioni
## Note
Se si vuole verificare che lo strumento funzioni correttamente è possibile testare singolarmente i diversi moduli.

Innanzitutto è bene fermare il servizio ISSS_RunTimeComponent.service.
```
sudo systemctl stop ISSS_RunTimeComponent.service
```
Dopodichè è necessario aprire 3 shell e per ciascuna spostarsi nella cartella di installazione (di default /usr/local/ISSS/ ).

Nella prima shell eseguire il file Evaluation_Engine.py.

Nella seconda shell eseguire il file Isulator_Engine.py

Nella terza shell eseguire il file Ban_Notifier_Engine.py con passando gli argomenti desiderati.

Se lo strumento funziona correttamente si dovrebbe ottenere una situazione come quella mostrata nella gif.
![](https://github.com/Sebastiano-Morson/IoT-Subnetting-Security-System/blob/main/readme_folder/ezgif.com-gif-maker.gif)
