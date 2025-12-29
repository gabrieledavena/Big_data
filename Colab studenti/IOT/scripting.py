import pandas as pd
import glob
import os


def unisci_e_ordina_csv(cartella='files', modello_file='*.xlsx', colonna_timestamp='Timestamp',
                        nome_output='report_unito_ordinato.csv'):
    """
    Trova tutti i file CSV in una cartella, li unisce e li ordina
    in base alla colonna specificata.

    Args:
        cartella (str): Il percorso della cartella contenente i file (predefinito: la cartella corrente).
        modello_file (str): Il pattern per trovare i file (es. '*.csv').
        colonna_timestamp (str): Il nome della colonna da usare per l'ordinamento.
        nome_output (str): Il nome del file CSV di output.
    """

    # 1. Trova tutti i file che corrispondono al modello
    percorso_completo = os.path.join(cartella, modello_file)
    tutti_i_file = glob.glob(percorso_completo)

    # Lista per contenere i DataFrame di ciascun file
    lista_df = []

    print(f"Trovati {len(tutti_i_file)} file da unire.")

    # 2. Leggi e unisci i file
    for filename in tutti_i_file:
        try:
            # Leggi il file CSV
            df = pd.read_excel(filename)
            lista_df.append(df)
            print(f" - Caricato: {filename}")
        except Exception as e:
            print(f"ATTENZIONE: Errore nella lettura del file {filename}: {e}")
            continue

    if not lista_df:
        print("Nessun file letto con successo. Uscita.")
        return

    # Concatena tutti i DataFrame in un unico DataFrame
    df_unito = pd.concat(lista_df, ignore_index=True)

    print(f"\nTotale righe dopo l'unione: {len(df_unito)}")

    # 3. Conversione e Ordinamento per Timestamp

    # Converti la colonna Timestamp nel formato datetime.
    # Questo è fondamentale per garantire un ordinamento cronologico corretto.
    if colonna_timestamp in df_unito.columns:
        print(f"Conversione della colonna '{colonna_timestamp}' in formato data/ora...")
        df_unito[colonna_timestamp] = pd.to_datetime(df_unito[colonna_timestamp])

        # Ordina l'intero DataFrame in base al timestamp
        df_ordinato = df_unito.sort_values(by=colonna_timestamp, ascending=True)
        print("Ordinamento completato.")
    else:
        print(f"ATTENZIONE: La colonna '{colonna_timestamp}' non è stata trovata nei file. L'output NON sarà ordinato.")
        df_ordinato = df_unito

    # 4. Salvataggio del file di output
    df_ordinato.to_csv(nome_output, index=False)

    print(f"\n--- Processo Completato ---")
    print(f"Il file unito e ordinato è stato salvato come: **{nome_output}**")


# Esegui la funzione
# Assicurati che 'Timestamp' sia il nome esatto della colonna
unisci_e_ordina_csv()