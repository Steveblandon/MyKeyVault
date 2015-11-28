'''
Created on Apr 8, 2015

@author: Steve
'''

if __name__ == '__main__':
    pass

import random
import os
import pyperclip
import shutil
print "==============="
print("KeyVault 2.0:")
print "==============="
keyfile_n = "KeyVault_key.dat"
database_n = "KeyVault_db.dat"
database_temp = []
config_n = "KeyVault_conf.txt"
refkey = '''0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM~!@#$%^&*()_+{}|:"<>?`-=[]\;',./'''
key = ""
keypath = ""

def createKey():
    global key
    print("Creating new encryption key...")
    randomnum = random.randrange(0,len(refkey))
    key = refkey[randomnum]
    while True:
        if len(key) == len(refkey): break
        else:
            randomnum = random.randrange(0,len(refkey))
            if key.find(refkey[randomnum]) != -1: continue
            else: key = key + refkey[randomnum]
    print "Encryption key created..."
    keyfile = open(keyfile_n,'w')
    keyfile.write(key)
    keyfile.close()
    shutil.move(os.getcwd() + '\\' + '\\' + keyfile_n, keypath + keyfile_n)
    print "New key saved to",keypath + keyfile_n
        
def getKey():
    global key, keypath
    config = open(config_n)
    try:
        shutil.move(keypath + keyfile_n, os.getcwd() + '\\' + '\\' + keyfile_n)
        keyfile = open(keyfile_n)
        key = keyfile.read().strip()
        keyfile.close()
        shutil.move(os.getcwd() + '\\' + '\\' + keyfile_n, keypath + keyfile_n)
        return True
    except:
        for line in config:
            if '=' in line:
                path = line[line.find('=')+1:].strip()
                try:
                    shutil.move(path + keyfile_n, os.getcwd() + '\\' + '\\' + keyfile_n)
                    keyfile = open(keyfile_n)
                    key = keyfile.read().strip()
                    keyfile.close()
                    keypath = path
                    shutil.move(os.getcwd() + '\\' + '\\' + keyfile_n, keypath + keyfile_n)
                    return True
                except: continue
    return False

def verifyPath():
    global keypath
    config = open(config_n)
    for line in config:
        if '=' in line:
            path = line[line.find('=')+1:].strip()
            if os.path.exists(path):
                keypath = path
                config.close()
                return True
    config.close()
    return False

def decode_db():
    global database_temp
    database_temp = []
    database = open(database_n)
    for line in database:
        strn = ""
        for letter in line:
            if letter == " ": strn = strn + " "
            elif letter == '\n': strn = strn + '\n'
            else: strn = strn + refkey[key.find(letter)]
        database_temp.append(strn.strip())
    database.close()

def encrypt_db(mode):
    global database_temp
    if mode == "transfer":
        database = open(database_n)
        for line in database: database_temp.append(line.strip())
        database.close()
    database = open(database_n,'w')
    database.write("")
    database.close()
    database = open(database_n,'a')
    strn = ""
    for line in database_temp:
        for letter in line:
            if letter == " ": strn = strn + " "
            elif letter == '\n': strn = strn + '\n'
            else: strn = strn + key[refkey.find(letter)]
        database.write(strn + '\n')
        strn = ""
    database.close()
    
def display_db():
    for line in database_temp:
        print line

while True:
    try:
        database = open(database_n)
        database.close()
        database = None
    except:
        print("No KeyVault_db.dat file found.")
        database = open(database_n,'w')
        database.write("")
        database.close()
        print "A new KeyVault_db.dat file was created."
    try:
        config = open(config_n)
    except:
        print("No KeyVault_conf.txt file found.")
        config = open(config_n,'w')
        config.write("PATH_1 = G:\\"+'\\'+'\n')
        config.close()
        config = open(config_n,'a')
        config.write("PATH_2 = H:\\"+'\\'+'\n')
        config.close()
        print "a new KeyVault_conf.txt file was created. Please update it if necessary before opening program again."
        config = open(config_n)
    enc = False
    conf = config.read()
    config.close()
    config = None
    if conf.find("kvf_encrypted") == -1:
        if verifyPath(): createKey()
        else:
            print "No external drive found."
            print "please insert USB drive and/or update paths in config file."
            break
        encrypt_db("transfer")
        config = open(config_n,'a')
        config.write("kvf_encrypted")
        config.close()
        config = None
        enc = True
    if verifyPath(): 
        if getKey():
            decode_db()
            display_db()
            while True:
                print "OPTIONS: Add Entry | Delete Entry | Create New Key | Display Key | Get Password | Update"
                action = raw_input("What would you like to do next?: ")
                if "add" in action.lower():
                    print "New Entry: Enter each line of text exactly as you want and press enter to go to the next line. Leave line empty to finish entry"
                    while True:
                        input_ = raw_input("")
                        database_temp.append(input_)
                        if input_ == "": break
                    print "New entry created."
                elif "delete" in action.lower():
                    print "Delete Entry: Enter at least a complete word from the entry to identify it"
                    input_ = raw_input("").strip()
                    list_temp = []
                    entry = []
                    skip = False
                    entryFound = False
                    for line in database_temp:
                        if input_ in line or skip:
                            skip = True
                            entryFound = True
                            if len(entry) == 0: print "Entry Found"
                            if line == "" or line == '\n': skip = False
                            else: entry.append(line)
                        else: list_temp.append(line)
                    if entryFound == False: "Entry not found."
                    else:
                        i = 1
                        for line in entry:
                            print "line #" + str(i)+'.',line
                            i += 1
                        cont = raw_input("delete? [yes/no]: ")
                        if "yes" in cont:
                            database_temp = list_temp
                            print "Entry deleted."
                        else: print "Entry was not deleted."
                elif "new" in action.lower():
                    if verifyPath():
                        createKey()
                        encrypt_db("")
                    else:
                        print "No external drive found."
                        print "please insert USB drive and/or update paths in config file."
                elif "display" in action.lower():
                    print key
                    pyperclip.copy(key.strip())
                    pyperclip.paste()
                    print "(copied to clipboard)"
                elif "update" in action.lower():
                    encrypt_db("")
                    print "database updated successfully."
                    display_db()
                elif "get" in action.lower():
                    print "Get Password: Enter at least a complete word from the entry to identify it"
                    input_ = raw_input("").strip()
                    list_temp = []
                    entryFound = False
                    for line in database_temp:
                        if (line == "" or line == '\n') and entryFound:
                            break
                        if entryFound: list_temp.append(line)
                        if input_ in line and entryFound == False:
                            entryFound = True
                            print "Entry found."
                            list_temp.append(line)
                    if entryFound == False: "Entry not found."
                    else:
                        i = 1
                        for line in list_temp:
                            print "line #" + str(i)+'.',line
                            i += 1
                        nm = int(raw_input("enter line number to extract (e.g. 1):"))
                        password = list_temp[nm-1].strip()
                        pyperclip.copy(password)
                        pyperclip.paste()
                        print password, "(copied to clipboard)"
                else: break
                print ""
        else:
            print "No KeyVault_key.dat file found."
            break
    else:
        print "No external drive found."
        print "please insert USB drive and/or update paths in config file."
        break
    
    break
raw_input("")
