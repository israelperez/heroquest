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
