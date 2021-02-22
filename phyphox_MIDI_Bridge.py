import mido
import mido.backends.rtmidi
import requests
import time
import sys
import math

# THIS FUNCTION CALCULATES ABSOLUTE ANGLE WITH MAGNETOMETER INPUT
#
# math.atan(x) Return the arc tangent of x, in radians. The result is between -pi/2 and pi/2.
# Recommended angle using magnetometer input
# Direction (y>0) = 90 - [arcTAN(x/y)]*180/pi
# Direction (y<0) = 270 - [arcTAN(x/y)]*180/pi
# Direction (y=0, x<0) = 180.0
# Direction (y=0, x>0) = 0.0
def anglefunction(array):

    if array[1] > 0:
        angle = 90 - math.atan(array[0]/array[1])*180/3.1415
    if array[1] < 0:
        angle = 270 - math.atan(array[0]/array[1])*180/3.1415
    if array[1] == 0 and array[0] < 0:
        angle = 180
    if array[1] == 0 and array[0] > 0:
        angle = 0

    return angle



#Initialize and request the parameters
print("\n" * 100)
print("*** PHYPHOX MIDI BRIDGE ***")
print("")
print("Please follow these directions EXTREMELY carefully.")
print("")
print("The original purpose of this tool is to enable a VR piano experience")
print("powered by a smartphone used as an orientation sensor to trigger an")
print("immersive binaural soundstage that tracks with the pianist's head")
print("movement. To do this, a smartphone orientation sensor is connected")
print("to the modulation wheel MIDI controller in Kontakt, or other VI or DAW")
print("")
print("Currently, this app is untested on MacOS.  For Windows users, you will")
print("need the LoopMIDI utility")
print("")
print("To use it, you must have Phyphox installed on your phone to")
print("collect the sensor data. Windows users also should have LoopMIDI running")
print("on your computer to receive the data so that it can be routed to a VI or DAW.")
print("")
print("LoopMIDI should thus be set as an input to your VI or DAW (e.g. Kontakt)")
print("")
print("The basic data chain is like this:")
print("1. Phyphox collects sensor data and sends to your PC")
print("2. Phyphox MIDI bridge receives the data, converts to MIDI CC data")
print("3. Phyphox MIDI bridge sends the CC data to LoopMIDI")
print("4. LoopMIDI sends the CC data to your VI or DAW")
print("")
print("Before starting, please have LoopMIDI running and a Loopback")
print('midi port running. Loopback midi ports have names like "loopMIDI Port 2"')
print("")
dummy = input("Press Enter to continue")

#MIDI configuration
print("\n" * 100)
print("")
print("*** SETUP MIDI CONFIGURATION")
print("")
print("Available midi ports are listed below:")
print(mido.get_output_names())
print("")
print('LoopMIDI ports typically have names like "loopMIDI port 2"')
print("")
M_OUTPUT = input("Enter midi port from the list (without quotemarks): ")
M_CHANNEL = 0
#M_CONTROLS = [1, 2, 3] #You can send on different CC channels
M_CONTROLS = [1, 2, 3]
print("")
print("")
print("")

try:
    output = mido.open_output(M_OUTPUT)
except:
    print("\n" * 100)
    print("Could not open the port output. Available outputs:")
    print(mido.get_output_names())
    print("")
    print("Sorry this isn't so user friendly, I think there was a typo. Run the app again")
    sys. exit()

#phyphox configuration
print("\n" * 100)
print("*** SETUP PHYPHOX PHONE CONNECTION")
print("")
print("1. Make sure that your phone and computer are on the same network")
print("2. Open the phyphox app on your phone, go to magnetometer screen")
print("3. Find and check the enable remote access box and note the ip address")
print("4. Press the play button to start the phone sensor transmitting")
print(" ")
PP_ADDRESS = input("Enter the ip address and port (example: 192.168.0.114:8080): ")
PP_ADDRESS = "http://" + PP_ADDRESS
#PP_CHANNELS = ["magX", "magY", "magZ"] #If using different CC channels, define multiple phyphox buffers
PP_CHANNELS = ["magX", "magY", "magZ"]
print("")
print("")
print("")


# Calibration routines to capture data at 4 specified angles:
# Center(forward), Center Down, Right and Left
# Then figure out which mag sensor to use by taking using the one
# with the largest change (Delta)

# ****CENTER CALIBRATION***
print("\n" * 100)
print("*** CALIBRATE THE MAGNETOMETER")
print("")
print("Now that the phone is connected and the sensors are turned on,")
print("place the phone underneath the headband of your headphones. Be")
print("careful not to turn off the screen by accident! The")
print("headband should press the phone to the top of your head. Try to")
print("make phone as stable as possible on your head and be careful not")
print("to drop your phone.")
print("")
print("If you are using earbuds, you will need to find a way to strap")
print("the phone to your head, potentially with a headband or strapped to")
print("a hat. Put the contraption onto your head.")
print("Now we can calibrate the system...")
print("")
print("To calibrate the magnetometer we need to take readings at")
print("different head orientations, relative to your keyboard.")
print("Try diff calibrations - try to make it as natural feeling as possible")
print("")
print("*****************************************************************")
print("")
print("CENTER CALIBRATION")
print("Face the piano and look straight as if you were reading music.")
print("Freeze your head in this position, and then...")
print("")
dummy = input("Press Enter to capture CENTER calibration")

#Capture the data at Center position
url = PP_ADDRESS + "/get?" + ("&".join(PP_CHANNELS))
data = requests.get(url=url).json()
Center_values = []
for i, control in enumerate(M_CONTROLS):
    Center_values.append(data["buffer"][PP_CHANNELS[i]]["buffer"][0])
#print(Center_values)
Ctr_absolute = anglefunction(Center_values)
print(Ctr_absolute)
print("")
print("CENTER calibration recorded!")



#RIGHT AND LEFT calibration may need to be re-written.  Not sure
#if there is a difference between calibrating while looking at C7 or above C7


# ****RIGHT CALIBRATION***
print("")
print("*****************************************************************")
print("")
print("RIGHT SIDE CALIBRATION")
print("Face the piano with your shoulders, turn your head to look")
print("directly at the highest C key.")
print("")
dummy = input("Press Enter to capture RIGHT calibration")
#Capture the data at Right position
url = PP_ADDRESS + "/get?" + ("&".join(PP_CHANNELS))
data = requests.get(url=url).json()
Right_values = []
for i, control in enumerate(M_CONTROLS):
    Right_values.append(data["buffer"][PP_CHANNELS[i]]["buffer"][0])
#print(Right_values)
Rt_absolute = anglefunction(Right_values)
print(Rt_absolute)
print("")
print("RIGHT calibration recorded!")




# ****LEFT CALIBRATION***
print("")
print("*****************************************************************")
print("")
print("LEFT SIDE CALIBRATION")
print("Face the piano with your shoulders, turn your head to look")
print("directly at the lowest C key.")
print("")
dummy = input("Press Enter to capture LEFT calibration")
#Capture the data at Left position
url = PP_ADDRESS + "/get?" + ("&".join(PP_CHANNELS))
data = requests.get(url=url).json()
Left_values = []
for i, control in enumerate(M_CONTROLS):
    Left_values.append(data["buffer"][PP_CHANNELS[i]]["buffer"][0])
#print(Left_values)
Lft_absolute = anglefunction(Left_values)
print(Lft_absolute)
print("")
print("LEFT calibration recorded!")




print("")
print("")
print("")
print("After you press Enter below, the app will begin. Close window")
print("to stop the app.")
dummy = input("Press Enter to start the MIDI bridge")

######
# Offset angles if the range goes through 0 deg. #
######

#if Lft_absolute < Ctr_absolute and Ctr_absolute < Rt_absolute:
offset = 0

if Lft_absolute > Ctr_absolute and Ctr_absolute < Rt_absolute:
    offset = 180
    Ctr_absolute = Ctr_absolute + offset
    Rt_absolute = Rt_absolute + offset
    Lft_absolute = Lft_absolute - offset

if Lft_absolute < Ctr_absolute and Ctr_absolute > Rt_absolute:
    offset = -180
    Ctr_absolute = Ctr_absolute + offset
    Rt_absolute = Rt_absolute - offset
    Lft_absolute = Lft_absolute + offset    


#Function used to map raw acceleration values to MIDI values 0..127
#Function also compensates for head down position (Z-axis compensation)
#
# ii = magnetometer angle input
# lc, cc, rc = calibration angles
# oxy = output XY 
#


# map1 with z-axis compensation OFF

def map1(ii,lc,cc,rc):
    try:  
        
        if ii < cc:
            oxy = 63 - round(64*(cc-ii)/(cc-lc))         
        else:
            oxy = 63 + round(64*(ii-cc)/(rc-cc))
        
    except:
        return 0
    if ii < lc:
        oxy = 0
    if ii > rc:
        oxy = 127
    if oxy > 127:
        oxy = 127
    if oxy < 0:
        oxy = 0
    return oxy


counter = 0
mylist = []
while True:

    url = PP_ADDRESS + "/get?" + ("&".join(PP_CHANNELS))
    data = requests.get(url=url).json()
    input_values = []
    for i, control in enumerate(M_CONTROLS):
        input_values.append(data["buffer"][PP_CHANNELS[i]]["buffer"][0])
     
    a = anglefunction(input_values)
    if offset == 180 or offset == -180:
        if a < 180:
            a = a + 180
        elif a > 180:
            a = a - 180 


    mylist.append(map1(a,Lft_absolute,Ctr_absolute,Rt_absolute))
    N = 3
    cumsum, moving_aves = [0], []

    for i, x in enumerate(mylist, 1):
        cumsum.append(cumsum[i-1] + x)
        value = 0
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            #can do stuff with moving_ave here
            value = round(moving_ave)
            moving_aves.append(moving_ave)

    #Set CC control number - 1 is for Mod wheel
    control = 1
 #   print("Channel " + str(M_CHANNEL) + ", CC #" + str(control) + ", value " + str(value) + ", (RAW " + str(a) + ")")
    output.send(mido.Message("control_change", channel=M_CHANNEL, control=control, value=value))



