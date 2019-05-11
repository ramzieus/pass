import random
import sqlite3
import getpass
import os
import sys
import pyperclip
import datetime


path = r'C:\Users\{}\AppData\Local\passe'.format(getpass.getuser())

if not os.path.exists(path):
    os.mkdir(path)
conn = sqlite3.connect(path + '\pass.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS pass(name text, pass text,time text)''')
s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
passlen = 32

def create_new_pass():
    name = input('Enter The name of password : ')
    c.execute("SELECT name FROM pass WHERE name = ?", (name,))
    data=c.fetchall()
    if len(data)==0:
        ch = input('0) Enter manualy \n1) Generate \n~> ')
        if ch == '0':
            password = input('enter your password : ')
        else:
            password = "".join(random.sample(s,passlen))
        print(password)
        c.execute("INSERT INTO pass VALUES ('{}','{}','{}')".format(name,password,datetime.datetime.now().date()))
    else:
        ex = input('the password exist !\n0) override ?\n1) no !\n~>')
        if ex == '0':
            ch = input('0) Enter manualy \n1) Generate \n~> ')
            if ch == '0':
                password = input('enter your password : ')
            else:
                password = "".join(random.sample(s,passlen))
            print(password)
            c.execute("UPDATE pass SET pass = '{}', time = '{}' WHERE name = '{}'".format(password,datetime.datetime.now().date(),name))
        else:
            print('ok !')
    conn.commit()
    conn.close()



def list_of_pass():
    for row in c.execute('SELECT * FROM pass'):
        name, pas, time = row
        print(name + ' : ' + pas + ' | ' + time)
    conn.commit()
    conn.close()
    

def remove_pass():
    rem = input('Enter the name of password you want to delete : ')
    c.execute("SELECT name FROM pass WHERE name = ?", (rem,))
    data=c.fetchall()
    if len(data)==0:
        print('The entry not exist')
    else:
        c.execute("DELETE FROM pass WHERE name='{}'".format(rem))
        print(rem +' was deleted')
    conn.commit()
    conn.close()

def remove_db():
    i = input('Are you sur ?\ntype yes to confirm : ')
    if i == 'yes':
        conn.close()
        os.remove(path + '\pass.db')
    else:
        print('ok !')

def get_pass(a):
    c.execute("SELECT pass FROM pass WHERE name = ?", (a,))
    data=c.fetchone()
    pyperclip.copy(data[0])
    print('passwor copied to clipboard !')


if len(sys.argv) == 1:
    choose = input('1) To generate password \n2) To list all passwords \n3) To delete passwords \n4) to clean all passwords \n~> ')
    if choose == '1':
        create_new_pass()
    elif choose == '2':
        list_of_pass()
    elif choose == '3':
        remove_pass()
    elif choose == '4':
        remove_db()
    else:
        print('GoodBye !')
else:
    get_pass(sys.argv[1])