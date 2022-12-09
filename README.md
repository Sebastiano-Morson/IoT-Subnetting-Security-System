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
3. seguire il comando 

```
sudo ./Initializer_Component.sh
```

La fase di installazione può durare diversi minuti duranti i quali saranno chieste alcune informazioni come SSID name, password e ip associati alla sottorete. Prevede inoltre l'installazione di tutte le dipendenze necessarie al corretto funzionamento dello strumento e listate all'interno dei file pip_requirements.txt e requirements.txt .
Una volta installato, lo strumento eseguirà il reboot. Se tutto è proseguito correttamente sarà visibile il nuovo AP con ssid stabilito durante la fase di installazione. Sarà inoltre presente un nuovo servizio che verrà automaticamente eseguito ad ogni boot del dispositivo.

## Configurazione
Per modificare la configurazione dello strumento è possibile sfruttare lo strumento .
Per modificare il nome dell'SSID e la password della rete è sufficiente accedere al file di configurazione /etc/hostapd/hostapd.conf e modificare le righe 3 e 10.

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
| -l, --list | |
| -s, --show-logs | |
| -a, --show-allerts ||
| --show-granted-devices ||
| -d ALLERTS_DELAY, --allerts-delay ALLERTS_DELAY ||
| -m MAX_ALLERTS, --max-allerts MAX_ALLERTS ||
| -o, --show-options ||
| --lock-device LOCK_DEVICE ||
| --unlock-device UNLOCK_DEVICE ||
| --grant-device GRANT_DEVICE ||
| --remove-grant REMOVE_GRANT ||

## Descrizione delle opzioni

![](https://github.com/Sebastiano-Morson/IoT-Subnetting-Security-System/blob/main/readme_folder/ezgif.com-gif-maker.gif)
