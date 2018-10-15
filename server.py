#! /usr/bin/python

import os.path
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import time
from neopixel import *
import argparse
import json

#Initialize Raspberry PI GPIO
# LED strip configuration:
LED_COUNT = 12      # Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10       # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
LED_CHANNEL    = 0
LED_STRIP      = ws.SK6812_STRIP_RGBW

#Tornado Folder Paths
settings = dict(
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "static")
    )

#Tonado server port
PORT = 80

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
strip.begin()

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def rgb2hex(r,g,b):
    hex = "#{:02x}{:02x}{:02x}".format(r,g,b)
    return hex

def hex2rgb(hexcode):
    rgb = tuple(map(ord,hexcode[1:].decode('hex')))
    return rgb

def hex_to_rgb(hex):
     hex = hex.lstrip('#')
     hlen = len(hex)
     return tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print("[HTTP](MainHandler) User Connected.")
        self.render("index.html")
    
class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("[WS] Connection was opened.")
 
    def on_message(self, message):
        print("[WS] Incoming message:", message)

        obj = json.loads(message)
        if obj["cmd"] == "led":
            rgb = hex_to_rgb(obj["data"])
            print(hex_to_rgb(obj["data"]))

            if rgb[0] == rgb[1] == rgb[2]:
                for i in range(strip.numPixels()):
                    strip.setPixelColor(i, Color(0,0,0, rgb[2]))
                strip.show()
            else:
                for i in range(strip.numPixels()):
                    strip.setPixelColor(i, Color(rgb[1], rgb[0], rgb[2]))
                strip.show()

    def on_close(self):
        print("[WS] Connection was closed.")
    

application = tornado.web.Application([
    (r'/', MainHandler),
    (r'/ws', WSHandler),
    ], **settings)


if __name__ == "__main__":
    try:
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(PORT)
        main_loop = tornado.ioloop.IOLoop.instance()

        print("Tornado Server started")
        main_loop.start()

    except:
        print("Exception triggered - Tornado Server stopped.")
        colorWipe(strip, Color(0,0,0), 10)

#End of Program
