import time
import re


def decorator_func(func):
    def wrappe(*args,**kwargs):
        start = time.time()
        sm = func(*args,**kwargs)
        end = time.time()
        print(f"{end - start} sekund")
        return sm
    return wrappe

class Contacts:
    def __init__(self):
        self.contacts=[]

    @decorator_func
    def add_contact(self,number,full_name):
        pattern = r"^\+998(90|91|93|94|95|97|98|99)\d{7}$"
        if re.match(pattern, number):
            self.contacts.append({"number": number,"full_name": full_name})
            print("Kontakt muvofaqyatli qo'shildi:)")
    print("Xatolik: Telefon raqam noto'g'ri kiritilgan!!!")

    def watch_list(self):
        if not self.contacts:
            print("Kontaktlar ro'yxati bo'sh")
        else:
            print("Kontaktlar ro'yxati:")
            for i, c in enumerate(self.contacts, 1):
                print(f"{i}. {c['full_name']} - {c['number']}")

    def del_contact(self,full_name):
        for c in self.contacts:
            if c["full_name"].lower()==full_name.lower():
                self.contacts.remove(c)
                print("Kontakt muvofiqiyatli o'chirildi:)")
                return
        print("Bunday kontakt mavjud emas!!!")


class Sms(Contacts):
    def __init__(self):
        super().__init__()
        self.SMS=[]

    def write_sms(self,phone,s):
        for c in self.contacts:
            if c["number"]==phone:
                self.SMS.append({"phone": phone,"sms": s})
                print("Sms muvofaqyatli jo'natildi:)")
                return
        print("Xatolik: Telefon raqam mavjud emas!!!")

    def watch_list(self):
        if not self.SMS:
            print("Smslar ro'yxati bo'sh!!!")
        else:
            print("Smslar ro'yxati: ")
            for i, s in enumerate(self.SMS, 1):
                print(f"{i}. {s['phone']} - {s['sms']}")

    def del_sms(self,phone):
        for s in self.SMS:
            if s["phone"]==phone:
                self.SMS.remove(s)
                print("Sms muvofiqiyatli o'chirildi:)")
                return
        print("Bunday raqam mavjud emas!!!")

contact=Contacts()
sms=Sms()

def sms_menu():
    print('''\n
    1. Sms yozish,
    2. Smslar listini ko'rish,
    3. Smsni o'chirish,
    4. Menuga qaytish
    ''')

    while True:
        try:
            s = int(input("S.Soni kiriting: "))
        except ValueError:
            print("Faqat son kiriting!!!")
            continue

        if s == 1:
            # misollar
            sms.write_sms("+998913698924","Salomlar")
            sms.write_sms("+998911320826","Uy ishini qildingmi???")
            ph=str(input("Telefon raqamni kiriting: "))
            sm=str(input("Texstni kiriting: "))
            sms.write_sms(ph,sm)

        elif s == 2:
            sms.watch_list()

        elif s == 3:
            # misollar
            sms.del_sms("+998913698924")
            ph = str(input("Telefon raqamni kiriting: "))
            sms.del_sms(ph)

        elif s == 4:
            return

        else:
            print("Xatolik iltimos menudagi sonlarni kiriting!!!")


def  contacts_menu():
    print('''\n
    1. Kontakt qo'shish,
    2. Kontaktlar listini ko'rish,
    3. Kontaktni o'chirish,
    4. Menuga qaytish
    ''')


    while True:
        try:
            num = int(input("K.Soni kiriting: "))
        except ValueError:
            print("Faqat son kiriting!!!")
            continue

        if num==1:
            # misollar
            contact.add_contact("+998913698924", "Ahror")
            contact.add_contact("+998911320826", "Begzod")
            number=str(input("Raqamingizni kiriting: "))
            name=str(input("Ismini kiriting: "))
            contact.add_contact(number,name)

        elif num==2:
            contact.watch_list()

        elif num==3:
            full_name=str(input("O'chirmoqchi bo'lgan kontakt ismini kiriting:"))
            contact.del_contact(full_name)

        elif num==4:
            return

        else:
            print("Xatolik iltimos menudagi sonlarni kiriting!!!")




def menu():

    while True:
        print('''\n
        Menu:
        1.Kontaktlar,
        2.Smslar,
        3.Chiqish
        ''')

        try:
            n = int(input("M.Son kiriting: "))
        except ValueError:
            print("Faqat son kiriting!")
            continue

        if n==1:
            contacts_menu()

        elif n==2:
            sms.contacts=contact.contacts
            sms_menu()

        elif n==3:
            print("Xayr salomat bo'ling:)")
            break

        else:
            print("Xatolik iltimos menudagi sonlarni kiriting!!!")


menu()