# Energy Data Wrangling - MDM Projekt 2 Vorbereitung

## 1. Überblick

Dieses Repository enthält ein vollständiges Data-Wrangling-Skript (preprocessing.py) sowie ein umfassendes Data-Exploration-Notebook (data_exploration_final.ipynb), das auf dem internationalen Energie-Datensatz der Vereinten Nationen basiert.
Die Bereinigung und Exploration dienen als gezielte Vorbereitung für Projekt 2 im Modul MDM.

⸻

## 2. Ziel
	•	Vorbereitung eines sauberen, europäischen Energiedatensatzes als Input für spätere Machine-Learning-Modelle.
	•	Bereitstellung eines kompakten, strukturierten DataFrame, der sich einfach in Java/Spring Boot Web-Services integrieren lässt.
	•	Standardisierung der Einheiten, um eine vergleichbare Analyse und verlässliche Prognosemodelle zu ermöglichen.

⸻

## 3. Datenquelle

Die Rohdaten stammen von Kaggle:

International Energy Statistics – United Nations

⸻

## 4. Durchführung
	•	Import und Analyse der Originaldaten (all_energy_statistics.csv).
	•	Bereinigung der commodity_transaction-Spalte durch sauberes Aufsplitten in commodity, transaction_type und additional_transaction_info.
	•	Entfernen irrelevanter Spalten (quantity_footnotes, commodity_transaction) zur Reduktion der Komplexität.
	•	Vereinheitlichung der Einheiten:
	•	Konvertierung verschiedener Energieangaben auf eine standardisierte Basis in Megajoule (MJ).
	•	Filterung auf europäische Länder (nur relevante Länder behalten).
	•	Vereinheitlichung von Ländernamen (z.B. “Czechia” → “Czech Republic”).
	•	Speicherung des bereinigten und erweiterten Datensatzes in energy_cleaned_europe_final.csv.

⸻

## 5. Erweiterung: Explorative Datenanalyse (EDA)

Im Jupyter Notebook data_exploration_final.ipynb wurde eine umfangreiche erste Analyse der Daten durchgeführt:
	•	Identifikation grüner Energieträger und Markierung im Datensatz (is_green_energy-Spalte).
	•	Normierung aller Mengenangaben auf Megajoule (MJ).
	•	Zeitliche Entwicklung der Energieproduktion je Land.
	•	Vergleich der Länder nach Anteil grüner Energie über die Jahre hinweg.
	•	Interaktive Visualisierung mit Plotly, um Entwicklungen pro Jahr dynamisch zu betrachten.

⸻

## 6. Ziel: Beantwortung der Projektfragen

Die Vorverarbeitung und Exploration bereiten gezielt die Beantwortung folgender Fragestellungen vor:
	1.	Prognose Schweiz:
Wie entwickelt sich der Energie-Mix der Schweiz in Zukunft?
	2.	Vergleich europäischer Länder:
Wie “grün” sind verschiedene europäische Länder im Hinblick auf ihre Energiequellen?

⸻

## 7. Bedeutung für das Java/Spring Boot Projekt

Das MDM-Projekt zwei wird in diesem Repository dokumentiert:
https://github.com/yanickfischer/mdm-project2

Sämtliche hier gemachten Vorbereitungen dienen diesem Projekt.

Durch diese strukturierte Datenaufbereitung haben wir die Grundlage geschaffen, um:
	•	saubere REST-APIs in Spring Boot zu entwickeln, die auf einem einheitlichen Datensatz basieren.
	•	Machine-Learning-Modelle effizient trainieren und auswerten zu können (z.B. Zeitreihenprognosen oder Klassifikationsmodelle).
	•	Vergleiche und Visualisierungen im Frontend konsistent und nachvollziehbar aufzubauen.

Ohne diese Vorbereitung wäre die Entwicklung robuster, produktionsreifer Services erheblich aufwändiger und fehleranfälliger gewesen.