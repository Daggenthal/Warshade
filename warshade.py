import functions

from subprocess import run
from sys import exit

try: 
        while True:

                run(['clear'], shell=True)

                print('\t Welcome to Warshade! What would you like to do? \n')
                print('\t 1: Backup')
                print('\t 2: Transfer Backup')
                print('\t 3: Server Setup')
                print('\t 4: Restore Backup')
                print('\t 5: Exit \n')

                response = input('\t Please input your selection as a number: ')

                run(['clear'], shell=True)

                if response == '1':
                        functions.Backup()
                elif response == '2':
                        functions.transferBackup()
                elif response == '3':
                        functions.serverSetup()
                elif response == '4':
                        functions.restoreBackup()
                elif response == '5':
                        exit()

except KeyboardInterrupt:
        
        run(['clear'], shell=True)

        print('\t User has purposefully interrupted the execution of the program.\n')
