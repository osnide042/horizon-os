#!/usr/bin/python3
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import json, os, shutil, subprocess, threading, time, urllib.request

ROOT='/opt/horizon'
STATE='/var/lib/horizon/state/device.json'
APPS='/var/lib/horizon/state/apps.json'
FLATPAKS={'steam':'com.valvesoftware.Steam'}
WEB_APPS={'netflix':'https://www.netflix.com/','youtube':'https://www.youtube.com/'}
STEAM_GAMES={
 'steam-cs2':'730',
 'steam-dota2':'570',
 'steam-tf2':'440',
 'steam-warframe':'230410',
 'steam-brawlhalla':'291550',
 'steam-apex':'1172470',
 'steam-halo-infinite':'1240440',
 'steam-destiny2':'1085660'
}

def steam_command(uri):
 return ['/usr/sbin/runuser','-u','horizon','--','env','DISPLAY=:0','XAUTHORITY=/home/horizon/.Xauthority','flatpak','run','com.valvesoftware.Steam',uri]

def steam_installed_ids():
 roots=[
  '/home/horizon/.var/app/com.valvesoftware.Steam/.local/share/Steam/steamapps',
  '/home/horizon/.steam/steam/steamapps'
 ]
 appids=set()
 for root in roots:
  if not os.path.isdir(root): continue
  for name in os.listdir(root):
   if name.startswith('appmanifest_') and name.endswith('.acf'):
    appids.add(name[12:-4])
  library_file=os.path.join(root,'libraryfolders.vdf')
  try:
   with open(library_file,errors='ignore') as f: content=f.read()
   import re
   for path in re.findall(r'"path"\s+"([^"]+)"',content):
    manifest_root=os.path.join(path.replace('\\\\','/'),'steamapps')
    if os.path.isdir(manifest_root):
     for name in os.listdir(manifest_root):
      if name.startswith('appmanifest_') and name.endswith('.acf'): appids.add(name[12:-4])
  except: pass
 return [game for game,appid in STEAM_GAMES.items() if appid in appids]

def read_json(path, fallback):
 try:
  with open(path) as f: return json.load(f)
 except: return fallback

def write_json(path, data):
 os.makedirs(os.path.dirname(path),exist_ok=True)
 with open(path,'w') as f: json.dump(data,f)

class Api(SimpleHTTPRequestHandler):
 def translate_path(self,path):
  requested=path.split('?',1)[0].lstrip('/') or 'index.html'
  target=os.path.realpath(os.path.join(ROOT,requested)); root=os.path.realpath(ROOT)+os.sep
  return target if target.startswith(root) else os.path.join(ROOT,'index.html')

 def reply(self,code,data=None):
  body=b'' if data is None else json.dumps(data).encode()
  self.send_response(code)
  if body: self.send_header('Content-Type','application/json')
  self.send_header('Content-Length',str(len(body))); self.end_headers()
  if body: self.wfile.write(body)

 def body(self):
  size=int(self.headers.get('Content-Length','0'))
  return json.loads(self.rfile.read(size) or b'{}')

 def do_GET(self):
  if self.path=='/api/system':
   saved=read_json(STATE,{})
   self.reply(200,{'hostname':os.uname().nodename,'deviceName':saved.get('deviceName','Horizon'),'setup':os.path.exists(STATE),'platform':'Horizon Desktop Preview 1.0'})
   return
  if self.path=='/api/apps':
   installed=set(read_json(APPS,[]))
   try:
    out=subprocess.run(['flatpak','list','--system','--app','--columns=application'],capture_output=True,text=True,timeout=20)
    flat=set(out.stdout.splitlines())
    for key,value in FLATPAKS.items():
     if value in flat: installed.add(key)
    installed.update(steam_installed_ids())
   except: pass
   self.reply(200,{'installed':sorted(installed)}); return
  super().do_GET()

 def do_POST(self):
  if self.path=='/api/setup':
   data=self.body(); write_json(STATE,{'deviceName':data.get('deviceName','Horizon'),'complete':True}); self.reply(204); return
  if self.path=='/api/apps/install':
   app=self.body().get('app','')
   if app in FLATPAKS or app in STEAM_GAMES:
    subprocess.run(['flatpak','remote-add','--system','--if-not-exists','flathub','https://dl.flathub.org/repo/flathub.flatpakrepo'],capture_output=True,timeout=60)
    installed_apps=subprocess.run(['flatpak','list','--system','--app','--columns=application'],capture_output=True,text=True,timeout=30).stdout.splitlines()
    if 'com.valvesoftware.Steam' not in installed_apps:
     result=subprocess.run(['flatpak','install','--system','--noninteractive','-y','flathub','com.valvesoftware.Steam'],capture_output=True,text=True,timeout=1800)
     if result.returncode: self.reply(500,{'error':(result.stderr or result.stdout)[-500:]}); return
    if app in STEAM_GAMES:
     subprocess.Popen(steam_command('steam://install/'+STEAM_GAMES[app]),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)
     self.reply(200,{'installingViaSteam':True}); return
   elif app=='netflix':
    if not shutil.which('google-chrome-stable'):
     package='/tmp/google-chrome-stable_current_amd64.deb'
     try: urllib.request.urlretrieve('https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb',package)
     except Exception as error: self.reply(500,{'error':'Could not download Google Chrome: '+str(error)}); return
     result=subprocess.run(['apt-get','install','-y',package],capture_output=True,text=True,timeout=900)
     if result.returncode: self.reply(500,{'error':(result.stderr or result.stdout)[-500:]}); return
   elif app not in WEB_APPS: self.reply(400,{'error':'Unknown Horizon Store app'}); return
   installed=set(read_json(APPS,[])); installed.add(app); write_json(APPS,sorted(installed)); self.reply(200,{'installed':True}); return
  if self.path=='/api/apps/uninstall':
   app=self.body().get('app','')
   if app in FLATPAKS: subprocess.run(['flatpak','uninstall','--system','--noninteractive','-y',FLATPAKS[app]],capture_output=True,timeout=900)
   elif app in STEAM_GAMES: subprocess.Popen(steam_command('steam://uninstall/'+STEAM_GAMES[app]),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)
   installed=set(read_json(APPS,[])); installed.discard(app); write_json(APPS,sorted(installed)); self.reply(200,{'installed':False}); return
  if self.path=='/api/apps/launch':
   app=self.body().get('app','')
   env=['/usr/sbin/runuser','-u','horizon','--','env','DISPLAY=:0','XAUTHORITY=/home/horizon/.Xauthority']
   if app in STEAM_GAMES: command=steam_command('steam://rungameid/'+STEAM_GAMES[app])
   elif app in FLATPAKS: command=env+['flatpak','run',FLATPAKS[app]]
   elif app in WEB_APPS:
    browser='google-chrome-stable' if app=='netflix' else 'chromium'
    command=env+[browser,'--user-data-dir=/home/horizon/.config/horizon-apps/'+app,'--app='+WEB_APPS[app],'--start-fullscreen','--no-first-run','--disable-session-crashed-bubble','--disable-features=Translate']
   else: self.reply(400,{'error':'App is not available'}); return
   process=subprocess.Popen(command,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)
   write_json('/run/horizon-active-app.json',{'pid':process.pid,'app':app,'close_on_escape':app in WEB_APPS})
   self.reply(200,{'launched':True}); return
  if self.path=='/api/power':
   action=self.body().get('action'); self.reply(204)
   if action in ('restart','poweroff'):
    command='reboot' if action=='restart' else 'poweroff'
    threading.Thread(target=lambda:(time.sleep(.5),subprocess.run(['/usr/bin/systemctl',command])),daemon=True).start()
   return
  self.reply(404,{'error':'Not found'})

 def log_message(self,*args): pass

os.chdir(ROOT)
ThreadingHTTPServer(('127.0.0.1',4782),Api).serve_forever()
