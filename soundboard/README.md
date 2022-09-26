# NeoTrellis M4 Soundboard

## Overview

I’ve always wanted to make my games immersive in a way most people could get into it and enjoy it. So, I decided to create a soundboard. in the past I used websites before using an app on my phone, and now I’ve finally created a standalone self-contained soundboard. Which can be used for anything really.

## Parts needed

![NeoTrellis m4](https://raw.githubusercontent.com/israelperez/heroquest/main/soundboard/neotrellis-m4-4020.jpeg)

**NeoTrellis M4**

https://www.adafruit.com/product/4020
I bought mine from digikey. this kit includes the following parts.

- 1 x Adafruit NeoTrellis M4 Mainboard
- 1 x Adafruit NeoTrellis M4 Enclosure kit
- 2 x Silicone Elastomer 4x4 Button Keypad
- 1 x Little Rubber Bumper Feet (4 bumpers total)

assembly of the NeoTrellis M4 Enclosure kit is pretty straight forward, just note the order of the acrylic panels is important. If you’re using the 3d printed mount then don’t use the screws on the side, we will use these to attach it to mount.
https://learn.adafruit.com/adafruit-neotrellis-m4/assembly

![usb speaker image](https://raw.githubusercontent.com/israelperez/heroquest/main/soundboard/usb-speakers.jpg)

**USB speaker**

This is the one I bought because it comes with volume control and the speakers have clips with make it easy to mount to something.

![Kenji power bank](https://raw.githubusercontent.com/israelperez/heroquest/main/soundboard/kenji-powerbank-10000mah.jpg)

**Power bank**

I bought the Kenji 10,000 mAh power bank. This project doesn’t require much power. this one was cheap and had dual usb outs and came with a usb to micro-usb to power the board. If you want to use it the same 3d printable frame you’ll need to make sure your power bank is smaller than 144mm (L) x 70mm (W) x 15mm (H). You could use sponge material to wedge which ever one you use. Just make sure there is access to any on/off button, the usb ports and the recharge port.

## Documentation and acknowledgements

### NeoTrellis M4

https://learn.adafruit.com/adafruit-neotrellis-m4
It has a lot of information, and it can be overwhelming but it’s there incase you need it. For this project the step are really minor

### Examples

I used the following projects as a basis

- https://learn.adafruit.com/neotrellis-dungeon-crawl-soundboard
- https://learn.adafruit.com/star-trek-sound-board-with-neotrellism4

## Prepare the Audio files

With this project there is the option of using up to 32 different audio samples. and 1 intro welcome sample. All the files need to be in the same format. That is **16-bit PCM WAV** at **22,050 Hz** and they need to be either **all Stereo** or **all Mono**. No mix and match! if the non-matching samples are played it will shutdown the unit.

## Setting up the NeoTrellis

1.  update to the latest bootloader
    https://learn.adafruit.com/adafruit-neotrellis-m4/update-the-uf2-bootloader
    1. essentially is download the UF2 file.
    2. click the reset button on the back of the board once or twice depending on what’s already running on the board. you should see the NeoTrellis M4 come up as a new drive labelled **something...BOOT**
    3. drag and drop the bootloader UF2 into the new drive
2.  install the latest CircuitPython for NeoTrellis
    https://learn.adafruit.com/adafruit-neotrellis-m4/circuitpython
    1. essentially is download the UF2 file of CircuitPython that is specifically made for this board.
    2. Double click the reset button and a new drive will appear **something...BOOT**
    3. drag and drop the circuit python UF2 into the new drive
3.  add the latest versions of the libraries used in this project.
    https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/
    which one to download is based on which version of Circuit Python you are using. I’ve included version 7x in this repo as it was the stable version at the time of writing this.

    for this project you will need the following files and paste them into the **/lib** folder.

    - adafruit_fancyled **(whole folder)**
    - adafruit_trellism4.mpy
    - neopixel.mpy
    - adafruit_matrixkeypad.mpy

## Code and Audio Samples

You can download the entire contents of
https://github.com/israelperez/heroquest/tree/main/soundboard/NeoTrellis%20M4
and paste it into the root directory of the NeoTrellis. Just be aware that this code is using version 7.x of circuit python, so if you are using another version you will need to grab the correct libraries.

**Copyright Notice**
The audio samples here were gathered from various sources and thus have copyright. They were edited and combined to create these samples. They are only intended for personal use and can not be sold or distributed.

### Welcome and intro

If you want an intro with a swirling light effect, include **welcome.wav** in the root directory. The welcome file in this repo is mono, but you can use a stereo one. You’ll just have to edit **code.py**.

1. Uncomment line 39 (remove the # at the start)
   ```sh
   # with audioio.AudioOut(board.A1, right_channel=board.A0) as audio:
   ```
2. comment line 40 (add a # at the start)
   ```sh
   with audioio.AudioOut(board.A1) as audio:
   ```

### Samples

This project uses the file **soundboard.txt**. This file should be in the root directory of the NeoTrellis. The file defines what sounds files are available, which button on the NeoTrellis is used and the chosen colour of that button. All audio files should be in the **/samples** folder.

Each line is made up of a filename and a colour, separated by a comma. Colour names correspond to those in the **color_names.py** file.

The first line defined the sample used for the top left button. The next line defines the button to the right unless there are no more on the current row in which case it will defined the first button pf a new line. Blank lines and comments (lines starting with # are ignored. Spaces around the separating commas are also ignored. If the file can’t be found it will be replaced with a pass value

#### Keywords for filenames

**pass** : if the line is pass, this button will have no sound and will be black
**bgm\_** : if the filename starts with "bgm*" then the sample is played a different layer and it can played in the background and won’t be interrupted but other sound effects. only another file starting with "bgm*" will interrupt playback. Example: bgm*mission\_\_complete.wav
**loop** : (only applies to files with files that start with "bgm*") By adding "loop" to the end of a file, the soundboard will loop the playback of the sample. Example: bgm_ambience-loop.wav

#### soundboard.txt

```sh
combat_general__hit.wav, RED
combat_general__blocked.wav, RED
combat_general__miss.wav, RED
combat_death__male.wav, ORANGE
game_door__stone.wav, GREEN
game_door__wood.wav, GREEN
game_trap__pit.wav, TEAL
game_trap__spike.wav, TEAL

combat_magic__hit.wav, RED
combat_magic__miss.wav, RED
combat_death__monster.wav, ORANGE
combat_death__female.wav, ORANGE
music_turn__evil.wav, YELLOW
music_turn__heroes.wav, YELLOW
game_error__buzzer.wav, CHERRY
game_error__fail.wav, CHERRY

combat_axe__throw-hit.wav, RED
combat_axe__throw-block.wav, RED
combat_axe__throw-miss.wav, RED
magic_restore.wav, BLUE
game_item__found.wav, YELLOW
music_mission__goal-complete.wav, YELLOW
bgm_mission__complete.wav, PURPLE
bgm_mission__fail.wav, PURPLE

combat_arrow__fire-hit.wav, RED
combat_arrow__fire-block.wav, RED
combat_arrow__fire-miss.wav, RED
magic_buff.wav, BLUE
magic_debuff.wav, BLUE
pass
pass
pass
```

#### color_names.py

I’ve created and tested my own colour values, the ones it had predefined weren’t well defined or looked so similar that you couldn't tell they were different colours.

```sh
RED = 0xff0000
ORANGE = 0xd03100
YELLOW = 0xffff00
GREEN = 0x00ff00
AQUA = 0x00e022
TEAL = 0x00b04f
SKY = 0x008080
BLUE = 0x0000ff
PURPLE = 0x4000c0
LILAC = 0x710090
PINK = 0xb80047
CHERRY = 0xe80017
WHITE = 0xFFFFFF
BLACK = 0x000000
```

### Soundboard code

**code.py** is the brains of the soundboard

#### code.py

```sh
# SPDX-FileCopyrightText: 2018 Limor Fried for Adafruit Industries
# SPDX-License-Identifier: MIT
# Enhanced by Israel Perez

import time
import board
import audioio
import audiocore
import audiomixer
import adafruit_fancyled.adafruit_fancyled as fancy
import adafruit_trellism4
from color_names import * # pylint: disable=wildcard-import,unused-wildcard-import

PLAY_SAMPLES_ON_START = False
SELECTED_COLOR = WHITE
SAMPLE_FOLDER = "/samples/"  # the name of the folder containing the samples
SAMPLES = []

# For the intro, pick any number of colors to make a fancy gradient!
INTRO_SWIRL = [RED, GREEN, BLUE]

# Our keypad + neopixel driver
trellis = adafruit_trellism4.TrellisM4Express(rotation=0)

# load the sound & color specifications
with open("soundboard.txt", "r") as f:
    for line in f:
        cleaned = line.strip()
        if len(cleaned) > 0 and cleaned[0] != "#":
            if cleaned == "pass":
                SAMPLES.append(("does_not_exist.wav", BLACK))
            else:
                f_name, color = cleaned.split(",", 1)
                SAMPLES.append((f_name.strip(), eval(color.strip())))

# Play the welcome wav (if its there) and run intro sequence
# with audioio.AudioOut(board.A1, right_channel=board.A0) as audio: # stereo
with audioio.AudioOut(board.A1) as audio: # mono
    try:
        f = open("welcome.wav", "rb")
        wave = audiocore.WaveFile(f)
        audio.play(wave)
        swirl = 0  # we'll swirl through the colors in the gradient
        while audio.playing:
            for i in range(32):
                palette_index = ((swirl+i) % 32) / 32
                color = fancy.palette_lookup(INTRO_SWIRL, palette_index)
                # print(palette_index, fancy.denormalize(color)) display RGB values of swirl
                trellis.pixels[(i%8, i//8)] = color.pack()
            swirl += 1
            time.sleep(0.005)
        f.close()
        # Clear all pixels
        trellis.pixels.fill(0)
        # just hold a moment
        time.sleep(0.5)
    except OSError:
        # no welcome.wav file
        pass

# Parse the first file to figure out what format its in
channel_count = None
bits_per_sample = None
sample_rate = None
with open(SAMPLE_FOLDER+SAMPLES[0][0], "rb") as f:
    wav = audiocore.WaveFile(f)
    channel_count = wav.channel_count
    bits_per_sample = wav.bits_per_sample
    sample_rate = wav.sample_rate
    print("%d channels, %d bits per sample, %d Hz sample rate " %
          (wav.channel_count, wav.bits_per_sample, wav.sample_rate))

    # Audio playback object - we'll go with either mono or stereo depending on
    # what we see in the first file
    if wav.channel_count == 1:
        audio = audioio.AudioOut(board.A1)
    elif wav.channel_count == 2:
        audio = audioio.AudioOut(board.A1, right_channel=board.A0)
    else:
        raise RuntimeError("Must be mono or stereo waves!")

mixer = audiomixer.Mixer(voice_count=2,
    sample_rate=sample_rate,
    channel_count=channel_count,
    bits_per_sample=bits_per_sample,
    samples_signed=True)
audio.play(mixer)

# Clear all pixels
trellis.pixels.fill(0)

# Light up button with a valid sound file attached
for i, v in enumerate(SAMPLES):
    filename = SAMPLE_FOLDER+v[0]
    try:
        with open(filename, "rb") as f:
            wav = audiocore.WaveFile(f)
            print(filename,
                  "%d channels, %d bits per sample, %d Hz sample rate " %
                  (wav.channel_count, wav.bits_per_sample, wav.sample_rate))
            if wav.channel_count != channel_count:
                pass
            if wav.bits_per_sample != bits_per_sample:
                pass
            if wav.sample_rate != sample_rate:
                pass
            trellis.pixels[(i%8, i//8)] = v[1]
            if PLAY_SAMPLES_ON_START:
                audio.play(wav)
                while audio.playing:
                    pass
    except OSError:
        # File not found! skip to next
        if filename != SAMPLE_FOLDER+"does_not_exist.wav":
            print('Not found: ' + filename)
        pass

def stop_playing_sample(playback_details):
    print("playing: ", playback_details)
    mixer.stop_voice(playback_details["voice"])
    trellis.pixels[playback_details["neopixel_location"]] = playback_details["neopixel_color"]
    playback_details["file"].close()
    playback_details["voice"] = None
    playback_details["sample_num"] = None

current_press = set()
current_background = {"voice" : None, "sample_num": None}
currently_playing = {"voice" : None}
#last_samplenum = None
while True:
    pressed = set(trellis.pressed_keys)
    just_pressed = pressed - current_press

    for down in just_pressed:
        sample_num = down[1]*8 + down[0]
        try:
            filename = SAMPLE_FOLDER+SAMPLES[sample_num][0]
            f = open(filename, "rb")
            wav = audiocore.WaveFile(f)
            print(sample_num, filename)
            # Check to see if its background music
            if filename[9:13] == "bgm_":
                # Check if sample is already playing then stop it
                if current_background["sample_num"] == sample_num:
                    stop_playing_sample(current_background)
                    break
                # Check to see if it needs to loop
                will_loop = False
                file_name = filename.split(".")[0]
                if file_name[len(file_name) -4:] == "loop":
                    will_loop = True
                if current_background["voice"] != None:
                    print("Interrupt")
                    stop_playing_sample(current_background)
                trellis.pixels[down] = WHITE
                mixer.play(wav, voice=0, loop=will_loop)
                current_background = {
                    "voice": 0,
                    "neopixel_location": down,
                    "neopixel_color": SAMPLES[sample_num][1],
                    "sample_num": sample_num,
                    "file": f}
            else:
                if currently_playing["voice"] != None:
                    print("Interrupt")
                    stop_playing_sample(currently_playing)
                trellis.pixels[down] = WHITE
                mixer.play(wav, voice=1, loop=False)
                currently_playing = {
                    "voice": 1,
                    "neopixel_location": down,
                    "neopixel_color": SAMPLES[sample_num][1],
                    "sample_num": sample_num,
                    "file": f}
        except OSError:
            pass # File not found! skip to next

    # check if any samples are done
    if not mixer.playing:
        if currently_playing["voice"] != None:
            stop_playing_sample(currently_playing)
        if current_background["voice"] != None:
            stop_playing_sample(current_background)

    time.sleep(0.01)  # a little delay here helps avoid debounce annoyances
    current_press = pressed
```

## Ready to use

Your soundboard is now ready to use how ever you want to. You'll notice pressing the button a second time will stop playback of that sample of the same layer. Pressing a new button will interrupt the currently playing sample of the same layer. Files starting with bgm\_ will play on one layer and all other files on another.

## Assembling the Portable solution

This frame uses 8x M3x6mm screws and 2x M3x16mm screws.
you will also need zip ties no wider than 4mm.
Once you print all the parts, test fit the parts, you may need to remove material from the tabs due to elephants’ foot or inaccuracies in your printer.

Assemble in the following order. (Images to come soon)

1. Combine the **speaker mount** to the **battery mount** with 2x M3x6mm screws.
2. Now combine **side B** using another 2 M3x6mm screws.
3. now add the part **cable tidy** with 1x M3x6mm screw. at this stage you can attach the speakers and start wiring, use the protrusions the wrap the wires. leave enough slack to be able to remove the speakers if need be. The side part has a part where you can zip tie the volume control to it. Ensure the volume dial is facing upwards. Continue to wrap the cable using zip ties as need be. leave enough slack on the other end to be able to plug the cables into the device and power bank.
4. Now add **side A** with 2 more M3x6mm screws.
5. time to prepare the NeoTrellis. remove the 2 side screws if you fully assembled it. use these holes and the 2x M3x16mm screws to attach it to **M4 mount**. there is also a hole for a zip tie so you can pass the 3.5mm audio jack and micro usb through. I didn’t tighten its but kept it as s lose loop.
6. Finally push the **M4 mount** with the NeoTrellis into the sides making sure the ports are on the speaker side.
