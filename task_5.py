from functools import wraps
from typing import Callable

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
def add_contact(args: list, contacts: dict):
    if len(args) < 2:
                raise IndexError("Enter the argument for the command!")

    name, phone = args

    if name.isdigit() or not phone.isdigit():
        raise ValueError("Name must contain symbols and phone number only digits!")

    if name in contacts:
        raise KeyError("Entered name is already exist. Change name or use another command to change phone number!")
    
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args: list, contacts: dict):
    if len(args) < 2:
        raise IndexError("You need to provide both name and phone!")

    name, phone = args

    if name.isdigit() or not phone.isdigit():
        raise ValueError("Name must contain symbols and phone number only digits!")

    if name not in contacts:
        raise KeyError("Entered name hasn't find in base!")

    if name in contacts:
        contacts[name] = phone

    return "Contact changed."

@input_error
def show_phone(args: list, contacts: dict):
    if len(args) < 1:
        raise IndexError("You need to provide name!")
    
    name = args[0]

    if name.isdigit():
        raise ValueError("Entered name contain only digits!")

    if name not in contacts:
        raise KeyError("Entered name hasn't find in base!")

    if name in contacts:
        return contacts[name]

@input_error
def show_all(contacts: dict):
    if not contacts:
        raise ValueError("The base is empty!")

    data_str: str = ""

    for key, value in contacts.items():
        data_str += f"Name: {key}, Phone: {value}\n"

    return data_str[0:-1]
    
def main():
    contacts: dict = {}
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
                    print(add_contact(args, contacts))
                case "change":
                    print(change_contact(args, contacts))
                case "phone":
                    print(show_phone(args, contacts))
                case "all":
                    print(show_all(contacts))
                case _:
                    print("Invalid command. You can use this command: add, change, phone, all, close or exit!")
        except ValueError:
            print("Please, enter a command!")

if __name__ == "__main__":
    main()