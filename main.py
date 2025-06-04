from collections import UserDict
from datetime import datetime,timedelta

class PhoneError(Exception):
     pass

class Field:
    def __init__(self, value):
        self.value = value


    def __str__(self):
        return str(self.value)


class Birthday(Field):
    def __init__(self, value):
        try:
            value = datetime.strptime(value,"%d.%m.%Y")
            super().__init__(value.date().strftime("%d.%m.%Y"))
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Name(Field):
    def __init__(self, value):
          super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if len(value)==10 and value.isdigit():
            super().__init__(value)
        else:
            raise PhoneError("The phone number is of incorrect length or contains non-numeric characters.")
    

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None


    def add_phone(self,phone):
         self.phones.append(Phone(phone))


    def add_birthday(self,birhday):
        self.birthday = Birthday(birhday)


    def remove_phone(self,phone):
        self.phones = [phones for phones in self.phones if phones.value != phone]


    def edit_phone(self,old_phone,new_phone):
        if Phone(new_phone):
            for phone in self.phones:
                if phone.value == old_phone:
                    phone.value = new_phone
                    break
            else:
                raise ValueError


    def find_phone(self,phone):
        for phone_find in self.phones:
            if phone_find.value == phone:
                return phone_find
        else:
            return None


    def __str__(self):
        birthday = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}{birthday}"

class AddressBook(UserDict):
    def add_record(self, record:Record):
        self.data[record.name.value] = record


    def find(self,name):
        return self.data.get(name)
    

    def delete(self,name):
        self.data.pop(name)
    

    def get_upcoming_birthdays(self):
        day_now = datetime.now().date()
        list_birthday = []
        for key,record in self.data.items():
            if not record.birthday:
                continue
            birthday_dt = datetime.strptime(record.birthday.value,"%d.%m.%Y").date()
            birthday_now = birthday_dt.replace(year=day_now.year)
            diff = (birthday_now - day_now).days
            if 0 <= diff <= 7:
                if birthday_now.weekday() == 5:
                    birthday_now = birthday_now + timedelta(days=2)
                elif birthday_now.weekday() == 6:
                    birthday_now = birthday_now + timedelta(days=1)
                list_birthday.append({"name":key,
                                      "birthday":datetime.strftime(birthday_now,"%d.%m.%Y")})
        return list_birthday
    

    def __str__(self):
        return "\n".join(str(value) for value in self.data.values())

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter the argument for the command"
        except KeyError:
            return "Enter a correct argument"
        except AttributeError:
            return "Required information is missing"
    return inner
    
            
@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book:AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args,book:AddressBook):
    name,old_phone,new_phone,*_ = args
    record = book.find(name)
    message = "Contact change"
    record.edit_phone(old_phone,new_phone)
    return message


@input_error
def show_phone(args,book:AddressBook):
    name,*_ = args
    record = book.find(name)
    return record


def show_all(book:AddressBook):
    return book


@input_error
def add_birthday(args, book:AddressBook):
    name,birthday,*_ = args
    record = book.find(name)
    record.add_birthday(birthday)
    message = "Birthday add"
    return message


@input_error
def show_birthday(args, book:AddressBook):
    name, *_ = args
    record = book.find(name)
    if record.birthday:
        return record.birthday.value
    else:
        return "No birthday set for this contact"


@input_error
def birthdays(args, book:AddressBook):
    return "\n".join(" ".join(value for value in info.values())for info in book.get_upcoming_birthdays())


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args,book))

        elif command == "change":
            print(change_contact(args,book))

        elif command == "phone":
            print(show_phone(args,book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args,book))

        elif command == "show-birthday":
            print(show_birthday(args,book))

        elif command == "birthdays":
            print(birthdays(args,book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
