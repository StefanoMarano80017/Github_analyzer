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

Per installare tutte le dipendenze:
```js
pip install -r requirements
```

Eseguire il file __main__.py per avviare il programma. 
