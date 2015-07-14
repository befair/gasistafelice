******** Installare gasista felice come developer (DA RIVEDERE)

1.	Creazione chiave SSH per stabilire una connessione sicura tra GitHub e il 
	proprio computer:
	
	nota: Per inserire la propria chiave SSH nel sito GitHUb è necessario 
	possedere un account nel suddetto sito.
	
	1.1	Controllare se già esiste una chiave SSH nel prorio computer:
		
		$ cd ~/.ssh
		
		quindi
		
		$ ls -a
		
		se la cartella non esiste, o se non contiene due file chiamati id_rsa e 
		id_rsa.pub, saltare al opunto 1.3, altrimenti continuare con il prossimo 
		punto.
	
	1.2	Backup e rimozione della chiave SSH esistente:
	
		$ mkdir key_backup (crea una sottocartella in ~/.ssh)
		$ cp id_rsa* key_backup (copia id_rsa e id_rsa.pub nella sottocartella)	 
		$ rm id_rsa* (rimuove i file copiati per premettere la creazione della 
					  nuova chiave)
					  
	1.3	Generazione chiave SSH:
	
		$ ssh-keygen -t rsa -C "indirizzo_email@dominio.com"
		
		verrà richiesto dove salvare la chiave, premere invio senza inserire 
		nulla per salvarla nella cartella predefinita(indicata nella richiesta).
		Quindi, scegliere una password e inserirla quando richiesto.
		
	1.4 Aggiungere la propria chiave SSH sul sito GitHub:
	
		1.4.1 Sul sito GitHub cliccare su “Account Settings” > “SSH Public Keys” > 
			  “Add another public key”
		1.4.2 Aprire il file id_rsa.pub creato precedentemente e copiarne il 
			  contenuto ESATTAMENTE COME E'SCRITTO NEL FILE nel campo "key" 
			  della pagina del sito.
		1.4.3 Premere il bottone "Add Key"
		1.4.4 Per testare il tutto, esguire da terminale
			
			  $ ssh -T git@github.com
			  
			  e rispondere "yes" alla richiesta di connessione al sito GitHub

2.	Clonare il repository in locale:
	
	(gasdev)$ git clone git@github.com:feroda/gasistafelice.git

3.	Richiedere l'autorizzazione alla scrittura nel repository (INCOMPLETO)		

