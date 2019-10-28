import sys
import subprocess
import re


# 1. Python script which will copy database file of debuggable apps from the android device to your computer using ADB.
# 2. This script ask for PackageName and DatabaseName at runtime.
# 3. You can make it static by passing -d at as command line argument while running script and setting defaults in following way.
# 4. Edit script and change the values of varialbe packageName and dbName to debuggable app package name and database name then
# run script as : python Copydbfileandroid.py -d 

useDefaults = False


def checkIfPackageInstalled(strSelectedDevice) :

    packageName = 'com.whatsapp'
    dbName = 'msgstore.db.crypt12'


    if not useDefaults : 
        print('Please enter package name : ')
        packageName = raw_input()

    packageString = 'package:'+packageName

    try:
        adbCheckIfPackageInstalledOutput = subprocess.check_output('adb -s ' + strSelectedDevice + ' shell pm list packages | grep -x '+ packageString, shell=True)
    except subprocess.CalledProcessError as e:
                print "Package not found"
                return


    if packageString.strip() == adbCheckIfPackageInstalledOutput.strip() : 
        if not useDefaults : 
            print('Please enter db name : ')
            dbName = raw_input()

        adbCopyDbString = 'adb -s '+strSelectedDevice + ' -d shell \"run-as '+packageName+' cat /data/data/'+packageName+'/databases/'+ dbName +'\" > '+dbName

        try:
            copyDbOp = subprocess.check_output(adbCopyDbString,shell=True)
        except subprocess.CalledProcessError as e:
                return

        if "is not debuggable" in copyDbOp :
            print packageString + 'is nto debuggable'

        if copyDbOp.strip() == "":
            print 'Successfully copied '+dbName + ' in current directory'

    else :
        print 'Package is not installed on the device'



defaultString = "-d"
if len(sys.argv[1:]) > 0 and sys.argv[1] == defaultString :
        useDefaults = True

listDevicesOutput = subprocess.check_output("adb devices", shell=True)
listDevicesOutput = listDevicesOutput.replace("List of devices attached"," ").replace("\n","").replace("\t","").replace("\n\n","")

numberofDevices = len(re.findall(r'device+', listDevicesOutput))

connectedDevicesArray = listDevicesOutput.split("device")   
del connectedDevicesArray[-1] 


strSelectedDevice = ''
if(numberofDevices > 1) :
    print('Please select the device : \n'),

    for idx, device in enumerate(connectedDevicesArray):
        print idx+1,device

    selectedDevice = raw_input()

    if selectedDevice.isdigit() :
        intSelected = int(selectedDevice)
        if 1 <= intSelected <= len(connectedDevicesArray) :
            print 'Selected device is : ',connectedDevicesArray[intSelected-1]
            checkIfPackageInstalled(connectedDevicesArray[intSelected-1])
        else :
            print 'Please select in range'
    else : 
        print 'Not valid input'

elif numberofDevices == 1 :
    checkIfPackageInstalled(connectedDevicesArray[0])
elif numberofDevices == 0 :
    print("No device is attached")
