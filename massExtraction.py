#!/usr/bin/env python
import os, glob

fList = []
Dir = "/media/sf_delete/Dlink/DLink_Scraper/firmwares"

#def getFiles():
	#return os.listdir(Dir)
	

if __name__=='__main__':
	print("[+] Starting")
	count = 0
 	#fList = getFiles()
	##print(fList)

	os.chdir("firmwares")
	for fmware in glob.glob("*.zip"):
		print(fmware)
		unzip = "unzip " + str(fmware)
		os.system(unzip)	

	##for f in fList:
	##	try:
	##		unzip = "unzip " + str(f)
	##		print(unzip)
	##		os.system(unzip)
	##		
	##		#print("There: " + f[:-4])
	##		#os.chdir( "cd " + str(f[:-4]) )
	##		#print("made it")

	##		#for fmware in glob.glob("*.bin"):
	##		#	binwlk = "binwalk -e " + str(fmware)
	##		#	os.system(binwlk)
	##		#	print("[+] Binwalked")


	##		#os.chdir("..")
	##		print("done")
	##	except:
	##		print("[-] Failed to binwalk")
	##	finally:
	##		break

	print("[+] Completed Task")
