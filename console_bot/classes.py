from collections import UserDict
from functools import reduce

class NoNumberInContact(Exception):
    pass

class EmptyName(Exception):
    pass

class EmptyNumber(Exception):
    pass

class SameNumber(Exception):
    pass

class Field():
    '''Common field characters'''
    def __init__(self, value) -> None:
        self.value = str(value)
        pass

class Name(Field):
    '''Name characters'''
    def __init__(self, value) -> None:
        if value:
            self.value = value
        else:
            raise EmptyName
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

    def raise_nonumber(func):
        '''
        Decorator to raise exeption if there are no phone 
        with such number in the phones
        '''
        def inner(self, phone, *args, **kwargs):
            if phone.value not in self.get_numbers():
                raise NoNumberInContact
            return func(self, phone, *args, **kwargs)
        return inner
    
    def raise_same_number(func):
        '''
        Decorator to raise exeption if already there is phone 
        with such number in the phones
        '''
        def inner(self, *args, **kwargs):
            phone = args[-1]
            number = phone.value
            if number in self.get_numbers():
                raise SameNumber
            return func(self, *args, **kwargs)
        return inner
    
    def raise_empty_number(func):
        '''Decorator to raise exeption if phone has empty number'''
        def inner(self, *args, **kwargs):
            for phone in args:
                if not phone.value:
                    raise EmptyNumber
            return func(self, *args, **kwargs)
        return inner

    @raise_empty_number
    @raise_same_number
    def add_phone(self, phone: Phone) -> list[Phone]:
        '''Add new phone to phones'''
        self.phones.append(phone)
        return self.phones

    @raise_empty_number
    @raise_nonumber
    def remove_phone(self, phone: Phone) -> list[Phone]:
        '''Remove phone with number from phones'''
        for s_phone in filter(lambda s_phone: s_phone.value == phone.value, self.phones):
            self.phones.remove(s_phone)
        return self.phones
    
    @raise_empty_number
    @raise_nonumber
    @raise_same_number
    def change(self, old_phone: Phone, new_phone: Phone) -> list[Phone]:
        '''Change phone number'''
        for phone in filter(lambda phone: phone.value == old_phone.value, self.phones):
            phone.value = new_phone.value
        return self.phones
    
    def get_numbers(self) -> list[str]:
        '''Return list with numbers'''
        numbers = [phone.value for phone in self.phones]
        return numbers

class AdressBook(UserDict):
    '''Represent adress book with records'''

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




