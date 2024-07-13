import subprocess
import os
import time
from colorama import init, Fore, Style
from tabulate import tabulate
import pyfiglet

# Initialize colorama
init(autoreset=True)

# Define color constants
B = Style.BRIGHT
r = Fore.RED
g = Fore.GREEN
b = Fore.BLUE
c = Fore.CYAN
y = Fore.YELLOW
m = Fore.MAGENTA
w = Fore.WHITE

CONTACT_FILE = 'contact.txt'
SLEEP_TIME_ADD = 1.54321
SLEEP_TIME_CALL = 2

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def add_contact():
    name = input(y + 'Enter name: ')
    number = input(y + 'Enter the number: ')

    with open(CONTACT_FILE, 'a') as contact_file:
        contact_file.write(f'{name},{number}\n')
    print(f'{B}{c}Contact adding....')
    time.sleep(SLEEP_TIME_ADD)
    print(f'{B}{g}Contact added successfully')

def remove_contact():
    try:
        with open(CONTACT_FILE, 'r') as contact_file:
            contacts = [line.strip().split(',') for line in contact_file]
    except FileNotFoundError:
        print(f'{B}{r}Contact file not found.')
        return

    print(f'{B}{b}Your current contacts:')
    list_contacts()
    indices = input(f'{B}{y}Enter indices of contacts to delete (e.g., 1 or 1,3,5): ').split(',')
    indices = [int(index.strip()) for index in indices if index.strip().isdigit()]

    if not indices:
        print(f'{B}{r}Invalid input. No contacts deleted.')
        return

    contacts_to_remove = [contacts[index - 1] for index in indices if 0 < index <= len(contacts)]
    if not contacts_to_remove:
        print(f'{B}{r}No valid contacts to delete.')
        return

    print(f'{B}{y}Contacts to delete:')
    print(tabulate(contacts_to_remove, headers=['Name', 'Number'], tablefmt="grid"))

    confirmation = input(f'{B}{y}Are you sure you want to delete these contacts? (yes/no): ').strip().lower()
    if confirmation == 'yes':
        remaining_contacts = [contact for index, contact in enumerate(contacts, start=1) if index not in indices]
        with open(CONTACT_FILE, 'w') as contact_file:
            for name, number in remaining_contacts:
                contact_file.write(f'{name},{number}\n')
        print(f'{B}{g}Contacts deleted successfully.')
    else:
        print(f'{B}{r}Operation aborted.')

def call_contact():
    name = input(y + 'Enter name: ')
    try:
        with open(CONTACT_FILE, 'r') as contact_file:
            contacts = [line.strip().split(',') for line in contact_file]
    except FileNotFoundError:
        print(f'{B}{r}Contact file not found.')
        return

    for contact_name, number in contacts:
        if contact_name == name:
            print(f'{B}{m}Calling {name} with number {number}')
            time.sleep(SLEEP_TIME_CALL)
            subprocess.run(['sh', os.path.join(os.getcwd(), 'call.sh'), number.strip()])
            return
    print(f'{B}{r}Contact not found')

def list_contacts():
    headers = ['___Name', 'Number___']
    data = []
    try:
        with open(CONTACT_FILE, 'r') as contact_file:
            data = [line.strip().split(',') for line in contact_file]
    except FileNotFoundError:
        print(f'{B}{r}Contact file not found.')
        return

    print(f'{m}{tabulate(data, headers=headers, tablefmt="grid")}')

def exit_program():
    print(f'{B}{b}Exiting...')
    exit()

def main():
    actions = {
        1: add_contact,
        2: call_contact,
        3: list_contacts,
        4: remove_contact,
        5: exit_program
    }

    while True:
        try:
            action = int(input(f'{B}{b}Enter action you want to do\n1. Add contact\n2. Call contact\n3. List contact\n4. Remove contact\n5. Exit\n'))
            if action in actions:
                actions[action]()
            else:
                print(f'{B}{r}Invalid action. Please try again.')
        except ValueError:
            print(f'{B}{r}Please enter a valid number.')

if __name__ == '__main__':
    clear()
    # List available fonts
    fonts = pyfiglet.FigletFont.getFonts()
    print(fonts)
    
    # Use a specific font
    f = pyfiglet.Figlet(font='slant')
    ascii_art = f.renderText("Contact")
    clear()
    print(B+c+ascii_art)
    print(B+c+"__________________________by karthi")

    main()
