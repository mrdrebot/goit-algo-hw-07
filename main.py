from functools import wraps
from typing import Callable
from classes_library import AddressBook, Record

def parse_input(user_input: str) -> tuple:
    cmd, *args = user_input.split()
    cmd: str = cmd.strip().lower()
    return cmd, *args

def input_error(func: Callable[[tuple], Callable[[tuple], tuple]]) -> Callable[[tuple], Callable[[tuple], tuple]]:
    @wraps(func)
    def inner(*args: tuple) ->  Callable[[tuple], Callable[[tuple], tuple]]:
        try:
            return func(*args)
        except ValueError as e:
            return f"Error: { e }"
        except KeyError as e:
            return f"Error: { e }"
        except IndexError as e:
            return f"Error: { e }"

    return inner

@input_error
def add_contact(args: list, book: AddressBook):
    if len(args) < 2:
        raise IndexError("Enter the argument for the command!")

    name, phone, *_ = args

    if name.isdigit() or not phone.isdigit():
        raise ValueError("Name must contain symbols and phone number only digits!")

    record = book.find(name)

    if record and record.find_phone(phone):
        raise KeyError("Entered name and number are already exists. Change name or check entered phone number!")

    if record is None:
        record = Record(name)
        book.add_record(record)
        record.add_phone(phone)
        message: str = "Contact added."
    else:
        record.add_phone(phone)
        message: str = "Contact updated."

    return message

@input_error
def change_contact(args: list, book: AddressBook):
    if len(args) < 3:
        raise IndexError("You need to provide both name and phone!")

    name, old_phone, new_phone, *_  = args

    if name.isdigit() or (not old_phone.isdigit() or not new_phone.isdigit()):
        raise ValueError("Name must contain symbols and phone number only digits!")

    record = book.find(name)

    if record is None:
        raise KeyError("Entered name hasn't find in base!")
    else:
        record.edit_phone(old_phone, new_phone)
        return "Contact changed."

@input_error
def show_phone(args: list, book: AddressBook):
    if len(args) < 1:
        raise IndexError("You need to provide name!")
    
    name, *_ = args

    if name.isdigit():
        raise ValueError("Entered name contain only digits!")

    record = book.find(name)

    if record is None:
        raise KeyError("Entered name hasn't find in base!")
    else:
        return record

@input_error
def show_all(book: AddressBook):
    if not book:
        raise ValueError("The base is empty!")

    return book

@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        raise IndexError("Enter the argument for the command!")

    name, birthday, *_ = args

    if name.isdigit():
        raise ValueError("Name must contain symbols and digits!")

    record = book.find(name)

    if record is None:
        raise KeyError("Entered name hasn't find in base!")
    elif record.birthday:
        raise KeyError("The data in field birthday is already exist. Use another command to change birthday date!")
    else:
        record.add_birthday(birthday)
        return "Birthday added." 

@input_error
def show_birthday(args, book: AddressBook):
    if len(args) < 1:
        raise IndexError("You need to provide name!")
    
    name, *_ = args

    if name.isdigit():
        raise ValueError("Entered name contain only digits!")

    record = book.find(name)

    if record is None:
        raise KeyError("Entered name hasn't find in base!")
    else:
        return record.birthday

@input_error
def birthdays(book: AddressBook):
    return book.get_upcoming_birthdays()
    
def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        try:
            user_input: str = input("Enter a command: ")
            command, *args = parse_input(user_input)

            match command:
                case "close" | "exit":
                    print("Good bye!")
                    break
                case "hello":
                    print("How can I help you?")
                case "add":
                    print(add_contact(args, book))
                case "change":
                    print(change_contact(args, book))
                case "phone":
                    print(show_phone(args, book))
                case "add-birthday":
                    print(add_birthday(args, book))
                case "show-birthday":
                    print(show_birthday(args, book))
                case "birthdays":
                    print(birthdays(book))
                case "all":
                    print(show_all(book))
                case _:
                    print("Invalid command. You can use this command: add, change, phone, all, close or exit!")
        except ValueError:
            print("Please, enter a command!")

if __name__ == "__main__":
    main()