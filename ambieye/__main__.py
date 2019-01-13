#!/usr/bin/python
import picamera
import utils.dominantcolor as dominantcolor

with picamera.PiCamera() as camera:
    camera.capture("snapshot.jpg")
    dominantcolor.get_dominant_color("snapshot.jpg")
