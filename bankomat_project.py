import psycopg2


class Bankomat:
    def __init__(self,connection):
        self.conn=connection
        self.cor=self.conn.cursor()
        self.card_num=0


    def withdraw(self,amount):
        self.cor.execute("SELECT Balance FROM cards WHERE CardNum = %s", (self.card_num,))
        result = self.cor.fetchone()
        if result[0]<int(amount):
            print("Balansingizda yetarli mablag' mavjud emas!")
        else:
            r=result[0]-int(amount)
            self.cor.execute("UPDATE cards SET Balance=%s WHERE CardNum= %s",(r,self.card_num))
            self.conn.commit()
            print(f"Balansingizdan {amount} so'm yechildi")



    def deposit(self,amount):
        self.cor.execute("SELECT Balance FROM cards WHERE CardNum = %s", (self.card_num,))
        result = self.cor.fetchone()
        a=result[0]+int(amount)
        self.cor.execute("UPDATE cards SET Balance=%s WHERE CardNum= %s",(a,self.card_num))
        self.conn.commit()
        print(f"Balansingizga: {amount} so'm qo'shildi")

    def check_balance(self):
        self.cor.execute("SELECT Balance FROM cards WHERE CardNum = %s", (self.card_num,))
        result = self.cor.fetchone()
        if result:
            print(f"Balansingizda: {result[0]} so'm bor")
        else:
            print("Balans topilmadi!")


    def login(self,card_num,code):
        self.cor.execute("SELECT Code FROM cards WHERE CardNum = %s", (card_num,))
        result = self.cor.fetchone()
        if result:
            if result[0] == code:
                print("Login muvaffaqiyatli")
                self.card_num = card_num
                return 1
            else:
                print("Kod xato kiritilgan!")
                return 0
        else:
            print("Bunday karta mavjud emas!")
            return 0

    def create_account(self, card_num, code):
        self.cor.execute("INSERT INTO cards(CardNum, Code, Balance) VALUES (%s, %s, %s)", (card_num, code, 0))
        self.conn.commit()
        print("Karta muvaffaqiyatli qo'shildi")

    def close(self):
        self.conn.close()
        self.cor.close()

def menu(b):
    while True:

        print('''
        1. Yangi akkaunt yaratish,
        2. Login akkaunt
        3. Chiqish
        ''')

        try:
            s = int(input("Soni kiriting: "))
        except ValueError:
            print("Faqat son kiriting!")
            continue

        if s ==1:
            k=input("Karta raqami(16talik): ")
            c=input("Code: ")
            b.create_account(k,c)

        elif s ==2:
            k=input("Karta raqami (16talik): ")
            c=input("Code: ")
            log=b.login(k,c)
            if log==1:

                while True:
                    print('''\n
                        Menu
                        1. Naqt Pul yechish,
                        2. Balansni ko'rish,
                        3. Pul tashlash,
                        4. Chiqish
                        ''')

                    try:
                        n = int(input("Soni kiriting: "))
                    except ValueError:
                        print("Faqat son kiriting!")
                        continue

                    if n == 1:
                        s = input("Summani kiriting: ")
                        b.withdraw(s)

                    elif n == 2:
                        b.check_balance()

                    elif n == 3:
                        s = input("Summani kiriting: ")
                        b.deposit(s)

                    elif n == 4:
                        print("Xayr salomat bo'ling:)")
                        break

                    else:
                        print("Menuda ko'rsatilgan sonlarni kiriting!")


        elif s==3:
            return

        else:
            print("Menuda ko'rsatilgan sonlarni kiriting!")



if __name__=="__main__":

    conn = psycopg2.connect(
        dbname="avto_salon_db",
        user="User_Sql",
        password="123",
        host="localhost",
        port="5432"
    )

    cor=conn.cursor()

    bankomat=Bankomat(conn)

    menu(bankomat)