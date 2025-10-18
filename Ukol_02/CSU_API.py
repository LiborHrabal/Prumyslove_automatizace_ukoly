# CSU_API.py 
# Knihovna pro práci s Českým statistickým úřadem (ČSÚ) API
import requests
import json

BASE = "https://data.csu.gov.cz/api"

def get_sady():
    url = f"{BASE}/katalog/v1/sady"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def get_vybery():
    url = f"{BASE}/katalog/v1/vybery"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def get_data_from_vyber_json(kod_vyber):
    url = f"{BASE}/dotaz/v1/data/vybery/{kod_vyber}"
    #params = {"format": fmt}
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def get_data_from_vyber_csv(kod_vyber):
    url = f"{BASE}/dotaz/v1/data/vybery/{kod_vyber}?format=CSV"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.content.decode("utf-8")

# Klicove slovo pro hledani v sadach
klicovoe_slovo = "podniky"

# --- Příklad použití  a ulozeni do csv souboru ---:
if __name__ == "__main__":
    sady = get_sady()
    if sady:
        for sada in sady:  # vypíše všechny sady
            kod_sady = sada["kod"]
            if klicovoe_slovo.lower() in sada["nazev"].lower(): # hledani podle klicoveho slova v nazvu sady
                print(f"Vybraná sada: {kod_sady} – {sada['nazev']}")
                vybery = get_vybery()
                vybery_pro_sadu = [v for v in vybery if v["sada"]["kod"] == kod_sady]
                print(vybery_pro_sadu)

                if vybery_pro_sadu:
                    for v in vybery_pro_sadu : # vypíše všechny výběry pro danou sadu 
                        print(f"  Výběr: {v['vyber']['kod']} – {v['vyber']['nazev']}")
                        kod_vyberu = v["vyber"]["kod"]
                        data = get_data_from_vyber_csv(kod_vyberu)
                        nazev = v["vyber"]["nazev"]
                        print(f"Kod vyberu: {kod_vyberu} Nazev: {nazev}")
                        with open(nazev+".csv", "w", encoding="utf-8") as f:
                            f.write(data)
                        print(f"Data uložena do souboru: {nazev}.csv")
                else:
                    print("Pro tuto sadu neexistuje žádný předdefinovaný výběr.")
    else:
        print("Žádné sady nebyly nalezeny.")
