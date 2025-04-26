# Energy Data Wrangling - MDM Projekt 2 Vorbereitung

## Überblick

Dieses Repository enthält ein vollständiges Data-Wrangling-Skript (preprocessing.py), das auf dem internationalen Energie-Datensatz der Vereinten Nationen basiert.
Die Bereinigung dient als Vorbereitung für Projekt 2 im Modul MDM.

## Ziel
	•	Vorbereitung eines sauberen, europäischen Energiedatensatzes als Input für spätere Machine-Learning-Modelle.
	•	Bereitstellung eines kompakten, strukturierten DataFrame, der sich einfach in Java/Spring Boot Web-Services integrieren lässt.

## Datenquelle

Die Rohdaten stammen von Kaggle: https://www.kaggle.com/datasets/unitednations/international-energy-statistics/data


## Durchführung
	•	Import und Analyse der Originaldaten (all_energy_statistics.csv).
	•	Bereinigung der commodity_transaction-Spalte durch sauberes Aufsplitten in commodity, transaction_type und additional_transaction_info.
	•	Entfernen irrelevanter Spalten und Vereinheitlichung von Einheiten (Metric Tons normalisiert zu Metric tons, thousand).
	•	Filterung auf europäische Länder.
	•	Vereinheitlichung von Ländernamen (z.B. “Czechia” → “Czech Republic”).
	•	Speicherung der bereinigten europäischen Daten in energy_cleaned_europe.csv.