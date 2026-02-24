# Financial_Non_Linear_Probability
Analisi di ETF e Obbligazioni con Python

# Panoramica del Progetto

Questo progetto esplora l'aspetto non lineare della probabilità nei mercati finanziari, con un focus specifico sull'analisi di Exchange Traded Funds (ETF) e obbligazioni. Utilizzando Python, il progetto dimostra come i rendimenti degli asset finanziari si discostino spesso dalle assunzioni di normalità, presentando caratteristiche come code grasse (fat tails) e asimmetria. L'obiettivo è fornire una comprensione intuitiva di questi fenomeni e un'applicazione pratica per la loro analisi.

# Risultati Chiave

Il progetto utilizza dati storici dell'ETF SPY (rappresentante il mercato azionario) e del rendimento del Treasury a 10 anni (DGS10, come proxy per il mercato obbligazionario). L'analisi si concentra sui rendimenti logaritmici per SPY e sulle variazioni giornaliere per DGS10.

Risultati dell'Analisi Statistica:

| Strumento | Media Rendimenti | Deviazione Standard | Skewness | Curtosi | P-value Jarque-Bera | Conclusione Normalità |
| --- | --- | --- | --- | --- | --- | --- |
| **SPY**   | 0.000501  | 0.011232 | -0.5833 | 14.5691 | 0.000000e+00 | NON Normale |
| **DGS10** | 0.000757  | 0.053147 | -0.0519 | 1.9925 | 7.000172e-95 | NON Normale |




I risultati evidenziano che entrambi gli strumenti finanziari mostrano una curtosi significativamente maggiore di 3 (il valore per una distribuzione normale), indicando la presenza di code grasse. Questo significa che eventi estremi sono più probabili di quanto una distribuzione normale prevederebbe. L'ETF SPY mostra anche una skewness negativa, suggerendo una maggiore probabilità di perdite significative rispetto a guadagni equivalenti. Il test di Jarque-Bera ha confermato statisticamente che nessuno dei due set di rendimenti segue una distribuzione normale.

Questi risultati sottolineano l'importanza di considerare la probabilità non lineare nell'analisi finanziaria per una modellazione più realistica del rischio e del comportamento del mercato.

# Come Utilizzare il Progetto

1. Clona il Repository: git clone https://github.com/tuo_username/Financial-Non-Linear-Probability.git

2. Installa le Dipendenze: Assicurati di avere Python 3 installato e installa le librerie necessarie:

      pip install yfinance pandas-datareader pandas numpy scipy statsmodels matplotlib seaborn

3. Esegui lo Script: Naviga nella directory del progetto ed esegui lo script Python:

      python nonlinear_finance_project.py



Lo script scaricherà i dati, eseguirà l'analisi e genererà i grafici di distribuzione nella stessa directory.



