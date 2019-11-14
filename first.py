import os
import shutil
import getpass
from http.server import BaseHTTPRequestHandler, HTTPServer
PORT = 8000

#Наследуем класс от basehttprequesthandler
class MyHttpRequestHandler(BaseHTTPRequestHandler):
  def send_head(self):
    self.send_response(200) #успешный запрос
    self.send_header('content-type','text/html')
    self.end_headers()
            
  def do_GET(self):
    mdir = format(self.path)[1:] #Получаем путь
    self.send_head()
    if mdir[0:2] == "r/":    #remove
      try:
        os.remove(mdir[2:])          
      except OSError:
        if os.listdir(mdir[2:]) == []:
          os.rmdir(mdir[2:])     
    elif mdir[0:2] == "d/":  #download
      file_name = ''
      mdir = mdir[2:]
      for ch in mdir:
        if ch == '/': break
        file_name = file_name + ch 
      url = mdir[len(file_name) + 1:] + '/' + file_name
      shutil.copy(url, 'C:/users/' + getpass.getuser() + '/downloads/', follow_symlinks=True)   #копируем файл в загрузки                 
    else:
      files = os.listdir(mdir)
      s = ''
      for i in files:
        s += i + '<br/>'
    self.wfile.write(('<meta charset="UTF-8"/>' + s).encode())

serv = HTTPServer(("localhost", PORT),MyHttpRequestHandler)
print("serving at port", PORT)
serv.serve_forever()