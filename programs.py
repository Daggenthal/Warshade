from subprocess import getoutput

OS = getoutput(["cat /etc/os-release"])

#############################################################################################################################################################

distro = ['debian', 'ubuntu', 'fedora', 'rocky', 'arch', 'opensuse', 'freebsd']

debian = 'sudo apt install nginx mariadb-server memcached certbot postfix pv php-cli php-mysqli php-xml php-fpm memcached python3-certbot-nginx vsftpd'

fedora = 'sudo dnf install nginx mariadb-server memcached certbot postfix pv php-cli php-mysqli php-xml php-fpm php-pecl-memcached python3-certbot-nginx vsftpd'

rocky = 'sudo dnf install -y epel-release && sudo dnf install nginx mariadb-server memcached certbot postfix pv php-cli php-mysqli php-xml php-fpm php-pecl-memcached python3-certbot-nginx vsftpd'

arch = 'sudo pacman -S nginx mariadb-server memcached certbot postfix pv php-cli php-mysqli php-xml php-fpm memcached python3-certbot-nginx vsftpd'

opensuse = 'sudo zypper install nginx mariadb-server memcached certbot postfix pv php-cli php-mysqli php-xml php-fpm memcached python3-certbot-nginx vsftpd'

freebsd = 'sudo pkg install nginx mariadb106-server-10.6.8 mariadb106-client-10.6.8  memcached postfix py38-certbot-nginx-1.22.0 apache24-2.4.54'

#############################################################################################################################################################

dpv = 'sudo apt install -y pv'

fpv = 'sudo dnf install -y pv'

apv = 'sudo pacman -S --noconfirm pv'

opv = 'sudo zypper install -y pv'

bpv = 'sudo pkg install -y pv'
