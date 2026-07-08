import psycopg2
import re

class Avto:
    def __init__(self,connection):
        self.conn = connection
        self.cur = self.conn.cursor()


    def add_avto(self,s_id,marc,color):
        self.cur.execute("Insert into avto values (%s,%s,%s)", (s_id, marc, color))
        self.conn.commit()
        print("Mashina muvofiqiyatli qo'shildi:)")


    def watch_avto(self):
        self.cur.execute("select count(*) from avto")
        result=self.cur.fetchone()
        if result[0]==0:
            print("Jadval bo'sh!")
        else:
            self.cur.execute("Select * from avto")
            rows=self.cur.fetchall()
            for row in rows:
                print(f"Salon_id: {row[0]}, Markasi: {row[1]}, Rangi: {row[2]}")


    def del_avto(self,marc):
        self.cur.execute("Delete from avto where avto_name=(%s)",(marc,))
        self.conn.commit()
        print("Mashina muvofiqiyatli o'chirildi:)")


    def editing(self):
        self.cur.execute("select count(*) from avto")
        result=self.cur.fetchone()
        if result[0]==0:
            print("Jadval bo'sh!")
        else:
            join='''select * from avto_salons s
            inner join avto a on s.salon_id=a.salon_id
            '''
            self.cur.execute(join)
            rows=self.cur.fetchall()
            for row in rows:
                print(f"Salon_id: {row[0]}, Salon_ismi: {row[1]}, Salon_telefoni: {row[2]},\n"
                      f"MashinaMarkasi: {row[4]}, MashinaRangi: {row[5]}")



    def close(self):
        self.cur.close()
        self.conn.close()





class AvtoSalons:
    def __init__(self, connection):
        self.conn = connection
        self.cur = self.conn.cursor()


    def add_salon(self,s_id,s_name,phone):
        pattern = r"^\+998(90|91|93|94|95|97|98|99)\d{7}$"
        if re.match(pattern, phone):
            self.cur.execute("Insert into avto_salons values (%s,%s,%s)",(s_id,s_name,phone))
            self.conn.commit()
            print("Salon muvofiqiyatli qo'shildi:)")
        else:
            print("Raqam noto'g'ri kiritilgan!")


    def watch_salons(self):
        self.cur.execute("select count(*) from avto_salons")
        result=self.cur.fetchone()
        if result[0]==0:
            print("Jadval bo'sh!")
        else:
            self.cur.execute("Select * from avto_salons")
            rows=self.cur.fetchall()
            for row in rows:
                print(f"Salon_id: {row[0]}, Salon_ismi: {row[1]}, Salon_telefoni: {row[2]}")


    def del_salon(self,id):
        self.cur.execute("Delete from avto_salons where salon_id=(%s)",(id,))
        self.cur.execute("Delete from avto where salon_id=(%s)",(id,))
        self.conn.commit()
        print("Salon muvofiqiyatli o'chirildi:)")


    def close(self):
        self.cur.close()
        self.conn.close()



def avto_menu(a):
    print('''\n
    1. mashina qoshish,
    2. mashinalar listi,
    3. mashina o'chirish,
    4. mashina tahrirlash
    5. menuga qaytish
    ''')

    while True:

        try:
            n=int(input("A.Soni kiriting: "))
        except ValueError:
            print("Faqat son kiriting!")
            continue

        if n==1:
            s_id=input("Salon idsini kiriting: ")
            marc=input("Mashina markasini kiriting: ")
            color=input("Mashina rangini kiriting: ")
            a.add_avto(s_id,marc,color)

        elif n==2:
            a.watch_avto()

        elif n==3:
            marc=input("Mashina markasini kiriting: ")
            a.del_avto(marc)

        elif n==4:
            a.editing()

        elif n==5:
            return

        else:
            print("Menuda ko'rsatilgan sonlarni kiriting! ")




def menu(s,a):
    while True:
        print('''\n
        Menu:
        1. Avto salon yaratish,
        2. Avto salon tanlash,
        3. Avto salonlarni ko'rish,
        4. Avto salon o'chirish,
        5. Chiqish
        ''')
        try:
            n=int(input("M.Soni kiriting: "))
        except ValueError:
            print("Faqat son kiriting!")
            continue

        if n==1:
            s_id=input("Salon idsini kiriting: ")
            s_name=input("Salon nomini kiriting: ")
            s_phone=input("Saloning telefon raqamini kiriting: ")
            s.add_salon(s_id,s_name,s_phone)

        elif n==2:
            avto_menu(a)

        elif n==3:
            s.watch_salons()

        elif n==4:
            s_id=input("Salon idsini kiriting: ")
            s.del_salon(s_id)

        elif n==5:
            print("Xayr salomat bo'ling:)")
            break

        else:
            print("Menuda ko'rsatilgan sonlarni kiriting! ")



if __name__ == "__main__":

    conn = psycopg2.connect(
        dbname="avto_salon_db",
        user="User_Sql",
        password="123",
        host="localhost",
        port="5432"
    )

    a_s=AvtoSalons(conn)
    avto = Avto(conn)

    menu(a_s,avto)




# Salonlar ustunlarini yaratish uchun:

# s1='''
# create table avto_salons(
# 	salon_id smallint primary key,
# 	salon_name character varying(15),
#   phone character varying(15)
# )'''
#
# s2='''
# create table avto(
# 	salon_id smallint,
# 	avto_name character varying(15),
# 	avto_color character varying(20)
# )'''