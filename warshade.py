import functions, argparse


from subprocess import run
from sys import exit

# Here we add CLI arguments for quick-and-easy execution instead of having to go through the menu.

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--Backup", action = "store_true", help = "Backs up the server.\n")
parser.add_argument("-tb", "--Transfer", action = "store_true", help = "Transfers to a new server.\n")
parser.add_argument("-s", "--Setup", action = "store_true", help = "Installs necessary files for the server. To see what's installed, view 'programs.py'.\n")
parser.add_argument("-r", "--Restore", action = "store_true", help = "This restores the server, putting the files we've backed up, back into their proper directories.\n")
args = parser.parse_args()

# Here we're checking to see if any CLI arguments were passed before execution. If none were passed, then we follow through with the default state.

try: 
        if args.Backup:
                functions.Backup()
        elif args.Transfer:
                functions.transferBackup()
        elif args.Setup:
                functions.serverSetup()
        elif args.Restore:
                functions.restoreBackup()

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
