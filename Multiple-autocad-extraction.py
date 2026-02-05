import os
import pandas as pd
import ezdxf

# 1. IMPOSTAZIONE CARTELLA
# Usa r"" prima della stringa per evitare errori con le barre rovesciate di Windows
cartella = r"C:\GitHub\Multiple-file-Autocad-data-extraction\prof"

# Dizionario contenitore per i dati
user_defined_dictionary = {}

# 2. DEFINIZIONE DELLA FUNZIONE DI ESTRAZIONE
def extract_attr_dxf(percorso_cartella, nome_file):
    try:
        full_path = os.path.join(percorso_cartella, nome_file)
        doc = ezdxf.readfile(full_path)
        modelspace = doc.modelspace()
        
        for n in modelspace:
            # Cerca solo gli oggetti di tipo INSERT (i blocchi)
            if n.dxftype() == "INSERT":
                # Controlla se il blocco ha l'attributo chiave "NUMEROARTICOLO"
                if n.has_attrib("NUMEROARTICOLO"):
                    articolo = {}
                    # Estrae tutti gli attributi del blocco
                    for attrib in n.attribs:
                        articolo[attrib.dxf.tag] = attrib.dxf.text
                    
                    # Aggiunge al dizionario generale usando il numero articolo come chiave
                    # NOTA: Se due file hanno lo stesso numero articolo, l'ultimo sovrascrive il primo
                    chiave = articolo["NUMEROARTICOLO"]
                    user_defined_dictionary[chiave] = articolo
                    print(f"Estratto articolo: {chiave} da {nome_file}")
                    
    except Exception as e:
        print(f"Errore nella lettura del file {nome_file}: {e}")

# 3. ESECUZIONE DEL CICLO
print("Inizio estrazione...")

# Scansiona la cartella
for nomefile in os.listdir(cartella):
    if nomefile.lower().endswith(".dxf"):
        extract_attr_dxf(cartella, nomefile)

# 4. SALVATAGGIO SU CSV (La parte che mancava)
print("Creazione del file CSV in corso...")

# Trasforma il dizionario in un DataFrame di Pandas
# orient='index' significa che le chiavi del dizionario diventano le righe
df = pd.DataFrame.from_dict(user_defined_dictionary, orient='index')

# Salva il file nella stessa cartella dei dxf
percorso_output = os.path.join(cartella, "risultato_estrazione.csv")

# Esporta in CSV (sep=';' è meglio per Excel in italiano, o usa ',' per standard inglese)
df.to_csv(percorso_output, sep=';', index=False)

print(f"Fatto! Il file è stato salvato qui: {percorso_output}")