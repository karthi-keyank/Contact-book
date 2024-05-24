from tabulate import tabulate
import subprocess
import time
import re
import os

B = '\033[1m'  # Bright
r = '\033[31m' # Red
g = '\033[32m' # Green
b = '\033[34m' # Blue
c = '\033[36m' # Cyan
y = '\033[33m' # Yellow
m = '\033[35m' # Magenta
w = '\033[37m' # White
reset = '\033[0m'  # Reset

def clear():
    subprocess.call('clear','&&','cls', shell=True)

def main():
    while True:
        action = int(input(B+b+"Enter action you want to do\n1. Add contact\n2. Call contact\n3. List contact\n4. Exit\n"))
        if action == 1:
            name, number = input(y+'Enter name: '), input(y+'Enter the number: ')
            with open('contact.txt', 'a') as contact:
                contact.write(f'{name},{number}\n')
            print(B+c+'Contact adding....')
            time.sleep(1.54321)
            print(B+g+'Contact added successfully')
        elif action == 2:
            name = input(y+'Enter name: ')
            with open('contact.txt', 'r') as contact:
                for line in contact:
                    if name in line:
                        _, number = line.strip().split(',')
                        print(B+m+f'Calling {name} with number {number}')
                        time.sleep(2)
                        subprocess.run(['sh', os.path.join(os.getcwd(), 'call.sh'), number.strip()])
                        break
                else:
                    print(B+r+'Contact not found')
        elif action == 3:
            headers = ['_'*3+'Name', 'Number'+'_'*3]
            data=[]
            with open('contact.txt', 'r') as contact:
                for line in contact:
                    name, number = line.strip().split(',')
                    data.append([name,number])
            print(m+tabulate(data, headers=headers, tablefmt="grid"))            
        else:
            print(b+"Exiting........")
            time.sleep(1.0)
            exit()

if __name__ == '__main__':
    main()
