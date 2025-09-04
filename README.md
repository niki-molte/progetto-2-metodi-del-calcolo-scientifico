# Progetto Metodi del Calcolo Scientifico — progetto 2

Questo progetto implementa un algoritmo di compressione di immagini in formato ```.bmp``` che sfrutta DCT e IDCT basate sulla trasformata di Fourier.

## Documentazione

Una descrizione dettagliata del progetto è visualizzabile all'interno della documentazione nella directory ```/relazione/```.


## Autori

- **Federica Ratti** — 886158
- **Nicolò Molteni** — 933190

Corso di Laurea Magistrale in Informatica  
Università degli Studi di Milano-Bicocca  
A.A. 2024-2025

---

## Setup del progetto

### 1. Clona la repository

Dopo aver creato una directory spostarsi al suo interno per clonare la repository.

```bash
cd existing_repo
git clone https://github.com/niki-molte/progetto-2-metodi-del-calcolo-scientifico
```

### 2. Setup del virtual environmnet

Aprire la directory del progetto nel terminale ed eseguire:

```bash
    python3 -m venv venv
    source venv/bin/activate       # Linux/macOS
    venv\Scripts\activate.bat      # Windows
```

### 3. Installa le dependencies

Dopo aver attivato il virtual environment è possibile installare le dependencies.

```bash
    pip install --upgrade pip
    pip install -r requirements.txt
```  

# Run

Aprire un terminale nella stessa schermata della directory in cui è stata clonata la repository ed eseguire

```bash
    python3 main.py
```  

In questo modo verrà mostrata un'interfaccia grafica che permetterà di definire i parametri di compressione e selezionare l'immagine in formato ```.bmp``` da comprimere. Al termine dell'algoritmo verranno mostrati i risultati ottenuti.
---
