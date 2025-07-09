import sqlite3
import os


MA_LUMOT_BAZA = "avtosalon.db"


def bazani_yarat():
    with sqlite3.connect(MA_LUMOT_BAZA) as ulanish:
        c = ulanish.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS avtosalon (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nomi TEXT NOT NULL
        )""")
        c.execute("""
        CREATE TABLE IF NOT EXISTS mashina (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            avtosalon_id INTEGER,
            nomi TEXT NOT NULL,
            FOREIGN KEY (avtosalon_id) REFERENCES avtosalon(id) ON DELETE CASCADE
        )""")
        ulanish.commit()


def asosiy_salonlarni_qoshish():
    with sqlite3.connect(MA_LUMOT_BAZA) as ulanish:
        c = ulanish.cursor()
        c.execute("SELECT COUNT(*) FROM avtosalon")
        soni = c.fetchone()[0]
        if soni == 0:
            salonlar = ["Tesla Center", "Audi Prime", "Hyundai World", "Nissan Global", "Chevrolet Hub"]
            for salon in salonlar:
                c.execute("INSERT INTO avtosalon (nomi) VALUES (?)", (salon,))
            ulanish.commit()


def salonlarni_korsat():
    with sqlite3.connect(MA_LUMOT_BAZA) as ulanish:
        c = ulanish.cursor()
        c.execute("SELECT * FROM avtosalon")
        salonlar = c.fetchall()
        if not salonlar:
            print("Avtosalonlar topilmadi.")
        else:
            print("\nMavjud avtosalonlar:")
            for salon in salonlar:
                print(f"{salon[0]}. {salon[1]}")


def mashinalarni_korsat(salon_id):
    with sqlite3.connect(MA_LUMOT_BAZA) as ulanish:
        c = ulanish.cursor()
        c.execute("SELECT * FROM mashina WHERE avtosalon_id = ?", (salon_id,))
        mashinalar = c.fetchall()
        if not mashinalar:
            print("Bu salonda mashinalar yo'q.")
        else:
            print("Mashinalar ro'yxati:")
            for mashina in mashinalar:
                print(f"{mashina[0]}. {mashina[2]}")


def mashina_qoshish(salon_id):
    nomi = input("Mashina nomini kiriting: ")
    with sqlite3.connect(MA_LUMOT_BAZA) as ulanish:
        c = ulanish.cursor()
        c.execute("INSERT INTO mashina (avtosalon_id, nomi) VALUES (?, ?)", (salon_id, nomi))
        ulanish.commit()
        print("Mashina muvaffaqiyatli qo'shildi.")


def mashina_ochirish(salon_id):
    mashinalarni_korsat(salon_id)
    try:
        mashina_id = int(input("O'chirmoqchi bo'lgan mashinaning ID raqamini kiriting: "))
        with sqlite3.connect(MA_LUMOT_BAZA) as ulanish:
            c = ulanish.cursor()
            c.execute("DELETE FROM mashina WHERE id = ? AND avtosalon_id = ?", (mashina_id, salon_id))
            ulanish.commit()
            print("Mashina o'chirildi.")
    except:
        print("Xatolik! Raqam kiriting.")


def salon_qoshish():
    nomi = input("Yangi avtosalon nomini kiriting: ")
    with sqlite3.connect(MA_LUMOT_BAZA) as ulanish:
        c = ulanish.cursor()
        c.execute("INSERT INTO avtosalon (nomi) VALUES (?)", (nomi,))
        ulanish.commit()
        print("Avtosalon qo'shildi.")


def salon_ochirish():
    salonlarni_korsat()
    try:
        salon_id = int(input("O'chirmoqchi bo'lgan avtosalon ID raqamini kiriting: "))
        with sqlite3.connect(MA_LUMOT_BAZA) as ulanish:
            c = ulanish.cursor()
            c.execute("DELETE FROM avtosalon WHERE id = ?", (salon_id,))
            ulanish.commit()
            print("Avtosalon va unga tegishli mashinalar o'chirildi.")
    except:
        print("Xatolik! Raqam kiriting.")


def salon_panel(salon_id):
    with sqlite3.connect(MA_LUMOT_BAZA) as ulanish:
        c = ulanish.cursor()
        c.execute("SELECT nomi FROM avtosalon WHERE id = ?", (salon_id,))
        nom = c.fetchone()
        if not nom:
            print("Bunday salon mavjud emas.")
            return

    while True:
        print(f"\n--- {nom[0]} avtosalon paneli ---")
        print("1. Mashinalarni ko'rish")
        print("2. Mashina qo'shish")
        print("3. Mashinani o'chirish")
        print("4. Orqaga qaytish")

        tanlov = input("Tanlovni kiriting (1-4): ")

        if tanlov == '1':
            mashinalarni_korsat(salon_id)
        elif tanlov == '2':
            mashina_qoshish(salon_id)
        elif tanlov == '3':
            mashina_ochirish(salon_id)
        elif tanlov == '4':
            break
        else:
            print("Noto'g'ri tanlov.")


def asosiy_menyu():
    while True:
        print("\n--- AVTOSALON DASTURI ---")
        print("1. Avtosalonlar ro'yxatini ko'rish")
        print("2. Avtosalon qo'shish")
        print("3. Avtosalonni o'chirish")
        print("4. Dasturdan chiqish")

        tanlov = input("Tanlovni kiriting (1-4): ")

        if tanlov == '1':
            salonlarni_korsat()
            try:
                salon_id = int(input("\nQaysi salonga kirishni xohlaysiz (ID)? (0 - orqaga): "))
                if salon_id == 0:
                    continue
                salon_panel(salon_id)
            except:
                print("Xatolik! Raqam kiriting.")
        elif tanlov == '2':
            salon_qoshish()
        elif tanlov == '3':
            salon_ochirish()
        elif tanlov == '4':
            print("Dastur yakunlandi.")
            break
        else:
            print("Noto'g'ri tanlov.")


if __name__ == "__main__":
    bazani_yarat()
    asosiy_salonlarni_qoshish()
    asosiy_menyu()