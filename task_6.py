from collections import UserDict
import re
from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, name):
        if name:
            super().__init__(name)
        else:
            raise ValueError("You have not enterd name!")

class Phone(Field):
    def __init__(self, phone):
        if len(phone) == 10 and phone.isdigit():
            super().__init__(phone)
        else:
            raise ValueError("You have enterd less than 10 digitals!")
        
class Birthday(Field):
    def __init__(self, value):
        print(f"Entered value {value}")
        pattern = r'^\d{2}\.\d{2}\.\d{4}$'
        try:
            # pass
            result = re.search(pattern, value)
            if result:
                # print(result)
                datetime_object = datetime.strptime(result.group(), "%d.%m.%Y")
                # print(datetime_object)
            else:
                raise ValueError()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.birthday = None
        self.phones = []

    def add_phone(self, phone_number):
        new_phone = Phone(phone_number)
        self.phones.append(new_phone)

    def add_birthday(self, birthday_date):
        self.birthday = Birthday(birthday_date)

    def remove_phone(self, remove_phone):
        for phone in self.phones:
            if phone.value == remove_phone:
                self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        old_p = Phone(old_phone)
        new_p = Phone(new_phone)

        if not any(old_phone == phone.value for phone in self.phones):
            raise ValueError("The entered number wasn`t found!")

        for phone in self.phones:
            if phone.value == old_p.value:
                phone.value = new_p.value

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
            
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, user_record):
          self.data[user_record.name.value] = user_record

    def find(self, contact_name):
        return self.data.get(contact_name)
    
    def delete(self, contact_name):
        self.data.pop(contact_name)

    def __str__(self):
        return f"Contacts:\n{"\n".join(str(user_data) for user_data in self.data.values())}"


# b_date = Birthday("09.10.1983")

#
# Checking the operation of the program
#
book = AddressBook()
print("---Add users records---")
maks_record = Record("Maks")
print(maks_record)
# miha_record = Record("Miha")
# print(miha_record)
# alex_record = Record("Alex")
# print(alex_record)
# print("---Add users phones---")
# maks_record.add_phone("1234567890")
# maks_record.add_phone("5555555555")
# maks_record.add_phone("5555555556")
# print(maks_record)
maks_record.add_birthday("5555555556")
# maks_record.add_birthday("55.55.5555")
maks_record.add_birthday("14.02.5555")
print(maks_record)

# miha_record.add_phone("5555555557")
# print(miha_record)
# alex_record.add_phone("5555555558")
# print(alex_record)
# print("---Delete user phone number---")
# maks_record.remove_phone("5555555556")
# print(maks_record)
# print("---Edit user phone number---")
# miha_record.edit_phone("5555555557", "7777777777")
# # miha_record.edit_phone("5555555550", "0777777777") # The phone number is missing in contact
# print(miha_record)
# print("---Find user phone number---")
# print(alex_record.find_phone("5555555558"))
# print(maks_record.find_phone("7777777779"))
# print("---Add contacts in the contacts book---")
# book.add_record(maks_record)
# book.add_record(miha_record)
# book.add_record(alex_record)
# print(book)
# print("---Find contacts in the contacts book---")
# print(book.find("Maks"))
# print(book.find("Maks1"))
# print("---Delete contact in the contacts book---")
# book.delete("Miha")
# print(book)