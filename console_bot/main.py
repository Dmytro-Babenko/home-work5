import re
import handlers

OPERATIONS = {
    'hello': handlers.hello,
    'add': handlers.adding,
    'change': handlers.changing,
    'phone': handlers.get_phones,
    'show all': handlers.show_all,
    'remove contact': handlers.remove_contact,
    'remove phone': handlers.remove_phone,
    'close': handlers.good_bye,
    'good bye': handlers.good_bye,
    'exit':handlers.good_bye,
}

COMMAND_WORDS = '|'.join(OPERATIONS)

def parser(message: str) -> tuple[str|None, str|None, str|None]:
    '''
    Parse message to command, name and number.
    command: one of the COMMAND_WORD at the beginning
    new_number: didgits at the end of the message after space
    old_namber: didgits before new number after space
    name: all symbols between command and number
    '''
    command, name, old_number, new_number = '', '', '', ''
    message = message.strip()
    command_match = re.search(fr'^{COMMAND_WORDS}', message, re.IGNORECASE)
    if command_match:
        command = command_match.group()
        message = re.sub(command, '', message)
        command = command.lower()

    message = message.strip()
    new_number_match = re.search(fr' (\d+)$', message)
    if new_number_match:
        new_number = new_number_match.group(1).strip()
        message = re.sub(new_number, '', message)

    message = message.strip()
    old_number_match = re.search(fr' (\d+)$', message)
    if old_number_match:
        old_number = old_number_match.group(1).strip()
        message = re.sub(old_number, '', message)

    name = message.strip()
    return command, name, new_number, old_number 


def main():
    contacts = handlers.address_book
    while True:
        inp = input('Write your command: ')
        command, name, new_number, old_number  = parser(inp)
        try:
            hendler = OPERATIONS[command]
        except KeyError:
            print('There are no command')
            continue
        output = hendler(name, new_number, old_number)
        if output == 'Good bye':
            break
    return contacts

if __name__ == '__main__':
    main()

