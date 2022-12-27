import functions, argparse


from subprocess import run
from sys import exit

# Here we add CLI arguments for quick-and-easy execution instead of having to go through the menu.

parser = argparse.ArgumentParser()
parser.add_argument("-fb", "--fullBackup", action = "store_true", help = "Backs up the server.\n")
parser.add_argument("-dbb", "--dbBackup", action = "store_true", help = "Backs up the database and timestamps it.\n")
parser.add_argument("-wb", "--webBackup", action = "store_true", help = "Backs up NGINX, Certs, and other important files such as the website NGINX is running.\n")
parser.add_argument("-tb", "--Transfer", action = "store_true", help = "Transfers to a new server.\n")
parser.add_argument("-s", "--Setup", action = "store_true", help = "Installs necessary files for the server. To see what's installed, view 'programs.py'.\n")
parser.add_argument("-fr", "--fullRestore", action = "store_true", help = "This restores the server, putting the files we've backed up, back into their proper directories.\n")
parser.add_argument("-dbr", "--dbRestore", action = "store_true", help = "This allows the user to select a specific .sql database and restore it.\n")
parser.add_argument("-wbr", "--webRestore", action = "store_true", help = "This attempts to restore the NGINX and webBackup that a user selects in the /tmp/ directory.\n")
args = parser.parse_args()

# Here we're checking to see if any CLI arguments were passed before execution. If none were passed, then we follow through with the default state.

try: 
        if args.fullBackup:
                functions.fullBackup()
        elif args.dbBackup:
                functions.dbBackup()
        elif args.webBackup:
                functions.webBackup()
        elif args.Transfer:
                functions.transferBackup()
        elif args.Setup:
                functions.serverSetup()
        elif args.fullRestore:
                functions.fullRestore()
        elif args.dbRestore:
                functions.dbRestore()
        elif args.webRestore:
                functions.webRestore()

        while True:

                run(['clear'], shell=True)

                print('\t Welcome to Warshade! What would you like to do? \n')
                print('\t 1: Full Backup')
                print('\t 2: Database Backup')
                print('\t 3: Website / NGINX Backup\n')
                print('\t 4: Transfer Backup')
                print('\t 5: Server Setup\n')
                print('\t 6: Restore Full Backup')
                print('\t 7: Restore Database')
                print('\t 8: Restore Website\n')
                print('\t 9: Exit \n')

                response = input('\t Please input your selection as a number: ')

                run(['clear'], shell=True)

                if response == '1':
                        functions.fullBackup()
                elif response == '2':
                        functions.dbBackup()
                elif response == '3':
                        functions.webBackup()
                elif response == '4':
                        functions.transferBackup()
                elif response == '5':
                        functions.serverSetup()
                elif response == '6':
                        functions.fullRestore()
                elif response == '7':
                        functions.dbRestore()
                elif response == '8':
                        functions.webRestore()
                elif response == '9':
                        exit()

except KeyboardInterrupt:
        
        run(['clear'], shell=True)

        print('\t User has purposefully interrupted the execution of the program.\n')
