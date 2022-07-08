# Github Analyzer
Con questo progetto si vuole cercare l'esistenza di una correlazione tra la popolarità di un progetto su Github e la documentazione fornita agli utenti,
così da avere degli indicatori sulla quantità di documentazione da fornire. 

Poiché questo tipo di domande sono frequenti e non esistono tools 
generici per fare questo tipo di analisi, allora nasce l'idea di realizzare un software che permetta di svolgere delle analisi e 
calcolare statistiche sulle informazioni fornite dalle
repository Github, in questa prima versione introducendo 
l'analisi Cloc e varie metriche per la popolarità e modificabilità, nonché la possibilità di generare dei relativi grafici. 

L'obiettivo è realizzare un software che fornisca la possibilità 
di estrarre dati facilmente e poi poter effettuare le proprie analisi su di essi, 
quindi viene posta molta importanza nella modificabilità e 
modularità in modo da poter introdurre facilmente nuove funzionalità d'analisi nelle release successive del software.

# Installazione
Per quanto riguarda l'installazione è possibile procedere in due modi:

Il primo modo consiste nello scaricare manualemnte le repository e creare un ambiente virtuale con le seguenti librerie:

PyGithub;	

Requests;

OS;

PyGount;

Tempfile;

PySimpleGUI;

Matplotlib;


Questo primo metodo risulta essere molto macchinoso, per questo motivo è stato implementato anche un secondo metodo.
Per il secondo metodo si è fatto uso del concetto di pip. Grazie all'uso di questa funzionalità si rende l'intallazione più semplice per l'utente

Con la prima istruzione si crea l'ambiente virtuale con tutte le dipendenze installate sul proprio personal computer

```js
pip install -i https://test.pypi.org/simple/github-analyzer
```
Infine l'istruzione seguente avvia effettivamente il programma

```js
Python -m GitHub_analyzer
