#!/usr/bin/env python
import base64
import hashlib
import getpass
from Crypto import Random
from Crypto.Cipher import AES
import os
import sys

class AESCipher(object):

    def __init__(self, key): 
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
    
    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
    
    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

def getConfigInfo():
    file = open("theDoctorconfig.cfg","r")
    list1 = []
    for line in file:
        if not line.startswith("#"):
            if line.startswith("."):
                print "File name cannot start with . (dot) character!"
                sys.exit()
            list1.append(line.strip())
    file.close()
    return list1

def main():
    list1 = getConfigInfo()
    try:
        fileName = list1[0]
        newfile = list1[1]
    except(Exception):
        print "No file name found in the configuration file"
        sys.exit()
    plainText = ""
    encText = ""
    print "Select option: 1 -> For file encryption. "
    print "               2 -> For file decryption. "

    while(True):
        try:
            value = int(input("Option: "))
        except (NameError, SyntaxError, ValueError):
            print "Sorry, I didn't understand that."
            continue
        if (value == 1) or (value == 2):
            break
        else:
            print "This is not a valid option!"
    
    if value == 1:
        try:
            file = open(fileName, 'r')
            for line in file:
                plainText += line
            file.close()           
            try:                
                password1 = getpass.getpass()
                print "Retype password"
                password2 = getpass.getpass()
                if password1 == password2:
                    file = open(newfile,"w")
                    aesCipher = AESCipher(password1)
                    encText = aesCipher.encrypt(plainText)
                    file.write(encText)
                    file.close()
                    try:
                        os.remove("./" + fileName)
                    except(ValueError):
                        print "An error has occured."
                    print "Success!"
                else:
                    print "Passwords don't match! Aborting..."
                    sys.exit()
            except (IOError):
                print "File " + newfile + " cannot be created!"
        except (IOError):
            print "No file " + fileName + " was found...Check if the configuration is good."
    
    if value == 2:
        try:
            file = open(newfile,"r")
            for line in file:
                encText += line
            file.close()
            password = getpass.getpass()
            aesCipher = AESCipher(password)
            try:   
                decText = aesCipher.decrypt(encText)
                try:
                    file = open(fileName,"w")
                    file.write(decText.encode('ascii', 'ignore').decode('ascii'))
                    file.close()
                except(IOError):
                    print "File " + newfile + " cannot be created!"
                try:
                    os.remove("./" + newfile)
                except(ValueError):
                    print "An error has occured."
                print "Succes!"
            except(UnicodeDecodeError):
                print "Wrong password!"
        except(IOError):
            print "No file " + newfile + " was found...Check if the configuration is good."

if __name__ == '__main__': main()