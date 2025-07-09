# django-store

Elaborato backend `Full Website: e-commerce` per l'esame Progettazione e Produzione Multimediale.

Il deploy del sito si trova al link: [**https://django-store-production.up.railway.app/**](https://django-store-production.up.railway.app/)

## Funzionalità del sito

Per utenti registrati:
- Modifca del profilo
- Visione dei propri ordini
- Visione del proprio carrello
- Filtraggio contenuti in base alla categoria
- Aggiunta di prodotti al carrello
- Possibilità di effettuare un ordine (fittizio, non presenta modalità di pagamento per semplificare il lavoro)

Per utenti manager:
- Tutto quello elencato sopra
- Possibilità di modificare i prodotti in vendita sul sito
- Possibilità di modificare le categorie presenti sul sito
- Possibilità di contrassegnare gli ordini dei clienti come consegnati o cancellarli

Viene fornito un utente manager di base in modo da poter esplorare le funzioni del sito:
- username: `manager`  
- password: `manager`

Per semplicità, la possibilità di eleggere un utente a manager è stata nascosta dietro la console `admin` di django.