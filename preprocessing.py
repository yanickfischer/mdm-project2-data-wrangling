#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


# In[12]:


#Datenpfad und Verzeichnisse
DATA_DIR = "data"
RAW_DATA_FILE = os.path.join(DATA_DIR, "all_energy_statistics.csv")
OUTPUT_DIR = "output"

# Sicherstellen, dass das Output-Verzeichnis existiert
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 3. Rohdaten laden

try:
    df = pd.read_csv(RAW_DATA_FILE)
    print("Daten erfolgreich geladen. Vorschau:")
    print(df.head())
except FileNotFoundError:
    print(f"Fehler: Datei {RAW_DATA_FILE} nicht gefunden.")


# In[ ]:


# Überblick über die Struktur der Rohdaten

print(f"Anzahl Zeilen und Spalten: {df.shape}")
print("\nSpaltennamen:")
print(df.columns.tolist())

print("\nFehlende Werte pro Spalte:")
print(df.isnull().sum())

print("\nDatentypen:")
print(df.dtypes)


# In[13]:


# Zeilen mit vorhandenen (nicht NaN) Footnotes anzeigen
df_footnotes = df[df["quantity_footnotes"].notna()]

# Vorschau der ersten Zeilen mit Footnotes
print(df_footnotes.head())

# Übersicht: Wieviele Zeilen haben eine Footnote?
print(f"Anzahl Zeilen mit Footnotes: {df_footnotes.shape[0]}")


# ## Cleaning of commodity

# In[16]:


# Maximal 100 Zeilen in der Ausgabe anzeigen, damit wir viele Einträge auf einmal sehen können
pd.set_option('print.max_rows', 100)


# In[17]:


# Verteilung der Hauptkategorien (nur zur Information)
print(df.category.value_counts())


# In[18]:


# Übersicht über die seltensten commodity_transaction-Einträge
print(df.commodity_transaction.value_counts().tail(50))


# In[19]:


# Vorschau: Wie sehen die ersten commodity_transaction-Einträge aus?
print(df.commodity_transaction.head())


# In[20]:


# Anzahl Trennzeichen in den commodity_transaction-Strings zählen
print(df.commodity_transaction.str.count(" - | – ").value_counts())


# In[21]:


# Aufteilen in drei neue Spalten: commodity, transaction_type und additional_transaction_info
split_commodities = df.commodity_transaction.str.split(" - | – ", expand=True)

# Vorschau auf die neuen Spalten
print(split_commodities.head())


# In[22]:


# Übersicht: Inhalt der zweiten Spalte (transaction_type)
print(split_commodities[1].str.lower().value_counts())

# Übersicht: Inhalt der dritten Spalte (additional_transaction_info)
print(split_commodities[2].str.lower().value_counts())

# Übersicht: Inhalt der ersten Spalte (commodity)
print(split_commodities[0].str.lower().str.strip().value_counts())


# In[23]:


# Anzeige erweitern, um mehr Werte zu sehen
pd.set_option('print.max_rows', 250)

# Kleinbuchstaben und Entfernen von Leerzeichen vorne/hinten
split_commodities[1] = split_commodities[1].str.lower().str.strip()

# Korrektur von häufigen Tippfehlern und unsauberen Schreibweisen
split_commodities[1] = split_commodities[1].str.replace("transformatin", "transformation", regex=False)
split_commodities[1] = split_commodities[1].str.replace("non energy uses", "consumption for non-energy uses", regex=False)
split_commodities[1] = split_commodities[1].str.replace(" /", "/", regex=False)
split_commodities[1] = split_commodities[1].str.replace("/ ", "/", regex=False)

# Kontrolle: Verteilung der bereinigten transaction_type
print(split_commodities[1].value_counts())


# In[24]:


# Nochmals prüfen: Was steht in additional_transaction_info?
print(split_commodities[2].str.lower().str.strip().value_counts())


# In[25]:


# Neue Spalten umbenennen, bevor wir sie ins Haupt-DataFrame einfügen
split_commodities.columns = ["commodity", "transaction_type", "additional_transaction_info"]

# Zusammenfügen entlang der Spaltenachse (axis=1)
df = pd.concat([df, 
                split_commodities["commodity"].str.lower(),
                split_commodities["transaction_type"],
                split_commodities["additional_transaction_info"].str.lower()], 
              axis=1)

# Vorschau: DataFrame nach Zusammenführung
print(df.head())

# ## Dropping and renaming irrelevant Data

# In[28]:

df.drop(columns=["commodity_transaction"], inplace=True)
df.drop(columns=["quantity_footnotes"], inplace=True)


# In[29]:

unit_counts = df["unit"].value_counts()

# Ausgabe
print("Verfügbare Einheiten und deren Häufigkeit:")
print(unit_counts)


# In[30]:


# Zeilen filtern, wo die Einheit "Metric Tons" ist
df_metric_tons = df[df["unit"] == "Metric Tons"]

# Vorschau
print(df_metric_tons)

print(f"Anzahl Zeilen mit Einheit 'Metric Tons': {df_metric_tons.shape[0]}")


# In[31]:


# Bedingung: Nur Zeilen mit Einheit "Metric Tons"
mask_metric_tons = df["unit"] == "Metric Tons"

# Menge durch 1000 teilen
df.loc[mask_metric_tons, "quantity"] = df.loc[mask_metric_tons, "quantity"] / 1000

# Einheit umbenennen auf "Metric tons, thousand", damit alles konsistent ist
df.loc[mask_metric_tons, "unit"] = "Metric tons, thousand"

print("Anpassung abgeschlossen. Einheit und Mengen für 'Metric Tons' sind jetzt normalisiert.")


# ## Bereinigtes CS Speichern und Check-Load: Gespeicherte Datei neu einlesen und prüfen
# 

# In[32]:


# Bereinigtes DataFrame als neue CSV speichern
# Neuer Pfad und Dateiname
OUTPUT_CLEANED_FILE = "/Users/yanickfischer/Documents/vsCode/MDM/mdm-project2-data-wrangling/data/energy_cleaned.csv"

# DataFrame als CSV speichern, ohne zusätzlichen Index
df.to_csv(OUTPUT_CLEANED_FILE, index=False)

print(f"Datei erfolgreich gespeichert unter: {OUTPUT_CLEANED_FILE}")


# In[33]:


# Datei neu einlesen
try:
    df_check = pd.read_csv(OUTPUT_CLEANED_FILE)
    print("Datei erfolgreich neu geladen. Vorschau:")
    print(df_check.head())
    
    print("\nForm der geladenen Datei:")
    print(df_check.shape)
except FileNotFoundError:
    print(f"Fehler: Datei {OUTPUT_CLEANED_FILE} nicht gefunden.")


# ## Filter for European countries

# In[34]:


# Liste europäischer Länder (sorgfältig zusammengestellt)
european_countries = [
    "Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia",
    "Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece",
    "Hungary", "Iceland", "Ireland", "Italy", "Kosovo", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg",
    "Malta", "Moldova", "Monaco", "Montenegro", "Netherlands", "North Macedonia", "Norway", "Poland",
    "Portugal", "Romania", "San Marino", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland",
    "Ukraine", "United Kingdom", "Vatican City"
]

# DataFrame auf europäische Länder filtern
df_europe = df[df["country_or_area"].isin(european_countries)]

# Vorschau auf das Ergebnis
print(df_europe.head())

print(f"Anzahl Zeilen nach Filterung auf europäische Länder: {df_europe.shape[0]}")


# In[35]:


# Alle einzigartigen Länder im DataFrame extrahieren und alphabetisch sortieren
unique_countries = sorted(df["country_or_area"].unique())

# Anzeige aller Länder
print("Liste der vorhandenen Länder im Datensatz:")
for country in unique_countries:
    print(country)

# Gesamtzahl der unterschiedlichen Länder
print(f"\nAnzahl unterschiedlicher Länder im Datensatz: {len(unique_countries)}")


# In[37]:


# Mapping von alternativen zu gesuchten Ländernamen
country_name_mapping = {
    "Czechia": "Czech Republic",
    "Republic of Moldova": "Moldova",
    "T.F.Yug.Rep. Macedonia": "North Macedonia"
    # Kosovo, Monaco, San Marino, Vatican City könnten tatsächlich fehlen
}

# Ländernamen im DataFrame ersetzen
df["country_or_area"] = df["country_or_area"].replace(country_name_mapping)

print("Ländernamen angepasst. Jetzt sind alternative Bezeichnungen vereinheitlicht.")

# Liste europäischer Länder (wie vorher definiert)
european_countries = [
    "Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia",
    "Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece",
    "Hungary", "Iceland", "Ireland", "Italy", "Kosovo", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg",
    "Malta", "Moldova", "Monaco", "Montenegro", "Netherlands", "North Macedonia", "Norway", "Poland",
    "Portugal", "Romania", "San Marino", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland",
    "Ukraine", "United Kingdom", "Vatican City"
]

# Alle eindeutigen Länder im Datensatz
unique_countries = set(df["country_or_area"].unique())

# Vergleich: Welche europäischen Länder fehlen?
missing_countries = [country for country in european_countries if country not in unique_countries]

# Ausgabe
if missing_countries:
    print("Diese europäischen Länder fehlen im Datensatz:")
    for country in missing_countries:
        print(f"- {country}")
else:
    print("Alle europäischen Länder aus der Liste sind im Datensatz vorhanden!")


# In[41]:


# Europäische Länderliste erneut definieren (falls nicht schon vorhanden)
european_countries = [
    "Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia",
    "Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece",
    "Hungary", "Iceland", "Ireland", "Italy", "Kosovo", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg",
    "Malta", "Moldova", "Monaco", "Montenegro", "Netherlands", "North Macedonia", "Norway", "Poland",
    "Portugal", "Romania", "San Marino", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland",
    "Ukraine", "United Kingdom", "Vatican City"
]

# DataFrame auf europäische Länder filtern (nach dem Mapping)
df_europe = df[df["country_or_area"].isin(european_countries)]

# Vorschau auf das gefilterte DataFrame
print(df_europe.head())

# Anzahl Zeilen nach Filter
print(f"\nAnzahl Zeilen mit europäischen Ländern: {df_europe.shape[0]}")

# Einzigartige europäischen Länder im gefilterten Datensatz
unique_european_countries = sorted(df_europe["country_or_area"].unique())

print(f"\nAnzahl unterschiedlicher europäischer Länder im Datensatz: {len(unique_european_countries)}")
print("\nListe der im Datensatz enthaltenen europäischen Länder:")
for country in unique_european_countries:
    print(f"- {country}")

# Überprüfung, ob noch Länder fehlen
missing_countries_final = [country for country in european_countries if country not in set(unique_european_countries)]

if missing_countries_final:
    print("\nDiese europäischen Länder fehlen nach finaler Anpassung weiterhin:")
    for country in missing_countries_final:
        print(f"- {country}")
else:
    print("\nAlle europäischen Länder aus der Liste sind jetzt im Datensatz vorhanden!")


# In[42]:


# Neuer Speicherpfad und Dateiname
OUTPUT_EUROPE_FILE = "/Users/yanickfischer/Documents/vsCode/MDM/mdm-project2-data-wrangling/data/energy_cleaned_europe.csv"

# DataFrame als CSV abspeichern, ohne Indexspalte
df_europe.to_csv(OUTPUT_EUROPE_FILE, index=False)

print(f"Europäischer Datensatz erfolgreich gespeichert unter: {OUTPUT_EUROPE_FILE}")


# In[43]:


# Überblick über numerische Werte (Mittelwert, Standardabweichung, Min, Max usw.)
print(df_europe.describe())

# Überblick über die Häufigkeit der Commodities (Energieträger)
print("\nVerteilung der Energieträger (commodity):")
print(df_europe["commodity"].value_counts())

# Überblick über die Häufigkeit der Transaktionstypen (transaction_type)
print("\nVerteilung der Transaktionstypen (transaction_type):")
print(df_europe["transaction_type"].value_counts())

# Überblick über die verwendeten Einheiten
print("\nVerwendete Einheiten (unit):")
print(df_europe["unit"].value_counts())


# In[ ]:




