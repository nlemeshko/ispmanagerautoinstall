import paramiko
import string
import time
import socket
import sys


ip = input (' Введите IP сервера:\n')
try:
    socket.inet_aton(ip)
    # legal
except socket.error:
    print(' Адрес введен неверно!')
    exit(0)
username = input (' Введите логин:\n')
password = input(' Введите пароль:\n')




uname = 'uname -a'
animation = "|/-\\"
ispmgr = 'cd /opt | curl -O http://cdn.ispsystem.com/install.sh'
bash = 'yes | bash install.sh ISPmanager --ignore-hostname'


try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,username=username,password=password)
    print(" Подключение к %s" % ip)
except paramiko.AuthenticationException:
    print(" Неудалось подключиться к %s неверный логин/пароль" %ip)
    exit(1)
except Exception as e:
    print(e.message)
    exit(2)

try:
    stdin, stdout, stderr = ssh.exec_command(uname)
except Exception as e:
    print(e.message)

err = ''.join(stderr.readlines())
out = ''.join(stdout.readlines())
osversion = str(out)+str(err)

print('\n Проверяем версию ОС...')
for i in range(20):
    time.sleep(0.1)
    sys.stdout.write("\r" + animation[i % len(animation)])
    sys.stdout.flush()
time.sleep(2)

if 'el' not in osversion:
    osversion='Debian'
else:
    osversion='RedHat'


if osversion=='RedHat':
    update='yum -y update'
    inst = 'sed -i s/^SELINUX=.*$/SELINUX=disabled/ /etc/selinux/config'
    curl='yum -y install curl'
    reboot = '/sbin/reboot'
else:
    update='yes | sudo apt-get update'
    inst='yes | sudo apt-get upgrade'
    curl='sudo apt-get install curl'
    reboot=''

print('\n Обновляем ОС...')
for i in range(20):
    time.sleep(0.1)
    sys.stdout.write("\r" + animation[i % len(animation)])
    sys.stdout.flush()
time.sleep(2)

try:
    stdin, stdout, stderr = ssh.exec_command(update)
except Exception as e:
    print(e.message)

err = ''.join(stderr.readlines())
out = ''.join(stdout.readlines())
updated=str(out)+str(err)
print(updated)

try:
    stdin, stdout, stderr = ssh.exec_command(inst)
except Exception as e:
    print(e.message)
err = ''.join(stderr.readlines())
out = ''.join(stdout.readlines())
instd=str(out)+str(err)
print(instd)

if osversion=='RedHat':
 print(' Выполняем перезагрузку...')
 for i in range(20):
     time.sleep(0.1)
     sys.stdout.write("\r" + animation[i % len(animation)])
     sys.stdout.flush()
 time.sleep(2)
 try:
    stdin, stdout, stderr = ssh.exec_command(reboot)
 except Exception as e:
    print(e.message)
 time.sleep(30)

 try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,username=username,password=password)
    print(" Переподключаемся к %s" % ip)
 except paramiko.AuthenticationException:
    print(" Неудалось подключиться к %s неверный логин/пароль" %ip)
    exit(1)
 except Exception as e:
    print(e.message)
    exit(2)




print('\n Проверка наличия curl...')
for i in range(20):
    time.sleep(0.1)
    sys.stdout.write("\r" + animation[i % len(animation)])
    sys.stdout.flush()
time.sleep(2)

try:
    stdin, stdout, stderr = ssh.exec_command(curl)
except Exception as e:
    print(e.message)
err = ''.join(stderr.readlines())
out = ''.join(stdout.readlines())
curld=str(out)+str(err)
print(curld)

print('\n Скачивание скрипта ISPmanager5...')
for i in range(20):
    time.sleep(0.1)
    sys.stdout.write("\r" + animation[i % len(animation)])
    sys.stdout.flush()
time.sleep(2)

try:
    stdin, stdout, stderr = ssh.exec_command(ispmgr)
except Exception as e:
    print(e.message)
err = ''.join(stderr.readlines())
out = ''.join(stdout.readlines())
vestad=str(out)+str(err)
print(vestad)


choose = input(' Какой версия ISPmanager5? \n1. Stable (По-умолчанию)\n2. Beta\n')
if choose=='1':
    bash=bash+' --release stable5'
elif choose=='2':
    bash=bash+' --release beta5'
else:
    bash=bash+' --release stable5'

choose = input(' Какой пакет ISPmanager5? \n1. ISPmanager5 с рекомендованными сервисами (По-умолчанию)\n2. ISPmanager5 с минимальным набором сервисов\n3. ISPmanager5 Business\n')
if choose=='1':
    bash=bash+' --pkgname ispmanager-lite'
elif choose=='2':
    bash=bash+' --pkgname ispmanager-lite-common'
elif choose=='3':
    bash=bash+' --pkgname ispmanager-business'
else:
    bash=bash+' --pkgname ispmanager-lite'


try:
    stdin, stdout, stderr = ssh.exec_command(bash)
except Exception as e:
    print(e.message)
err = ''.join(stderr.readlines())
out = ''.join(stdout.readlines())
bashd=str(out)+str(err)
print(bashd)



print(' ISPmanager5 успешно установлен\nАдрес: http://'+ip+':1500\nLogin: root\nПароль: (root пароль)\n\nУспешной работы.')