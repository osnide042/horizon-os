#!/usr/bin/python3
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import json,os,subprocess
ROOT='/opt/horizon'; STATE='/var/lib/horizon/state/device.json'
class Api(SimpleHTTPRequestHandler):
 def translate_path(self,path):
  requested=path.split('?',1)[0].lstrip('/') or 'index.html';target=os.path.realpath(os.path.join(ROOT,requested));root=os.path.realpath(ROOT)+os.sep
  return target if target.startswith(root) else os.path.join(ROOT,'index.html')
 def do_GET(self):
  if self.path=='/api/system':
   saved={}
   try: saved=json.load(open(STATE))
   except: pass
   data={'hostname':os.uname().nodename,'deviceName':saved.get('deviceName','Horizon'),'setup':os.path.exists(STATE),'platform':'Horizon OS Preview 0.5'};body=json.dumps(data).encode();self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body);return
  super().do_GET()
 def do_POST(self):
  if self.path=='/api/setup':
   size=int(self.headers.get('Content-Length','0'));data=json.loads(self.rfile.read(size) or b'{}');os.makedirs(os.path.dirname(STATE),exist_ok=True);open(STATE,'w').write(json.dumps({'deviceName':data.get('deviceName','Horizon'),'complete':True}));self.send_response(204);self.end_headers();return
  if self.path=='/api/power':
   size=int(self.headers.get('Content-Length','0'));data=json.loads(self.rfile.read(size) or b'{}');action=data.get('action');self.send_response(204);self.end_headers()
   if action=='restart': subprocess.Popen(['/usr/bin/systemctl','reboot'])
   elif action=='poweroff': subprocess.Popen(['/usr/bin/systemctl','poweroff'])
   return
  self.send_error(404)
 def log_message(self,*args): pass
os.chdir(ROOT);ThreadingHTTPServer(('127.0.0.1',4782),Api).serve_forever()
