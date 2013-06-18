from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
import urllib2
import subprocess
import piface.pfio as pfio
from os import path
from urlparse import urlparse
from urlparse import parse_qs
 
class SondeHandler(BaseHTTPRequestHandler):
        def do_GET(self):
                try:
                        self.send_response(200)
                        parsed=parse_qs(urlparse(self.path).query)
                        pfio.digital_write(int(parsed['i'].pop()), int(parsed['s'].pop()))
                        rep="C'est fait"
                        self.send_header('Content-Type','text/html')
                except Exception, e:
                        self.send_response(500)
                        self.send_header('Content-Type','text/html')
                        rep="ERROR : "+str(e)
                       
                self.end_headers()
                self.wfile.write(rep)
 
        def execScript(self,arg):
                print arg
                value=str(subprocess.check_output(arg).strip())
                return value
 
class myHTTPServer(HTTPServer):
 
        def __init__(self, *args, **kw):
                self.port=args[0][1]
                HTTPServer.__init__(self, *args, **kw)
                self.stopHTTP=False
 
        def serve_forever(self):
                while ( self.stopHTTP == False):
                        self.handle_request()
 
       
 
class SondeHTTP():
 
        def __init__(self):
                self.port=8080
                pfio.init()
                print 'Start HTTP server on '+str(self.port)
                self.server = myHTTPServer(('',self.port),SondeHandler)
                self.server.serve_forever()
                print 'Stop HTTP server on '+str(self.port)