import json
import os


class AJRecept:
    def __init__(self, nev, kategoria, hozzavalok, leiras):
        self.nev = nev
        self.kategoria = kategoria
        self.hozzavalok = hozzavalok
        self.leiras = leiras


def AJ_betoltes_fajlbol(fajlnev):
    if not os.path.exists(fajlnev):
        return []
    try:
        with open(fajlnev, "r", encoding="utf-8") as f:
            adatok = json.load(f)
    except Exception:
        return []
    receptek = []
    for elem in adatok:
        nev = elem.get("nev", "")
        kategoria = elem.get("kategoria", "")
        hozzavalok = elem.get("hozzavalok", "")
        leiras = elem.get("leiras", "")
        receptek.append(AJRecept(nev, kategoria, hozzavalok, leiras))
    return receptek


def AJ_mentes_fajlba(fajlnev, receptek):
    lista = []
    for r in receptek:
        lista.append(
            {
                "nev": r.nev,
                "kategoria": r.kategoria,
                "hozzavalok": r.hozzavalok,
                "leiras": r.leiras,
            }
        )
    with open(fajlnev, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=2)


def AJ_export_recept_txt(recept):
    safe_name = "".join(c for c in recept.nev if c.isalnum() or c in " _-").strip()
    if not safe_name:
        safe_name = "recept"
    fajlnev = safe_name.replace(" ", "_") + ".txt"
    with open(fajlnev, "w", encoding="utf-8") as f:
        f.write(recept.nev + "\n")
        f.write("Kategória: " + recept.kategoria + "\n\n")
        f.write("Hozzávalók:\n")
        f.write(recept.hozzavalok + "\n\n")
        f.write("Elkészítés:\n")
        f.write(recept.leiras + "\n")
    return os.path.abspath(fajlnev)
