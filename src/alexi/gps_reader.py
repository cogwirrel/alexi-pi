import os
import gps
import arrow
from threading import Thread
import alexi.server as server

class GpsListener(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.gps_listener = gps.gps(mode=gps.WATCH_ENABLE)
        self.active = True
 
    def run(self):
        while self.active:
            # Get updates gps_listener with the latest data
            try:
                self.gps_listener.next()

                server.send_gps({
                    'latitude': self.gps_listener.fix.latitude,
                    'longitude': self.gps_listener.fix.longitude,
                    'altitude': self.gps_listener.fix.altitude,
                    'speed': self.gps_listener.fix.speed,
                    'climb': self.gps_listener.fix.climb,
                    'track': self.gps_listener.fix.track,
                    'timestamp': self.gps_listener.utc,
                })
            except StopIteration as e:
                pass


    def get(self):
        return self.gps_listener

    def stop(self):
        self.active = False
 

_gps_listener = None

def start():
    global _gps_listener
    if _gps_listener is not None:
        _gps_listener.stop()
    
    _gps_listener = GpsListener()
    _gps_listener.start()

def get_data():
    global _gps_listener
    gps_info = _gps_listener.get()

    return {
        'latitude': gps_info.fix.latitude,
        'longitude': gps_info.fix.longitude,
        'altitude': gps_info.fix.altitude,
        'speed': gps_info.fix.speed,
        'climb': gps_info.fix.climb,
        'track': gps_info.fix.track,
        'timestamp': gps_info.utc,
    }

def stop():
    global _gps_listener
    _gps_listener.stop()
    _gps_listener = None