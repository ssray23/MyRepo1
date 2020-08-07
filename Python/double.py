import os
import datetime 
os.remove("number2.txt")
f = open("number.txt", "r")
f1 = open("number2.txt","x")
for y in f:
	x = int(y)*2
	f1.write("%s\n" %x)
f.close()
f1.close()