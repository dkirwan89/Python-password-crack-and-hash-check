#Author: Dearbhail Kirwan
#Student No.D13128910
#Lab3 - Password Cracker with hash checker - calculates SHA1, SHA-256 and SHA-512 of file, cracks the password, and then calculates hashes of file again and compares.(Requires user to input password and close file)
#Written in python 3.4.4 on system running Ubuntu 15.10.
#office2john.py (stored in hashcat folder) was downloaded from https://github.com/kholia/RC4-40-brute-office/blob/master/office2john.py
#cudaHashcat was downloaded from https://hashcat.net/oclhashcat/ (stored on desktop).
#(For filepaths:)Python program was also stored on Desktop.


import subprocess 
import hashlib 

input("\nPlease run this file as root or some of the functions will not work.\nIf you have not done so, please close and start again.\nOtherwise, press enter to continue.\n") #hashcat requires sudo to run successfully

filepath = input("Please enter the filepath of the file you want to crack:") #get the filepath of file to be checked

print("\nBelow are the hashes of the file. They have also been stored in a file called\n SHA-Hashes.txt\n")

#Calculate SHA-1:
BLOCKSIZE = 65536
hasher1 = hashlib.sha1()
with open(filepath, 'rb') as afile:
    buf = afile.read(BLOCKSIZE)
    while len(buf) > 0:
        hasher1.update(buf)
        buf = afile.read(BLOCKSIZE)
sha1 = hasher1.hexdigest()
sha1a = ("SHA-1 of " + filepath + ":" + sha1 + "\n")

#Calculate SHA-256:
BLOCKSIZE = 65536
hasher256 = hashlib.sha256()
with open(filepath, 'rb') as afile:
    buf = afile.read(BLOCKSIZE)
    while len(buf) > 0:
        hasher256.update(buf)
        buf = afile.read(BLOCKSIZE)
sha256 = hasher256.hexdigest()
sha256a = ("SHA-256 of "+ filepath + ":" + sha256 + "\n")

#Calculate SHA-512:
BLOCKSIZE = 65536
hasher512 = hashlib.sha512()
with open(filepath, 'rb') as afile:
    buf = afile.read(BLOCKSIZE)
    while len(buf) > 0:
        hasher512.update(buf)
        buf = afile.read(BLOCKSIZE)
sha512 = hasher512.hexdigest()
sha512a = ("SHA-512 of " + filepath + ":" + sha512 + "\n")

print(sha1a) #print hashes for user
print(sha256a)
print(sha512a)

shas = open("SHA-Hashes.txt", "w")

shas.write(sha1a) #write hashes to a file
shas.write(sha256a)
shas.write(sha512a)


input("Press enter to continue")


subprocess.call("python2 /home/dearbhail/Desktop/cudaHashcat/office2john.py " + filepath + " > hash.txt", shell = True) #get hash of password

subprocess.call('/home/dearbhail/Desktop/cudaHashcat/cudaHashcat64.bin -a 0 -m 9600 --username -o result.txt hash.txt /home/dearbhail/Desktop/cudaHashcat/rockyou.txt', shell = True) #find password with matching hash
	
subprocess.call("mv cudaHashcat.log /home/dearbhail/Desktop/cudaHashcat/extraoutputfiles", shell = True) #clean up

subprocess.call("mv cudaHashcat.pot /home/dearbhail/Desktop/cudaHashcat/logandpotfiles", shell = True) #clean up

print("\n\nThe log and pot files for this session have been stored in \n /home/dearbhail/Desktop/cudaHashcat/logandpotfiles. \nPlease move them if you wish to store them as you may have to \nreplace them if you wish to save further log and pot files.")
input("\nPress enter to continue.\n") #informing user

output = open("result.txt", "r")#opens results file

line = output.readline() #reads output file

passwds = line.split(":") #seperates password from string

output.close() #close results file

passw = open("password.txt", "w") #create file to write password to

firstline = ("The password for the file " + filepath + " is: " + passwds[1]) #variable to write password to file in single arguement

passw.write(firstline) #write password to file

passw.close() #close password file

print (firstline) #prints password for user

print("\nThe password has been saved to a file called passwords.txt. \nThis will be overwritten if you run this program again.")

subprocess.call("rm -r hash.txt", shell = True) #clean up

subprocess.call("rm -r result.txt", shell = True) #clean up

print("\nThe file will be opened now. \nPlease input the password when prompted and then close the file.")

input("\nPress enter to continue")

subprocess.call("libreoffice " + filepath, shell = True) #open password protected file

input("\nPress enter when you have completed this\n") #wait for user to input password then close

print("The hashes will now be compared.\n") #recalculate hashes after cracking


#Calculate SHA-1:
BLOCKSIZE = 65536
hasher1 = hashlib.sha1()
with open(filepath, 'rb') as afile:
    buf = afile.read(BLOCKSIZE)
    while len(buf) > 0:
        hasher1.update(buf)
        buf = afile.read(BLOCKSIZE)
sha1_1 = hasher1.hexdigest()
sha1b = ("(After opening) SHA-1 of " + filepath + ":" + sha1_1 + "\n")

#Calculate SHA-256:
BLOCKSIZE = 65536
hasher256 = hashlib.sha256()
with open(filepath, 'rb') as afile:
    buf = afile.read(BLOCKSIZE)
    while len(buf) > 0:
        hasher256.update(buf)
        buf = afile.read(BLOCKSIZE)
sha256_1 = hasher256.hexdigest()
sha256b = ("(After opening) SHA-256 of "+ filepath + sha256_1 + "\n")

#Calculate SHA-512:
BLOCKSIZE = 65536
hasher512 = hashlib.sha512()
with open(filepath, 'rb') as afile:
    buf = afile.read(BLOCKSIZE)
    while len(buf) > 0:
        hasher512.update(buf)
        buf = afile.read(BLOCKSIZE)
sha512_1 = hasher512.hexdigest()
sha512b = ("(After opening) SHA-512 of " + filepath + ":" + sha512_1 + "\n")

print(sha1b) #print hashes for user
print(sha256b)
print(sha512b)


shas.write(sha1b) #write hashes to file
shas.write(sha256b)
shas.write(sha512b)

shas.close() #close hash file

sha_check = 0 #variable for checking all hashes match

if sha1 == sha1_1:
	print("Pre and Post cracking SHA-1 match\n")
	sha_check += 1
if sha1 != sha1_1:
	print("Pre and Post cracking SHA-1 do not match\n")
if sha256 == sha256_1:
	print("Pre and Post cracking SHA-256 match\n")
	sha_check += 1
if sha256 != sha256_1:
	print("Pre and Post cracking SHA-256 do not match\n")
if sha512 == sha512_1:
	print("Pre and Post cracking SHA-512 match\n")
	sha_check +=1
if sha512 != sha512_1:
	print("Pre and Post cracking SHA-512 do not match\n")

if sha_check == 3:
	print("Overall result: Cracking did not alter the hashes of the file.")
else:
	print("Overall result: Cracking altered the hashes of the file.\n")
