#!/usr/bin/python3
import json, os, select, signal, time
from evdev import InputDevice, list_devices, ecodes

ACTIVE='/run/horizon-active-app.json'

def close_active(escape=False):
 try:
  with open(ACTIVE) as f: app=json.load(f)
  if escape and not app.get('close_on_escape',False): return
  pid=int(app.get('pid',0))
  if pid:
   try: os.killpg(pid,signal.SIGTERM)
   except ProcessLookupError: pass
  try: os.unlink(ACTIVE)
  except FileNotFoundError: pass
 except: pass

def devices():
 found=[]
 for path in list_devices():
  try:
   dev=InputDevice(path)
   keys=dev.capabilities().get(ecodes.EV_KEY,[])
   if ecodes.KEY_ESC in keys or ecodes.BTN_MODE in keys: found.append(dev)
  except: pass
 return found

current=[]
while True:
 if not current: current=devices()
 try:
  ready,_,_=select.select(current,[],[],2)
  for dev in ready:
   for event in dev.read():
    if event.type!=ecodes.EV_KEY or event.value!=1: continue
    if event.code==ecodes.KEY_ESC: close_active(escape=True)
    elif event.code==ecodes.BTN_MODE: close_active(escape=False)
 except: current=[]; time.sleep(1)
