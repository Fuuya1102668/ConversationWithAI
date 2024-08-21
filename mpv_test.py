import mpv
import time

player = mpv.MPV(volume=0, loop="inf", fullscreen=True)

player.play("dottimo.mp4")

while True:
    time.sleep(2)
    if player.pause:
        player.pause = False
    else:
        player.pause = True

player.wait_for_playback()

