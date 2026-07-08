import psycopg2

conn=psycopg2.connect(
    dbname="contact_manager_db",
    user="User_Sql",
    password="123",
    host="localhost",
    port="5432"
)

cur=conn.cursor()

def add_contact(number,name):
    conn.commit()
    if number.isdigit():
        cur.execute("insert into contacts(phone,first_name) values (%s,%s)",(number,name))
        print("Kontakt qo'shildi")
    else:
        print("Xatolik:Raqam xato kiritilgan")

def watch_list():
    cur.execute("SELECT * FROM contacts")
    rows = cur.fetchall()
    for row in rows:
        print(f"Telefon: {row[0]}, Ism: {row[1]}")

def del_contact(name):
    cur.execute("DELETE FROM contacts where first_name=%s",(name,))
    conn.commit()
    print("Kontakt o'chirildi")

def Menu():
    print('''
    Menu:
    1. Kontakt qo'shish,
    2. Kontaktlar listini ko'rish,
    3. Kontaktni o'chirish,
    4. Chiqish
    ''')

    while True:
        num = int(input("Raqam Kiriting: "))

        if num==1:
            number=str(input("Kontakt Telefon Raqamini kiriting: "))
            name=str(input("Kontakt Ismini kiriting: "))
            add_contact(number,name)

        elif num==2:
            watch_list()

        elif num==3:
            name=str(input("O'chirmoqchi bo'lgan kontakt ismini kiriting:"))
            del_contact(name)

        elif num==4:
            print("Xayr salomat bo'ling:)")
            break

        else:
            print("Xatolik iltimos menudagi sonlarni kiriting!!!")


Menu()
conn.close()
cur.close()
