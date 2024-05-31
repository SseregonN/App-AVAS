# App-AVAS
Avas Sound Modifier Simulator


## What the application does
- Allows the user to load a .wav file.
- Allows the user to play and to stop it.
- Allows the user to change the frequency of the sound by modulating the scale "Speed of the vehicle" (speed in kilometer per hour going from 0 to 30)
- Allows the user to export the file in .wav so he can save the sound at a specific speed.

## Application Limits :
- There is a "sound cut" everytime the user changes the scale value. This is due to the loading of a temporary file each time the scale is being modified.
- If the user presses the "Play" or "Stop" button while there is no file loaded, the application crashes.
- The user cannot load several files in several tabs, only one audio file can be loaded at a time.


