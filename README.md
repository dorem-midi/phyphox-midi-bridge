# phyphox-midi-bridge
Code that converts data received by a computer from phone Phyphox app to midi CC messages

This app was written to be used as a part of the Pianobook project's free VST instruments. I am currently creating a binaural piano instrument that will change sound perspectives as you move your head.  Think of it as a virtual reality instrument.  As your head moves, the soundstage stays in the same location as if you were playing a real piano.

The "panning" (it's not panning, it literally is the a "morphing" of the soundstage) is done like this:

1. you download Phyphox on your phone, run the magnetometer routine, and transmit the data on your local wifi network.
2. you run phyphox-midi-bridge to collect the data in real time and transform it into midi CC1 (modulation wheel)
3. the phyphox-midi-bridge sends the CC1 data to your virtual instrument - in the case of a Windows machine, you need to use loopMIDI to create a virtual midi port.

To use the apparatus described in 1-3, you put your phone on your head (so it can track your head angle), preferably between your headphone strap and head to stay relatively secure, and go and play your digital piano VI.  As you change your left/right head angle, the modulation wheel CC1 controller will change.

I'm currently making a new piano VI, that has been recorded at different binaural angles that is to be used with the apparatus 1-3.  It is amazing how realistic the prototype is.

NOTE:  currently the python app works on PC - if someone can try it on MacOS, that would be great.

Also, the .exe version was made using pyinstaller, and it is currently flagged by antivirus.  My suggestion if you don't trust the exe is to just install python and all of the include libraries and run directly from sourcecode.  If anyone has a better idea, let me know.

More information on how to install can be found on my rudimentary youtube page:
https://www.youtube.com/watch?v=Ddhh9WF95ho&t=28s
