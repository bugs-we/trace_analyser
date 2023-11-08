import re
import os
import tkinter as tk
from tkinter import messagebox
import traceback

def analyze_logfiles(directory):
    # Zähler für verschiedene Ereignisse initialisieren
    error_count = 0
    warning_count = 0
    info_count = 0

    # Liste für betroffene Zeilen erstellen
    matched_lines = []

    # Alle Dateien im angegebenen Verzeichnis durchgehen
    for filename in os.listdir(directory):
        if filename.endswith(".log"):
            # Vollständigen Pfad zur Logdatei erstellen
            logfile_path = os.path.join(directory, filename)

            # Logdatei öffnen
            with open(logfile_path, 'r', encoding='utf-8') as logfile:
                # Logdatei Zeile für Zeile durchgehen
                lines = logfile.readlines()
                for line_number, line in enumerate(lines, start=1):
                    # Zeile auf bestimmte Muster überprüfen
                    if re.search(r'ERROR', line):
                        error_count += 1
                        # Zeilen vor und nach dem Fehler extrahieren
                        start_line = max(line_number - 2, 1)
                        end_line = min(line_number + 9, len(lines))
                        matched_lines.append((filename, line_number, line, lines[start_line-1:end_line]))

                    elif re.search(r'WARNING', line):
                        warning_count += 1
                        # Zeilen vor und nach dem Fehler extrahieren
                        start_line = max(line_number - 2, 1)
                        end_line = min(line_number + 9, len(lines))
                        matched_lines.append((filename, line_number, line, lines[start_line-1:end_line]))
                        
                    elif re.search(r'INFO', line):
                        info_count += 1

    # Ergebnisse anzeigen
    messagebox.showinfo("Ergebnisse", f"Anzahl der Fehler: {error_count}\nAnzahl der Warnungen: {warning_count}\nAnzahl der Informationen: {info_count}")

    # Betroffene Zeilen in Datei exportieren, wenn vorhanden
    if matched_lines:
        output_file = 'E:\\trace_analyzier\\matched\\matched_lines.txt'
        with open(output_file, 'w', encoding='utf-8') as file:
            try:
                file.write("Betroffene Zeilen:\n")
                for filename, line_number, line, context_lines in matched_lines:
                    file.write(f"{filename}, Zeile {line_number}: {line}\n")
                    file.write("Vorherige Zeilen:\n")
                    for context_line in context_lines[:2]:
                        file.write(f"{context_line}\n")
                    file.write("Nachfolgende Zeilen:\n")
                    for context_line in context_lines[2:]:
                        file.write(f"{context_line}\n")
            except Exception as e:
                traceback.print_exc()

        print(f"Betroffene Zeilen wurden in die Datei '{output_file}' exportiert.")
    else:
        print("Es wurden keine betroffenen Zeilen gefunden.")

# Beispielaufruf der Funktion für ein bestimmtes Verzeichnis
directory = 'e:\\traininglogs\\'
analyze_logfiles(directory)
