import getpass

from subprocess import run
from sys import exit
from time import sleep
from programs import OS, distro, debian, fedora, rocky, arch, opensuse, freebsd
from programs import dpv, fpv, apv, opv, bpv




def Backup():
	while True:

			# Create a temporary directory that will be used throughout the script.

			run(['mkdir /tmp/Backup/ && mkdir /tmp/Backup/etc/ && mkdir /tmp/Backup/usr'], shell=True, check=True)

			print('\n\t NGINX settings, Apache, the mariaDB database, letsencrypt SSL certs, \n\t and the postfix configs will be backed up.\n')
			print('\t Is this something you wanted to do?\n')
			print('\t 1: Yes')
			print('\t 2: No\n')

			response = input('\t Please input your selection: ')

			if response == '1':

				run(['clear'], shell=True)

				print('\t Grabbing pv to show pipe progress during compression and decompression...\n')
				
				if distro[0 or 1] in OS:
					run([dpv], shell=True, check=True)
				elif distro[2] in OS:
					run([fpv], shell=True, check=True)
				elif distro[3] in OS:
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
				
				print('\n\t Backup initiated, please wait...\n')

				run(['cd /tmp/Backup && mysqldump --user=' + userName + ' --password=' + passWord + ' --lock-tables --all-databases > server_db_backup.sql'], shell=True, check=True)

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

				# Compresses the /tmp/Backup/ folder for RSYNC later on.

				#run(['cd /tmp/ && sudo tar -zcvf "ServerBackup.tar.gz" /tmp/Backup '], shell=True, check=True)
				run(["cd /tmp/ && sudo tar cf - /tmp/Backup -P | pv -s $(sudo du -sb /tmp/Backup | awk '{print $1}') | gzip > ServerBackup.tar.gz"], shell=True, check=True)
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

			elif response == '2':
				break




def transferBackup():
	while True:
		
		run(['clear'], shell=True)

		print('\n\t This will RSYNC the Backup to the new server.\n')
		print('\t Is this something you wanted to do?\n')
		print('\t 1: Yes')
		print('\t 2: No\n')
		
		response = input('\t Please input your selection: ')
		
		if response == '1':

			# This clears the terminal, and attempts to RSYNC the previously .tar.gz file we created earlier, and attempts to send it to the new one.
			# Please, if you use this, make sure to change out $yourUsername and $yourIP, otherwise it won't work at all.

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

				print('\n\t Attempting to rsync the file, please wait...\n\t')
				
				# Now we're going to take the input that we stored previously, and import them into the terminal command, so the user doesn't have to manually edit this source file.

				run(['cd /tmp/ && sudo rsync -av -P ServerBackup.tar.gz ' + userName + '@' + ipAddress + ':/tmp/'], shell=True, check=True)

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
			
		elif response == '2':
			break
		



def serverSetup():
	while True:
		
		run(['clear'], shell=True)

		print('\n\t This will install the prerequisites that are needed. Do you want to proceed with this?\n')
		print('\t 1: Yes')
		print('\t 2: No\n')
				
		response = input('\t Please input your selection: ')


		if response == '1':
		
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
  
		elif response == '2':
			break




def restoreBackup():
	while True:
		
		run(['clear'], shell=True)

		print('\n\t Please make sure you have the pre-requisites installed! \n\t In this case, you need NGINX, mariaDB, certbot, and postfix.\n')
		print('\n\t Please make sure that mariaDB is properly setup\n\t with the corresponding user that you will use.\n')
		print('\n\t Do you want to proceed with this?\n')
		print('\t 1: Yes')
		print('\t 2: No\n')

		response = input('\t Please input your selection: ')

		if response == '1':

			# This CD's into /tmp/ and untar's our .tar.gz that we created earlier.
			# Please, make sure that you're in the proper folder in order for this to work.

			run(['clear'], shell=True)
			
			# Here we're going to disable the services while we attempt to restore them.

			print('\t Disabling services momentarily...\n\t')
			sleep(1.25)


			if distro[0 or 1 or 2 or 3 or 4 or 5] in OS:

				run(['sudo systemctl stop nginx'], shell=True, check=True)
				run(['sudo systemctl stop postfix'], shell=True, check=True)
				run(['sudo systemctl stop mariadb'], shell=True, check=True)
				run(['sudo systemctl stop memcached.service'], shell=True, check=True)

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

			run(['cd /tmp/ && sudo pv ServerBackup.tar.gz | tar -xz'], shell=True, check=True)
			sleep(3)
			run(['clear'], shell=True)

			print('\t The file has successfully been decompressed! Attempting restore...\n\t')
			sleep(1.25)

			# Here we're going to move the files to the proper directory that they came from.

			if distro[0 or 1 or 2 or 3 or 4 or 5] in OS:

				run(['cd /tmp/tmp/Backup/etc && sudo cp my.cnf /etc/'], shell=True, check=True)
				run(['cd /tmp/tmp/Backup/etc && sudo cp php.ini /etc/'], shell=True, check=True)
				run(['cd /tmp/tmp/Backup/etc && sudo cp -r nginx/ /etc/'], shell=True, check=True)
				run(['cd /tmp/tmp/Backup/etc && sudo cp -r postfix/ /etc/'], shell=True, check=True)

			elif distro[6] in OS:

				run(['cd /tmp/tmp/Backup/etc/ && sudo cp my.cnf /usr/local/etc/mysql/'], shell=True, check=True)
				run(['cd /tmp/tmp/Backup/etc/ && sudo cp php.ini /usr/local/etc/'], shell=True, check=True)

				# You may ask yourself why we're moving the directories out. Errors are thrown that the directories already exist, so we're moving them!
				# Sure, we can use -f to force the mv into the directory, but moving them to /tmp/ is cleaner, as later on we enable /tmp/ to be autocleared upon reboot.

				run(['cd /usr/local/etc/ && sudo mv nginx/ /tmp/'], shell=True, check=True)
				run(['cd /usr/local/etc/ && sudo mv postfix /tmp/'], shell=True, check=True)

				# Now we'll finally move the directories that we want, back into their proper homes!

				run(['cd /tmp/tmp/Backup/etc/ && sudo mv nginx/ /usr/local/etc/'], shell=True, check=True)
				run(['cd /tmp/tmp/Backup/etc/ && sudo mv postfix/ /usr/local/etc/'], shell=True, check=True)
			
			print('\t /etc/ folders have successfully been restored! Attempting website restore...\n\t')
			sleep(1.25)

			# Now we're going to move the website and mail certs back to their origin.
			# We move the folder that's created by nginx, to the /tmp/ directory, so we can install our own copy.

			if distro[0 or 1 or 2 or 3 or 4 or 5] in OS:

				run(['cd /usr/share/ && sudo mv nginx/ /tmp/'], shell=True)
				run(['cd /tmp/tmp/Backup/usr && sudo cp -r nginx/ /usr/share/'], shell=True, check=True)

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

				run(['cd /tmp/tmp/Backup/etc && sudo cp -r letsencrypt/ /etc/'], shell=True, check=True)

			elif distro[6] in OS:

				run(['cd /usr/local/etc/ && sudo mv letsencrypt/ /tmp/holding/'], shell=True, check=True)
				run(['cd /tmp/tmp/Backup/etc && sudo mv letsencrypt/ /usr/local/etc/'], shell=True, check=True)

			print('\t SSL certs have successfully been restored!\n\t')
			sleep(1.25)

			# Now we'll start the services again, and enable them to persist upon reboot.

			print('\n\t Starting services, and enabling them for future reboots, please wait...\n')

			if distro[0 or 1 or 2 or 3 or 4 or 5] in OS:

				run(['sudo systemctl start nginx && sudo systemctl enable nginx'], shell=True, check=True)
				run(['sudo systemctl start postfix && sudo systemctl enable postfix'], shell=True, check=True)
				run(['sudo systemctl start mariadb && sudo systemctl enable mariadb'], shell=True, check=True)
				run(['sudo systemctl start memcached.service && sudo systemctl enable memcached.service'], shell=True, check=True)

			elif distro[6] in OS:

				run(['sudo service nginx start'], shell=True, check=True)
				run(['sudo service postfix start'], shell=True, check=True)
				run(['sudo service mysql-server start'], shell=True, check=True)
				run(['sudo service memcached start'], shell=True, check=True)

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

					run(['sudo mysql_secure_installation'], shell=True, check=True)

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
		elif response == '2':
			break
