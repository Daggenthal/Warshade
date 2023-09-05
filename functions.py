import getpass, os

from subprocess import run
from sys import exit
from time import sleep
from programs import *


def fullBackup():
	while True:
		
		# Cleans up the /tmp/Backup/ directory incase the script was executed without fully completing.

		run(['cd /tmp/ && sudo rm -rf Backup/'], shell=True, check=True)
	
		# Create a temporary directory that will be used throughout the script.

		run(['mkdir /tmp/Backup/ && mkdir /tmp/Backup/etc/ && mkdir /tmp/Backup/usr'], shell=True, check=True)

		run(['clear'], shell=True)

		print('\t Grabbing pv to show pipe progress during compression and decompression...\n')
		
		if distro[0 or 1] in OS:
			run([dpv], shell=True, check=True)
		elif distro[2 or 3] in OS:
			run([fpv], shell=True, check=True)
		elif distro[4] in OS:
			run([apv], shell=True, check=True)
		elif distro[5] in OS:
			run([opv], shell=True, check=True)
		elif distro[6] in OS:
			run([bpv], shell=True, check=True)
		
		print('\t PV has been installed, continuing backup...')

		sleep(3)

		run(['clear'])

		userName = input('\n\t Please input your MariaDB Username: ')
		passWord = getpass.getpass('\n\t Please input your password: ')
		
		run(['clear'], shell=True, check=True)

		# Start the backup process of the mariaDB database.
		
		print('\n\t Backup initiated, this may take a bit and is active, please wait...\n')

		run(['cd /tmp/Backup && mariadb-dump --user=' + userName + ' --password=' + passWord + ' --lock-tables --all-databases > server_db_backup.sql'], shell=True, check=True)

		print('\t Database has been backed up! Backing up /etc/...\n')

		# Starts the backup process of my.cnf, NGINX, apache(HTTPD), and postfix for the mail system / SendGrid settings, then moves them in the tmp directory.

		run(['cp /etc/my.cnf /tmp/Backup/etc/'], shell=True, check=True)
		run(['cp /etc/php.ini /tmp/Backup/etc/'], shell=True, check=True)
		run(['sudo cp -r /etc/nginx/ /tmp/Backup/etc/'], shell=True, check=True)
		run(['sudo cp -r /etc/postfix/ /tmp/Backup/etc/'], shell=True, check=True)
		
		# Starts the backup process of the letsencrypt certs for the website's SSL

		run(['sudo cp -r /etc/letsencrypt/ /tmp/Backup/etc/'], shell=True, check=True)

		print('\t /etc/ has been backed up! Backing up the website...\n')

		# Starts the backup process of the website, and its included files. This may take long depending on what's in there.

		run(['sudo cp -r /usr/share/nginx/ /tmp/Backup/usr/'], shell=True, check=True)

		print('\t The website has been backed up! Compressing files...\n\t')

		# Dates and compresses the /tmp/Backup/ folder for RSYNC later on, then removes the temporary /tmp/Backup/ folder.

		run(["""cd /tmp/ && sudo tar -zcvf "$(date '+%Y-%m-%d').tar.gz" /tmp/Backup/"""], shell=True, check=True)

		run(['cd /tmp/ && sudo rm -rf Backup/'], shell=True, check=True)

		print('\n\t Backup has been completed, would you like to return to the main menu?\n')
		print('\t 1: Yes')
		print('\t 2: No\n')

		response = input('\t Please input your selection: ')

		if response == '1':
			break
		elif response == '2':
			run(['clear'], shell=True)
			exit()




def dbBackup():
	while True:

		# Clear the terminal for our next output

		run(['clear'], shell=True)

		# Print on the screen that the backup is being initiated

		print('\n\t MariaDB backup initiated...')

		# Ask for the Username and Password, storing those into 2 variables we've aptly created.

		userName = input('\n\t Please input your MariaDB Username: ')
		passWord = getpass.getpass('\n\t Please input your password: ')

		# Print out that we are initializing the backup, and tell the user where it will be located.

		print('\n\t The DB backup will be stored in /tmp/\n\t Please wait, as depending on the size of the DB, this may seem inactive...')
		sleep(1.25)

		# Use the information we've gathered earlier, and CD into the specific user directory that this is being ran inside of. If we did this in /tmp/, we'd have to make a folder there and constantly check for it.
		# Instead, we're just storing it in their /Documents/ folder, as that is >typically< created upon user account creation.
		# We finalzie this process by tagging the Year, Month, and Day of DB creation so we can select which one to recover from later.
		
		run(["cd /tmp/ && mariadb-dump --user=" + userName + " --password=" + passWord + " --lock-tables --all-databases > $(date '+%Y-%m-%d').sql"], shell=True, check=True)

		# Clear the screen upon completion, and tell the user that it has finished successfully.

		run(["clear"], shell=True)
		print('\n\t The Database was successfully backed up. The default location is in /home/$USER/Documents/')
		exit()




def dbRestore():
	while True:

		# Clear the terminal.

		run(['clear'], shell=True)

		print('Scanning the /tmp/ directory for any databases...')
		sleep(1)
		run(['clear'], shell=True)
		
		# Now we will search the specified location for .sql files, and if none are found, exit. If they are found, allow the user to select them and restore the database with it.

		while True:

			try:

				# Get the list of files inside the /home/$USER/Documents/ directory

				files = os.listdir('/tmp/')

				# Print out a numbered list of files

				for index, file in enumerate(files):
					
					if file.endswith(".sql"):
						print(f"{index+1}. {file}\n")

				# Get the user's input

				selection = int(input('Enter the number of the file you wish to select: '))

				# Check if the selection is valid

				if selection > 0 and selection <= len(files):
					
					# Get the file name

					output_file = files[selection-1]
					
				else:
					print("Invalid selection")
				
				# Grab the DB Username we will use to force the DB to be restored.

				userName = input('\n\t Please input your MariaDB Username: ')

				# Force the restoration by inputting the username, asking a password, and pushing through the file we've selected.
				
				run(['sudo mysql --user ' + userName + ' --password --force < ' + output_file], shell=True, check=True)

				# Clear the shell and print out that it was successful.

				run(['clear'], shell=True)

				print('\n\t The Database was properly restored! Exiting now...')
				sleep(1.5)
				exit()

			except:

				# Clear the terminal.

				run(['clear'], shell=True)

				# Tell the user that nothing was found.

				print('\n\t No files with the .sql extension were -\n\t - found in /tmp/, or the program was exited.\n')
				exit()




def webBackup():
	while True:

		# Clears the terminal, creates a directory for where we'll store our website backup, then we'll tar the directories and move them into /home/$USER/Documents while being timestamped.

		run(['clear'], shell=True)
	
		# Cleans up the /tmp/Backup/ directory incase the script was executed without fully completing.

		run(['cd /tmp/ && sudo rm -rf Backup/'], shell=True, check=True)
	
		# Create a temporary directory that will be used throughout the script.

		run(['mkdir /tmp/Backup/ && mkdir /tmp/Backup/etc/ && mkdir /tmp/Backup/usr'], shell=True, check=True)
		
		# Starts the backup process of my.cnf, NGINX, apache(HTTPD), and postfix for the mail system / SendGrid settings, then moves them in the tmp directory.

		run(['cp /etc/my.cnf /tmp/Backup/etc/'], shell=True, check=True)
		run(['cp /etc/php.ini /tmp/Backup/etc/'], shell=True, check=True)
		run(['sudo cp -r /etc/nginx/ /tmp/Backup/etc/'], shell=True, check=True)
		run(['sudo cp -r /etc/postfix/ /tmp/Backup/etc/'], shell=True, check=True)
		
		# Starts the backup process of the letsencrypt certs for the website's SSL

		run(['sudo cp -r /etc/letsencrypt/ /tmp/Backup/etc/'], shell=True, check=True)

		print('\t /etc/ has been backed up! Backing up the website...\n')

		# Starts the backup process of the website, and its included files. This may take long depending on what's in there.

		run(['sudo cp -r /usr/share/nginx/ /tmp/Backup/usr/'], shell=True, check=True)

		print('\t The website has been backed up! Compressing files...\n\t')

		# Dates and compresses the /tmp/Backup/ folder for RSYNC later on, then removes the temporary /tmp/Backup/ folder.

		run(["""cd /tmp/ && sudo tar -zcvf "$(date '+%Y-%m-%d')_webBackup.tar.gz" /tmp/Backup/"""], shell=True, check=True)

		# Moves the folder we've created to the /tmp/ directory to be cleared whenever the server is rebooted, or when /tmp/ is usually cleared.

		run(['cd /tmp/ && sudo rm -rf Backup/'])

		# Clear the terminal and tell the user that the operation finished.

		run(['clear'], shell=True)

		print('\n\t The Website and its subdirectories have been fully backed up, and are located inside /home/$USER/Documents')
		print('\n\t Exiting program...')
		sleep(1.5)
		exit()




def webRestore():
	while True:

		# This function lists the users Website backups that are located in /home/$USER/Documents/ and allows them to restore NGINX, the website, and all required files to be fully operational.

		run(['clear'], shell=True)
		print('\n\t Scanning the /tmp/ directory for files...')
		sleep(1)
		run(['clear'], shell=True)

		try:

			# Get the list of files inside the /tmp/ directory

			files = os.listdir('/tmp/')

			# Print out a numbered list of files

			for index, file in enumerate(files):
				
				if file.endswith("_webBackup.tar.gz"):
					print(f"{index+1}. {file}\n")

			# Get the user's input

			selection = int(input('Enter the number of the file you wish to select: '))

			# Check if the selection is valid

			if selection > 0 and selection <= len(files):
				
				# Get the file name

				output_file = files[selection-1]
				
			else:
				print("Invalid selection")

			# Clear the screen and tell the user that a file was selected, and that the operation will begin.

			run(['clear'], shell=True)
			print('\n\t Website Backup file has been selected, attempting restoration...')

			# Here we're going to disable the services while we attempt to restore them.

			print('\t Disabling services momentarily...\n\t')
			sleep(1.25)


			if distro[0 or 1 or 2 or 3 or 4 or 5] in OS:

				run(['sudo systemctl stop nginx postfix mariadb memcached.service'], shell=True, check=True)

			# Turns out that in FreeBSD, services aren't auto-started once installed. Here, we enable to start on boot, but for now they'll stay turned off.
			# Later on we'll actually start these.

			elif distro[6] in OS:

				run(['sudo sysrc nginx_enable=YES'], shell=True, check=True)
				run(['sudo sysrc postfix_enable=YES'], shell=True, check=True)
				run(['sudo sysrc mysql_enable=YES'], shell=True, check=True)
				run(['sudo sysrc memcached_enable=YES'], shell=True, check=True)
				run(['clear'], shell=True, check=True)


			print('\t Services have successfully been disabled. Attempting restoration, please wait...\n\t')
			sleep(1.25)

			# Here we're beginning to decompress the file we created, and moved, earlier. This contains everything we need to properly setup the new server.

			print('\t Attempting to decompress the file, please wait...\n\t')
			sleep(2)

			run(['cd /tmp/ && sudo pv ' + output_file + ' | tar -xz'], shell=True, check=True)
			sleep(3)
			run(['clear'], shell=True)

			print('\t The file has successfully been decompressed! Attempting restore...\n\t')
			sleep(1.25)

			# Here we're going to move the files to the proper directory that they came from.

			if distro[0 or 1 or 2 or 3 or 4 or 5] in OS:

				run(['cd /tmp/tmp/Backup/etc && sudo rsync -avr * /etc/'], shell=True, check=True)

			elif distro[6] in OS:

				run(['cd /tmp/tmp/Backup/etc/ && sudo cp my.cnf /usr/local/etc/mysql/'], shell=True, check=True)
				run(['cd /tmp/tmp/Backup/etc/ && sudo cp php.ini /usr/local/etc/'], shell=True, check=True)

				# You may ask yourself why we're moving the directories out. Errors are thrown that the directories already exist, so we're moving them!
				# Sure, we can use -f to force the mv into the directory, but moving them to /tmp/ is cleaner, as later on we enable /tmp/ to be autocleared upon reboot.

				run(['cd /usr/local/etc/ && sudo mv nginx/ /tmp/'], shell=True, check=True)
				run(['cd /usr/local/etc/ && sudo mv postfix /tmp/'], shell=True, check=True)

				# Now we'll finally move the directories that we want, back into their proper homes!

				run(['cd /tmp/tmp/Backup/etc && sudo rsync -avr nginx/ postfix/ localhost:/usr/local/etc/'], shell=True, check=True)
			
			print('\t /etc/ folders have successfully been restored! Attempting website restore...\n\t')
			sleep(1.25)

			# Now we're going to move the website and mail certs back to their origin.
			# We move the folder that's created by nginx, to the /tmp/ directory, so we can install our own copy.

			if distro[0 or 1 or 2 or 3 or 4 or 5] in OS:

				run(['cd /tmp/tmp/Backup/usr && sudo rsync -avr nginx/ /usr/share/'])

			elif distro[6] in OS:

				run(['sudo mkdir /tmp/holding/'], shell=True, check=True)
				run(['cd /usr/local/www/ && sudo rm -rf nginx/'], shell=True, check=True)
				run(['cd /tmp/tmp/Backup/usr/ && sudo mv nginx/ /usr/local/www/'], shell=True, check=True)

			print('\t Website has successfully been restored! Attempting API key restore...\n\t')
			sleep(1.25)

			# Now we're going to setup postfix so we can use the same API keys

			if distro[0 or 1 or 2 or 3 or 4 or 5] in OS:

				run(['sudo postmap /etc/postfix/sasl_passwd'], shell=True, check=True)

			elif distro[6] in OS:

				# We need to create the group postdrop, and then give them postfix permissions.

				run(['sudo pw groupadd postdrop && sudo postfix set-permissions'], shell=True, check=True)

				# Now we can properly set the main.cf file for our usage.

				run(['sudo postmap /usr/local/etc/postfix/sasl_passwd'], shell=True, check=True)

			print('\t API keys have been successfully restored! Attempting SSL certs restore...\n')
			sleep(1.25)

			# Now we're going to restore the letsencrypt SSL certificates for the website.
			
			if distro[0 or 1 or 2 or 3 or 4 or 5] in OS:

				sleep(0.25)

			elif distro[6] in OS:

				run(['cd /usr/local/etc/ && sudo mv letsencrypt/ /tmp/holding/'], shell=True, check=True)
				run(['cd /tmp/tmp/Backup/etc && sudo mv letsencrypt/ /usr/local/etc/'], shell=True, check=True)

			print('\t SSL certs have successfully been restored!\n\t')
			sleep(1.25)

			# Now we'll start the services again, and enable them to persist upon reboot.

			print('\n\t Starting services, and enabling them for future reboots, please wait...\n')

			if distro[0 or 1 or 2 or 3 or 4 or 5] in OS:

				run(['sudo systemctl start nginx postfix mariadb memcached.service && sudo systemctl enable nginx postfix mariadb memcached.service'], shell=True, check=True)

			elif distro[6] in OS:

				run(['sudo service nginx postfix mysql-server memcached start'], shell=True, check=True)

				# This line right here adds 'weekly_certbot_enable="YES"' to a file that we create, so certbot is checked weekly.
				# We're also disabling sendmail, eventhough it's not present, due to enabling postfix prior in this script.

				run(["""sudo touch /etc/periodic.conf && sudo echo 'weekly_certbot_enable="YES"' >> /etc/periodic.conf """], shell=True, check=True)
				run(["""sudo echo 'sendmail_enable="NONE"' >> /etc/periodic.conf """], shell=True, check=True)
				run(["""sudo echo 'clear_tmp_enable="YES" >> /etc/rc.conf"""], shell=True, check=True)

		except:

			run(['clear'], shell=True)
			print('\n\t No _website.tar.gz files were located in /tmp/, or the user exited the program, aborting...')
			sleep(5)
			exit()




def transferBackup():
	while True:

		# This clears the terminal, and attempts to RSYNC the previously .tar.gz file we created earlier, and attempts to send it to the new one.

		run(['clear'], shell=True)

		# Here we're storing the target userName, and ipAddress, for the server where our file will be rsync'd to.
		# These will be called later on.

		userName = input('\n\t Please input the target username: ')
		ipAddress = input('\n\t Please input the target IP Address: ')

		run(['clear'], shell=True)

		print('\n\t Are these correct?')
		print('\n\t Username: ', userName)
		print('\t IP Address: ', ipAddress, '\n')


		print('\t 1: Yes')
		print('\t 2: No\n')

		response = input('\t Please input your selection: ')

		if response == '1':

			run(['clear'], shell=True)

			# Get the list of files inside the /tmp/ directory.

			files = os.listdir('/tmp/')

			# Print out a numbered list of files that we scan for.

			try:

				for index, file in enumerate(files):
					
					if file.endswith('.tar.gz'):
						print(f"{index+1}. {file}\n")

			except:

				print("\n\tNo files with the extension of '.tar.gz' exists in /tmp/\n Please check it or move files there. Exiting now...\n")
				sleep(2.5)
				exit()
				
			# Get the user's input

			selection = int(input('Enter the number of the file you wish to select: '))

			# Check if the selection is valid

			if selection > 0 and selection <= len(files):
				
				# Get the file name

				output_file = files[selection-1]
				
			else:
				print("Invalid selection")

			# Now we're going to RSYNC our selected file to the destination that we've chosen earlier.

			run(['cd /tmp/ && sudo rsync -av -P ' + output_file + ' ' + userName + '@' + ipAddress + ':/tmp/'], shell=True, check=True)

			print('\t Rsync was successful! Would you like to return to the main menu?\n')
			print('\t 1: Yes')
			print('\t 2: No\n')

			response = input('\t Please input your selection: ')

			if response == '1':
				break
			
			elif response == '2':
				run(['clear'], shell=True)
				exit()
				
		elif response == '2':
			run(['clear'], shell=True)
			print('\n\t Returning to main menu...')
			sleep(1.25)
			break




def serverSetup():
	while True:
		
		run(['clear'], shell=True)
		
		# Here we're installing the necessary programs that we'll be using for later on. These are *required* for the restoreBackup() function to properly work.
		# What we're doing now is checking the users Linux distribution with 'cat /etc/os-release', and reading the output while scanning for key words, then executing what's needed.

		if distro[0 or 1] in OS:
			run([debian], shell=True, check=True)
		elif distro[2] in OS:
			run([fedora], shell=True, check=True)
		elif distro[3] in OS:
			run([rocky], shell=True, check=True)
		elif distro[4] in OS:
			run([arch], shell=True, check=True)
		elif distro[5] in OS:
			run([opensuse], shell=True, check=True)
		elif distro[6] in OS:
			run([freebsd], shell=True, check=True)
		
		run(['clear'], shell=True)
		print('\n\t The prerequisites have been installed! Would you like to return to the main menu?\n')
		print('\t 1: Yes')
		print('\t 2: No\n')

		response = input('\t Please input your selection: ')

		if response == '1':
			break
		elif response == '2':
			run(['clear'], shell=True)
			exit()




def fullRestore():
	while True:

		# This CD's into /tmp/ and untar's our .tar.gz that we created earlier.
		# Please, make sure that you're in the proper folder in order for this to work.

		run(['clear'], shell=True)
		
		# Here we're going to disable the services while we attempt to restore them.

		print('\t Disabling services momentarily...\n\t')
		sleep(1.25)


		if distro[0 or 1 or 2 or 3 or 4 or 5] in OS:

			run(['sudo systemctl stop nginx postfix mariadb memcached.service'], shell=True, check=True)

		# Turns out that in FreeBSD, services aren't auto-started once installed. Here, we enable to start on boot, but for now they'll stay turned off.
		# Later on we'll actually start these.

		elif distro[6] in OS:

			run(['sudo sysrc nginx_enable=YES'], shell=True, check=True)
			run(['sudo sysrc postfix_enable=YES'], shell=True, check=True)
			run(['sudo sysrc mysql_enable=YES'], shell=True, check=True)
			run(['sudo sysrc memcached_enable=YES'], shell=True, check=True)
			run(['clear'], shell=True, check=True)


		print('\t Services have successfully been disabled. Attempting restoration, please wait...\n\t')
		sleep(1.25)


		# Get the list of files inside the /tmp/ directory
		files = os.listdir('/tmp/')

		# Print out a numbered list of files
		for index, file in enumerate(files):
			
			if file.endswith(".tar.gz"):
				print(f"{index+1}. {file}\n")

		# Get the user's input
		selection = int(input('Enter the number of the file you wish to select: '))

		# Check if the selection is valid
		if selection > 0 and selection <= len(files):
			
			# Get the file name
			output_file = files[selection-1]
			
		else:
			print("Invalid selection")

		# Here we're beginning to decompress the file we created, and moved, earlier. This contains everything we need to properly setup the new server.

		print('\t Attempting to decompress the file, please wait...\n\t')
		sleep(2)

		run(['cd /tmp/ && sudo pv ' + output_file + ' | tar -xz'], shell=True, check=True)
		sleep(3)
		run(['clear'], shell=True)

		print('\t The file has successfully been decompressed! Attempting restore...\n\t')
		sleep(1.25)

		# Here we're going to move the files to the proper directory that they came from.

		if distro[0 or 1 or 2 or 3 or 4 or 5] in OS:

			run(['cd /tmp/tmp/Backup/etc && sudo rsync -avr * /etc/'], shell=True, check=True)

		elif distro[6] in OS:

			run(['cd /tmp/tmp/Backup/etc/ && sudo cp my.cnf /usr/local/etc/mysql/'], shell=True, check=True)
			run(['cd /tmp/tmp/Backup/etc/ && sudo cp php.ini /usr/local/etc/'], shell=True, check=True)

			# You may ask yourself why we're moving the directories out. Errors are thrown that the directories already exist, so we're moving them!
			# Sure, we can use -f to force the mv into the directory, but moving them to /tmp/ is cleaner, as later on we enable /tmp/ to be autocleared upon reboot.

			run(['cd /usr/local/etc/ && sudo mv nginx/ /tmp/'], shell=True, check=True)
			run(['cd /usr/local/etc/ && sudo mv postfix /tmp/'], shell=True, check=True)

			# Now we'll finally move the directories that we want, back into their proper homes!

			run(['cd /tmp/tmp/Backup/etc && sudo rsync -avr nginx/ postfix/ localhost:/usr/local/etc'])
		
		print('\t /etc/ folders have successfully been restored! Attempting website restore...\n\t')
		sleep(1.25)

		# Now we're going to move the website and mail certs back to their origin.

		if distro[0 or 1 or 2 or 3 or 4 or 5] in OS:

			run(['cd /tmp/tmp/Backup/usr && sudo rsync -avr nginx/ /usr/share'], shell=True, check=True)

		elif distro[6] in OS:

			run(['sudo mkdir /tmp/holding/'], shell=True, check=True)
			run(['cd /tmp/tmp/Backup/usr/ && sudo rsync -avr nginx/ /usr/local/www/'], shell=True, check=True)

		print('\t Website has successfully been restored! Attempting API key restore...\n\t')
		sleep(1.25)

		# Now we're going to setup postfix so we can use the same API keys

		if distro[0 or 1 or 2 or 3 or 4 or 5] in OS:

			run(['sudo postmap /etc/postfix/sasl_passwd'], shell=True, check=True)

		elif distro[6] in OS:

			# We need to create the group postdrop, and then give them postfix permissions.

			run(['sudo pw groupadd postdrop && sudo postfix set-permissions'], shell=True, check=True)

			# Now we can properly set the main.cf file for our usage.

			run(['sudo postmap /usr/local/etc/postfix/sasl_passwd'], shell=True, check=True)

		print('\t API keys have been successfully restored! Attempting SSL certs restore...\n')
		sleep(1.25)

		# Now we're going to restore the letsencrypt SSL certificates for the website.
		
		if distro[0 or 1 or 2 or 3 or 4 or 5] in OS:

			sleep(0.25)

		elif distro[6] in OS:

			run(['cd /tmp/tmp/Backup/etc && sudo rsync -avr letsencrypt/ /usr/local/etc/'], shell=True, check=True)

		print('\t SSL certs have successfully been restored!\n\t')
		sleep(1.25)

		# Now we'll start the services again, and enable them to persist upon reboot.

		print('\n\t Starting services, and enabling them for future reboots, please wait...\n')

		if distro[0 or 1 or 2 or 3 or 4 or 5] in OS:

			run(['sudo systemctl start nginx postfix mariadb memcached.service && sudo systemctl enable nginx postfix mariadb memcached.service'], shell=True, check=True)

		elif distro[6] in OS:

			run(['sudo service nginx postfix mysql-server memcached start'], shell=True, check=True)

			# This line right here adds 'weekly_certbot_enable="YES"' to a file that we create, so certbot is checked weekly.
			# We're also disabling sendmail, eventhough it's not present, due to enabling postfix prior in this script.

			run(["""sudo touch /etc/periodic.conf && sudo echo 'weekly_certbot_enable="YES"' >> /etc/periodic.conf """], shell=True, check=True)
			run(["""sudo echo 'sendmail_enable="NONE"' >> /etc/periodic.conf """], shell=True, check=True)
			run(["""sudo echo 'clear_tmp_enable="YES" >> /etc/rc.conf"""], shell=True, check=True)

		
		print('\n\t Services have successfully been enabled! Configuring the database...\n')


		print('\n\t Have you already setup MariaDB?\n')
		print('\t 1: Yes')
		print('\t 2: No\n')

		response = input('\t Please input your selection: ')

		if response == '1':

			userName = input('\n\t Please enter your mariaDB username: ')

			print('\n\t Attempting mariaDB / mySQL Database restoration, please wait... ')

			run(['sudo mysql --user ' + userName + ' --password --force < /tmp/tmp/Backup/server_db_backup.sql'], shell=True, check=True)

			print('\n\t Database restoration was successful! Completing restoration, please wait... ')

			sleep(1.25)
			
		elif response == '2':

			print('\n\t Would you like to go ahead and setup MariaDB?\n')
			print('\t 1: Yes')
			print('\t 2: No\n')

			response = input('\t Please input your selection: ')

			if response == '1':

				run(['sudo mariadb-secure-installation'], shell=True, check=True)

				userName = input('\n\t Please enter your mariaDB username: ')

				print('\n\t Attempting mariaDB / mySQL Database restoration, please wait... ')

				run(['sudo mysql --user ' + userName + ' --password --force < /tmp/tmp/Backup/server_db_backup.sql'], shell=True, check=True)

				print('\n\t Database restoration was successful! Going back to main menu...')

				sleep(4)
				break
			elif response == '2':

				print('\n\t Please note, that you may need to manually\n\t setup the DB for it to properly function.')
				print('\n\n\t Restoration complete! Going back to main menu...')

				sleep(4)
				break
