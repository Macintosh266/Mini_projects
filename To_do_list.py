import psycopg2

class TDL:
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        self.conn=psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cur=self.conn.cursor()
        self.user_id=0

    def create_accaunt(self,username,pw):
        self.cur.execute("INSERT INTO users(username,password) values (%s,%s)",(username,pw))
        self.conn.commit()
        print("Akkaunt muvofaqiyatli qo'shildi")

    def login(self,username,pw):
        self.cur.execute("SELECT password,user_id from users WHERE username=%s",(username, ))
        result=self.cur.fetchone()
        if result is None:
            print("Foydalanuvchi topilmadi!")
            return 0
        password,user_id=result
        if password==pw:
            self.user_id=user_id
            print(f"Hush kelibsiz {username}")
            return 1
        else:
            print("Kod xato kiritilgan!")
            return 0


    def watch_list(self):
        r=""
        self.cur.execute("SELECT * FROM tasks WHERE user_id=%s",(self.user_id, ))
        rows=self.cur.fetchall()
        if not rows:
            print("Hozircha hech qanday tasklar mavjud emas!")
        else:
            for row in rows:
                if row[2]=="True":
                    r="yo'q"
                elif row[2]=="False":
                    pass
                print(f"ID: {row[3]}| Task: {row[0]} | Time: {row[1]} | Qilindimi: {r}")

    def del_task(self,task_id):
        self.cur.execute("UPDATE tasks SET is_active=%s  WHERE task_id=%s and user_id=%s",
                         ("false",task_id,self.user_id))
        self.conn.commit()
        print("Mashg'ulot o'chirildi")

    def add_task(self,task,time):
        is_active="true"
        self.cur.execute("INSERT INTO tasks(user_id,task,time,is_active) values (%s,%s,%s,%s)",
                         (self.user_id,task,time,is_active))
        self.conn.commit()
        print("Mashg'ulot muvofaqiyatli qo'shildi")

    def update_task(self,task_id,task,time,is_active):
        self.cur.execute("UPDATE tasks SET task=%s, time=%s, is_active=%s  WHERE task_id=%s and user_id=%s",
                         (task,time,is_active,task_id,self.user_id))
        self.conn.commit()
        print("Mashg'ulot yangilandi")


    def close(self):
        self.conn.close()
        self.cur.close()


tdl=TDL('Full_db', 'User_Sql', '123')

def tasks_menu():

    while True:
        print('''
        Menu
        1. tasklarni ko'rish,
        2. task ni o'chirish(True yoki False qilish),
        3. task qo'shish,
        4. tasklarni yangilash
        5. bosh menuga qaytish
        ''')

        n=input("Soni kiriting: ")

        if n=="1":
            tdl.watch_list()

        elif n == "2":

            ta_id = input("Mashg'ulot idsi: ")

            tdl.del_task(int(ta_id))

        elif n == "3":

            ta = input("Mashg'ulot: ")

            ti = input("Vaqti (YYYY-MM-DD HH:MM:SS): ")

            tdl.add_task(ta, ti)

        elif n == "4":
            ta_id=input("Mashg'ulot idsi: ")
            ta=input("Mashg'ulot: ")
            ti=input("Vaqti (YYYY-MM-DD HH:MM:SS): ")
            q=input("Qilindimi (ha/yo'q): ")


            if q.lower() == "yo'q":
                q="true"
            elif q.lower() == "ha":
                q="false"


            tdl.update_task(ta_id,ta,ti,q)

        elif n=="5":
            return


def menu():

    while True:
        print('''\n
        1. Login kirish,
        2. Yangi akkaunt yaratish
        ''')

        n=input("Soni kiriting: ")


        if n == "1":
            l=input("Username: ")
            p=input("Password: ")


            if tdl.login(l,p)==1:
                while True:
                    print('''
        1. Tasklar,
        2. Chiqish
        ''')

                    num=input("Soni kiriting: ")

                    if num=="1":
                        tasks_menu()

                    elif num=="2":
                        return

                    else:
                        print("Menuda ko'rsatilgan sonlarni kiriting!")

        elif n == "2":
            l=input("Username: ")
            p=input("Password: ")

            tdl.create_accaunt(l,p)

        else:
            print("Menuda ko'rsatilgan sonlarni kiriting!")

menu()


# ____________________________
#  Users jadvali
#  CREATE TABLE users (
#      user_id SERIAL PRIMARY KEY,
#      username VARCHAR(50) ,
#      password VARCHAR(255)
#  );
# -------------------------
#  Tasks jadvali
#  CREATE TABLE tasks (
#      task_id SERIAL PRIMARY KEY,
#      user_id INT,
#      task TEXT,
#      time TIMESTAMP,
#      is_active BOOLEAN DEFAULT TRUE,
#      FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
#  );