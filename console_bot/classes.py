from collections import UserDict
from functools import reduce

class NoNumberInContact(Exception):
    pass

class Field():
    '''Common field characters'''
    def __init__(self, value) -> None:
        self.value = str(value)
        pass

class Name(Field):
    '''Name characters'''
    def __init__(self, value) -> None:
        super().__init__(value)
        pass

class Phone(Field):
    '''Phone characters'''
    def __init__(self, value) -> None:
        super().__init__(value)
        pass

class Record():
    '''Represent record with fields'''
    def __init__(self, name, *phones):
        self.name = name
        self.phones = [phone for phone in filter(lambda phone: phone.value.isdigit(), phones)]

    def add_phone(self, phone: Phone) -> list[Phone]:
        '''Add new phone to phones'''
        self.phones.append(phone)
        return self.phones
    
    def raise_nonumber(func):
        '''
        Decorator to raise exeption if there are no phone 
        with such number in the phones
        '''
        def inner(self, number, *args, **kwargs):
            if number not in self.get_numbers():
                raise NoNumberInContact
            return func(self, number, *args, **kwargs)
        return inner

    @raise_nonumber
    def remove_phone(self, number: str) -> list[Phone]:
        '''Remove phone with number from phones'''
        for phone in filter(lambda phone: phone.value == number, self.phones):
            self.phones.remove(phone)
        return self.phones
    
    @raise_nonumber
    def change(self, old_number: str, new_number: str) -> list[Phone]:
        '''Change phone number'''
        for phone in filter(lambda phone: phone.value == old_number, self.phones):
            phone.value = new_number
        return self.phones
    
    def get_numbers(self) -> list[str]:
        '''Return list with numbers'''
        numbers = [phone.value for phone in self.phones]
        return numbers

class AdressBook(UserDict):
    '''Represent adress book with records'''
    def __init__(self, data={}):
        self.data = data
        pass

    def add_record(self, record: Record) -> dict[str:Record]:
        '''Add new record to the adress book'''
        key = record.name.value
        self.data[key] = record
        return self.data
    
    def show_records(self) -> str:
        '''Show all records in the adress book data'''
        if not self.data:
            return 'There are no contacts in list'
        output = reduce(lambda s, t: '\n'.join((s, f'{t[0]}: {t[1].get_numbers()}')), 
                        self.data.items(), 'Yor contacts:')
        return output








