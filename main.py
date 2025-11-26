import tkinter as tk
from tkinter import ttk, messagebox
import random

from AJ_receptmodul import AJRecept, AJ_betoltes_fajlbol, AJ_mentes_fajlba, AJ_export_recept_txt

ADAT_FAJL = "receptek.json"


class AJReceptFuzetAblak:
    def __init__(self, foablak):
        self.foablak = foablak
        self.foablak.title("AJ receptfüzete")
        self.foablak.geometry("900x520")

        self.receptek = AJ_betoltes_fajlbol(ADAT_FAJL)

        self.valasztott_kategoria = tk.StringVar(value="összes")

        self.felulet_felépítés()
        self.lista_frissites()

    def felulet_felépítés(self):
        keret_felso = ttk.Frame(self.foablak)
        keret_felso.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        ttk.Label(keret_felso, text="Szűrés kategória szerint:").pack(side=tk.LEFT)
        valaszto = ttk.Combobox(
            keret_felso,
            values=["összes", "leves", "főétel", "desszert"],
            state="readonly",
            textvariable=self.valasztott_kategoria,
            width=12
        )
        valaszto.pack(side=tk.LEFT, padx=5)
        valaszto.bind("<<ComboboxSelected>>", lambda e: self.lista_frissites())

        fo_keret = ttk.Frame(self.foablak)
        fo_keret.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        bal_keret = ttk.LabelFrame(fo_keret, text="Recept adatai")
        bal_keret.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        ttk.Label(bal_keret, text="Név:").grid(row=0, column=0, sticky="w")
        self.mezo_nev = ttk.Entry(bal_keret)
        self.mezo_nev.grid(row=0, column=1, sticky="ew", pady=2)

        ttk.Label(bal_keret, text="Kategória:").grid(row=1, column=0, sticky="w")
        self.mezo_kategoria = ttk.Combobox(
            bal_keret,
            values=["leves", "főétel", "desszert"],
            state="readonly"
        )
        self.mezo_kategoria.grid(row=1, column=1, sticky="ew", pady=2)
        self.mezo_kategoria.set("főétel")

        ttk.Label(bal_keret, text="Hozzávalók:").grid(row=2, column=0, sticky="nw")
        self.mezo_hozzavalok = tk.Text(bal_keret, height=6, width=40)
        self.mezo_hozzavalok.grid(row=2, column=1, sticky="nsew", pady=2)

        ttk.Label(bal_keret, text="Elkészítés:").grid(row=3, column=0, sticky="nw")
        self.mezo_leiras = tk.Text(bal_keret, height=10, width=40)
        self.mezo_leiras.grid(row=3, column=1, sticky="nsew", pady=2)

        bal_keret.columnconfigure(1, weight=1)
        bal_keret.rowconfigure(2, weight=1)
        bal_keret.rowconfigure(3, weight=2)

        gomb_keret = ttk.Frame(bal_keret)
        gomb_keret.grid(row=4, column=0, columnspan=2, pady=8)

        ttk.Button(gomb_keret, text="Új recept", command=self.uj_recept_urlap).grid(row=0, column=0, padx=4)
        ttk.Button(gomb_keret, text="Hozzáadás", command=self.recept_hozzaadas).grid(row=0, column=1, padx=4)
        ttk.Button(gomb_keret, text="Módosítás", command=self.recept_modositas).grid(row=0, column=2, padx=4)
        ttk.Button(gomb_keret, text="Törlés", command=self.recept_torles).grid(row=0, column=3, padx=4)

        ttk.Button(gomb_keret, text="Mentés", command=self.mentes_gomb).grid(row=0, column=4, padx=4)
        ttk.Button(gomb_keret, text="Export TXT", command=self.export_gomb).grid(row=0, column=5, padx=4)

        jobb_keret = ttk.LabelFrame(fo_keret, text="Receptlista")
        jobb_keret.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        self.lista = tk.Listbox(jobb_keret)
        self.lista.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.lista.bind("<<ListboxSelect>>", lambda e: self.kivalasztott_megjelenites())
        self.lista.bind("<Double-Button-1>", self.reszletek_ablak)

        ttk.Button(jobb_keret, text="Részletek külön ablakban", command=self.reszletek_ablak).pack(pady=3)
        ttk.Button(jobb_keret, text="Mai ajánlat", command=self.ajanlat_gomb).pack(pady=3)

    def szurt_receptek(self):
        kategoria = self.valasztott_kategoria.get()
        if kategoria == "összes":
            return list(self.receptek)
        return [r for r in self.receptek if r.kategoria == kategoria]

    def lista_frissites(self):
        self.lista.delete(0, tk.END)
        for recept in self.szurt_receptek():
            self.lista.insert(tk.END, f"{recept.kategoria} | {recept.nev}")

    def kivalasztott_index(self):
        kategoria = self.valasztott_kategoria.get()
        szurt = self.szurt_receptek()
        kijeloles = self.lista.curselection()
        if not kijeloles:
            return -1
        helyi_index = kijeloles[0]
        if kategoria == "összes":
            return helyi_index
        if helyi_index < len(szurt):
            recept = szurt[helyi_index]
            for i, r in enumerate(self.receptek):
                if r is recept:
                    return i
        return -1

    def urlap_torles(self):
        self.mezo_nev.delete(0, tk.END)
        self.mezo_kategoria.set("főétel")
        self.mezo_hozzavalok.delete("1.0", tk.END)
        self.mezo_leiras.delete("1.0", tk.END)

    def uj_recept_urlap(self):
        self.lista.selection_clear(0, tk.END)
        self.urlap_torles()

    def recept_hozzaadas(self):
        nev = self.mezo_nev.get().strip()
        kategoria = self.mezo_kategoria.get().strip()
        hozzavalok = self.mezo_hozzavalok.get("1.0", tk.END).strip()
        leiras = self.mezo_leiras.get("1.0", tk.END).strip()

        if not nev:
            messagebox.showwarning("Hiányzó adat", "A név mező kitöltése kötelező.")
            return

        if not kategoria:
            kategoria = "főétel"

        uj = AJRecept(nev, kategoria, hozzavalok, leiras)
        self.receptek.append(uj)
        self.lista_frissites()
        self.urlap_torles()
        messagebox.showinfo("Receptfüzet", "Az új recept elmentve a füzetbe.")

    def recept_modositas(self):
        index = self.kivalasztott_index()
        if index == -1:
            messagebox.showwarning("Nincs kijelölve", "Előbb válassz ki egy receptet a listából.")
            return

        nev = self.mezo_nev.get().strip()
        kategoria = self.mezo_kategoria.get().strip()
        hozzavalok = self.mezo_hozzavalok.get("1.0", tk.END).strip()
        leiras = self.mezo_leiras.get("1.0", tk.END).strip()

        if not nev:
            messagebox.showwarning("Hiányzó adat", "A név mező kitöltése kötelező.")
            return

        if not kategoria:
            kategoria = "főétel"

        r = self.receptek[index]
        r.nev = nev
        r.kategoria = kategoria
        r.hozzavalok = hozzavalok
        r.leiras = leiras

        self.lista_frissites()
        messagebox.showinfo("Receptfüzet", "A recept módosításra került.")

    def recept_torles(self):
        index = self.kivalasztott_index()
        if index == -1:
            messagebox.showwarning("Nincs kijelölve", "Előbb válassz ki egy receptet a listából.")
            return

        recept = self.receptek[index]
        if messagebox.askyesno("Recept törlése", f"Biztosan törlöd a(z) {recept.nev}-t?"):
            del self.receptek[index]
            self.lista_frissites()
            self.urlap_torles()

    def mentes_gomb(self):
        try:
            AJ_mentes_fajlba(ADAT_FAJL, self.receptek)
            messagebox.showinfo("Mentés", "A receptfüzet tartalma fájlba került.")
        except Exception as hiba:
            messagebox.showerror("Hiba", f"Hiba történt mentés közben:{hiba}")

    def export_gomb(self):
        index = self.kivalasztott_index()
        if index == -1:
            messagebox.showwarning("Nincs kijelölve", "Előbb válassz ki egy receptet.")
            return
        recept = self.receptek[index]
        try:
            ut = AJ_export_recept_txt(recept)
            messagebox.showinfo("Export", f"A recept külön fájlba került:{ut}")
        except Exception as hiba:
            messagebox.showerror("Hiba", f"Hiba történt exportálás közben:{hiba}")

    def kivalasztott_megjelenites(self):
        index = self.kivalasztott_index()
        if index == -1:
            return
        r = self.receptek[index]
        self.mezo_nev.delete(0, tk.END)
        self.mezo_nev.insert(0, r.nev)
        self.mezo_kategoria.set(r.kategoria)
        self.mezo_hozzavalok.delete("1.0", tk.END)
        self.mezo_hozzavalok.insert(tk.END, r.hozzavalok)
        self.mezo_leiras.delete("1.0", tk.END)
        self.mezo_leiras.insert(tk.END, r.leiras)

    def reszletek_ablak(self, event=None):
        index = self.kivalasztott_index()
        if index == -1:
            messagebox.showwarning("Nincs kijelölve", "Előbb válassz ki egy receptet.")
            return
        r = self.receptek[index]

        ablak = tk.Toplevel(self.foablak)
        ablak.title(r.nev)
        ablak.geometry("520x440")

        ttk.Label(ablak, text=r.nev, font=("Arial", 14, "bold")).pack(pady=4)
        ttk.Label(ablak, text=f"Kategória: {r.kategoria}").pack(pady=2)

        ttk.Label(ablak, text="Hozzávalók:", font=("Arial", 11, "underline")).pack(anchor="w", padx=10)
        szoveg_hozz = tk.Text(ablak, height=6, wrap="word")
        szoveg_hozz.pack(fill=tk.BOTH, expand=False, padx=10, pady=4)
        szoveg_hozz.insert(tk.END, r.hozzavalok)
        szoveg_hozz.config(state="disabled")

        ttk.Label(ablak, text="Elkészítés:", font=("Arial", 11, "underline")).pack(anchor="w", padx=10)
        szoveg_leir = tk.Text(ablak, height=10, wrap="word")
        szoveg_leir.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)
        szoveg_leir.insert(tk.END, r.leiras)
        szoveg_leir.config(state="disabled")

    def ajanlat_gomb(self):
        if not self.receptek:
            messagebox.showinfo("Mai ajánlat", "A füzet még üres, előbb vigyél fel pár receptet.")
            return
        recept = random.choice(self.receptek)
        messagebox.showinfo("Mai ajánlat", f"Ma ezt főzném:{recept.kategoria} | {recept.nev}")


def main():
    app = tk.Tk()
    AJReceptFuzetAblak(app)
    app.mainloop()


if __name__ == "__main__":
    main()
