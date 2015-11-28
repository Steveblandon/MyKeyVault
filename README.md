# MyKeyVault
Small program I created to mess around with encryption for storing passwords and account information. The program by no means follows any encryption standards of cryptography as far I know. What it actually does is that the program obfuscates data in a text file, then a separate file is created as the key that the program needs to decrypt the data file. The main idea being that you put this key file in a separate physical device like a USB. The program can be set to automatically check a USB drive for the key file as soon as it starts.

HOW IT WORKS:
1. user sets where to find the key (in this case, USB path names) in the configuration file named KeyVault_conf.txt (e.g. G:\\)
2. program is started, it tries to open the database file named KeyVault_db.dat and the configuration file. 
3. program then checks the config file for the keyword "kvf_encrypted" in the config file. If not found the program assumes that the KeyVault_db.txt file is not encrypted. So it calls for a new key to be created and dumps a key file named KeyVault_key.dat. It then encrypts the file.
4. if keyword is found, it assumes that the database is encrypted so it will try to obtain a key, looking in the places noted in the config file. If found it continues onto opening the database file and decoding it. The program copies every line into a list and it then displays everything that's inside decoded.
5. program then loops through a set of options: "Add Entry", "Delete Entry", "Create New Key", "Display Key", "Update", "Get Password"
    - "Add Entry" loops into a list, the user should leave entry blank to notify program that that would be all. Entry is appended to the list containing the database.
    - "Delete Entry" asks the user to input the entry's title. Program loops through list containing the database saving every line to a temporary list, skipping the entry to be deleted from when the entry title is found until a blank line space is found. The program then replaces the original list containing the database with the new list.
    - "Create New Key"  creates a new encryption key, encrypts database with key.
    - "Display Key" displays the key and copies it to clipboard.
    - "Update" overwrites database file with the list containing the database. And displays the updated entries.
    - "Get Password" asks user to enter entry to extract password from, then on which line the password is. Password is then copied to clipboard.
