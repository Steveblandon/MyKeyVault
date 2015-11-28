'''
Created on Apr 8, 2015

@author: Steve
'''

if __name__ == '__main__':
    pass

import random

print("Key Vault 1.0:")
print("program should be ran in the same file directory as your database file")
datafile = None
datafile_enc = None
action = None
datafilename = None
refkey = '''0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM~!@#$%^&*()_+{}|:"<>?`-=[]\;',./'''
key = ""

while True:
    print("Would you like to encrypt or decode a database?")
    action = raw_input("ENCRYPT/DECODE: ")
    action = action.upper()
    if action == "ENCRYPT" or action == "DECODE":
        break

while True:
    datafilename = raw_input("enter database file name: ")
    try:
        datafile = open(datafilename)
        break
    except:
        print("could not open database. Make sure you write the correct file name (e.g. mypasswords.txt) and that it exists.")

if action == "ENCRYPT":
    while True:
        print("dump encrypted database into new file or overwrite? (overwrite is more memory intensive, it will load the entire file to memory)")
        action = raw_input("NEW/OVERWRITE: ")
        action = action.upper()
        if action == "NEW" or action == "OVERWRITE":
            break
    print("creating key...")
    randomnum = random.randrange(0,len(refkey))
    key = refkey[randomnum]
    while True:
        if len(key) == len(refkey):
            break
        else:
            randomnum = random.randrange(0,len(refkey))
            if key.find(refkey[randomnum]) != -1:
                continue
            else:
                key = key + refkey[randomnum]
    print "new key: " + key
    print("this key will be saved to " + datafilename[:datafilename.find('.')] + "_key.dat, Feel free to rename the file but do not temper with the key. If you do temper with the key the database might not decode correctly.")
    print("make sure to keep this key away from your encrypted database and only bring it out when you need to access your database. You should store it away and make several backups.")   
    
    keyfile = open(datafilename[:datafilename.find('.')] + "_key.dat",'w')
    keyfile.write(key)
    keyfile.close()
    
    if action == "OVERWRITE":
        print "beginning overwrite"      
        database = datafile.readlines()
        print database
        datafile.close()
        datafile = open(datafilename,'w')
        strn = ""
        datafile.write(strn)
        datafile.close()
        datafile = open(datafilename,'a')
        for l in database:
            print l
            for le in l:
                if le == " ":
                    strn = strn + " "
                elif le == '\n':
                    strn = strn + '\n'
                else:
                    strn = strn + key[refkey.find(le)]
            datafile.write(strn)
            print strn
            strn = ""
        database = None
        key = None
        datafile.close()

if action == "DECODE":
    while True:
        print("dump decoded database into new file or overwrite? (overwrite is more memory intensive, it will load the entire file to memory)")
        action = raw_input("NEW/OVERWRITE: ")
        action = action.upper()
        if action == "NEW" or action == "OVERWRITE":
            break
    while True:
        keyfilename = raw_input("enter key file name: ")
        try:
            keyfile = open(keyfilename)
            key = keyfile.read().strip()
            print key
            break
        except:
            print("could not open database. Make sure you write the correct file name (e.g. mypasswords_key.dat) and that it exists.")
    if action == "OVERWRITE":
        print "beginning overwrite"      
        database = datafile.readlines()
        print database
        datafile.close()
        datafile = open(datafilename,'w')
        strn = ""
        datafile.write(strn)
        datafile.close()
        datafile = open(datafilename,'a')
        for l in database:
            print l
            for le in l:
                if le == " ":
                    strn = strn + " "
                elif le == '\n':
                    strn = strn + '\n'
                else:
                    strn = strn + refkey[key.find(le)]
            datafile.write(strn)
            print strn
            strn = ""
        database = None
        key = None
        datafile.close()
raw_input("DONE. You may close this window or press enter")
    