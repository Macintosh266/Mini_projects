import time


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
        if number.isdigit():
            self.contacts.append({"number": number,"full_name": full_name})
            print("Kontakt muvofaqyatli qo'shildi:)")
        else:
            print("Xatolik: Telefon raqam noto'g'ri kiritilgan!!!")

    def watch_list(self):
        if not self.contacts:
            print("Kontaktlar ro'yxati bo'sh")
        else:
            print("Kontaktlar ro'yxati:")
            for i, contact in enumerate(self.contacts, 1):
                print(f"{i}. {contact['full_name']} - {contact['number']}")

    def del_contact(self,full_name):
        for contact in self.contacts:
            if contact["full_name"].lower()==full_name.lower():
                self.contacts.remove(contact)
                print("Kontakt muvofiqiyatli o'chirildi:)")
                return
            else:
                print("Bunday kontakt mavjud emas!!!")


def Menu():
    print('''
    Menu:
    1. Kontakt qo'shish,
    2. Kontaktlar listini ko'rish,
    3. Kontaktni o'chirish,"
    4. Chiqish
    ''')
    contact=Contacts()

    while True:
        num = int(input("Kiriting: "))

        if num==1:
            number=str(input("Raqamingizni kiriting: "))
            name=str(input("Ismini kiriting: "))
            contact.add_contact(number,name)

        elif num==2:
            contact.watch_list()

        elif num==3:
            full_name=str(input("O'chirmoqchi bo'lgan kontakt ismini kiriting:"))
            contact.del_contact(full_name)

        elif num==4:
            print("Xayr salomat bo'ling:)")
            break

        else:
            print("Xatolik iltimos menudagi sonlarni kiriting!!!")


Menu()
