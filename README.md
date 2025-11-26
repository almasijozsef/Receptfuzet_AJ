# AJ Receptfüzet

Hallgató: Almási József  
Neptun-kód: S958I6  

## Rövid leírás

A program egy grafikus receptfüzet.  
Lehet benne recepteket felvenni, módosítani, törölni, fájlba menteni, betölteni, valamint véletlenszerű "Mai ajánlatot" kérni.  
A recepteket kategóriák szerint kezeli: leves, főétel, desszert.

A grafikus felület `tkinter` és `ttk` modulokra épül, az adatok tárolása JSON fájlban történik.

## Fő fájlok

- `main.py` – a program indító fájlja, grafikus felület
- `AJ_receptmodul.py` – saját modul, amely a recept adatszerkezetét és a fájlkezelő függvényeket tartalmazza
- `receptek.json` – a receptadatbázis fájlja

## Használt modulok

- Beépített modulok:
  - `json`
  - `os`
  - `random`
- Grafikus modulok:
  - `tkinter`
  - `tkinter.ttk`
  - `tkinter.messagebox`
- Saját modul:
  - `AJ_receptmodul`

## Saját osztályok

- `AJRecept`  
  Egyetlen recept adatait tárolja: név, kategória, hozzávalók, elkészítés.

- `AJReceptFuzetAblak`  
  A teljes grafikus felületet megvalósító osztály.  
  Feladata a receptek megjelenítése, szerkesztése, szűrése, mentése és exportálása.

## Saját függvények

A saját modulban (`AJ_receptmodul.py`):

- `AJ_betoltes_fajlbol(fajlnev)`  
  Beolvassa a recepteket a megadott JSON fájlból, és `AJRecept` objektumok listáját adja vissza.

- `AJ_mentes_fajlba(fajlnev, receptek)`  
  Elmenti a kapott `AJRecept` objektumok listáját JSON fájlba.

- `AJ_export_recept_txt(recept)`  
  A megadott receptet külön szövegfájlba exportálja, és visszaadja a létrehozott fájl elérési útját.

A főprogramban (`main.py`):

- `main()`  
  Létrehozza a fő ablakot (`root`), példányosítja az `AJReceptFuzetAblak` osztályt, és elindítja a grafikus eseménykezelő ciklust.

## A program használata

1. **Indítás**
   - A program a `main.py` futtatásával indítható.
   - A főablakban bal oldalon a "Recept adatai", jobb oldalon a "Receptlista" látható.

2. **Receptlista szűrése kategóriák szerint**
   - A felső legördülő listában választható kategória: **összes**, **leves**, **főétel**, **desszert**.
   - A lista tartalma azonnal frissül a választott kategória alapján.

3. **Új recept felvétele**
   - A bal oldali mezőkben töltsd ki a következőket:
     - **Név** – a recept neve.
     - **Kategória** – leves / főétel / desszert.
     - **Hozzávalók** – tetszőleges szöveg, több sorban is.
     - **Elkészítés** – a lépések leírása.
   - Kattints a **„Hozzáadás”** gombra.
   - A recept megjelenik a listában, majd a **„Mentés”** gombbal a fájlba is elmenthető.

4. **Meglévő recept kiválasztása**
   - A jobb oldali listában kattints egy receptre.
   - A recept adatai automatikusan betöltődnek a bal oldali mezőkbe.
   - Kétszeri kattintásra külön ablakban is megnyitható a recept.

5. **Recept módosítása**
   - Válaszd ki a módosítandó receptet a listából.
   - A bal oldali mezőkben írd át a szükséges adatokat.
   - Kattints a **„Módosítás”** gombra.
   - A lista frissül, a módosított recept tartalma elmentődik a memóriában.
   - A **„Mentés”** gombbal a módosítások bekerülnek a JSON fájlba is.

6. **Recept törlése**
   - Válaszd ki a törölni kívánt receptet a listából.
   - Kattints a **„Törlés”** gombra.
   - A megjelenő kérdésnél válaszd az **„Igen”** lehetőséget a végleges törléshez.

7. **Recept mentése fájlba**
   - A **„Mentés”** gomb az összes jelenlegi receptet elmenti a `receptek.json` fájlba.
   - A program indításkor ebből a fájlból tölti vissza a recepteket.

8. **Recept exportálása TXT fájlba**
   - Válassz ki egy receptet a listából.
   - Kattints az **„Export TXT”** gombra.
   - A program létrehoz egy külön szövegfájlt, amely a recept nevét tartalmazza (például: `Gulyasleves_egyszeruen.txt`).

9. **Recept részletes megjelenítése külön ablakban**
   - Válassz ki egy receptet, majd kattints a **„Részletek külön ablakban”** gombra,
     vagy kattints duplán a listában.
   - A felugró ablakban csak olvasható formában látható a név, kategória, hozzávalók és elkészítés.

10. **„Mai ajánlat” funkció**
    - Kattints a **„Mai ajánlat”** gombra.
    - A program véletlenszerűen kiválaszt egy receptet, és megjeleníti egy üzenetablakban.
