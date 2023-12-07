import subprocess,re,time
def devices():
  result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
  output = result.stdout
  if 'List of devices attached' in output:
      devices = output.split('\n')[1:-2]
      num_devices = len(devices)
      if num_devices < 1:
        return ['']
      else:
        list_devices=[]
        for get_devices in range(0,num_devices):
          list_devices.append(devices[get_devices].split('\t')[0])
        return list_devices
class click:
  def __init__(self,devices,x,y):
    result = subprocess.run(['adb', '-s',str(devices),'shell','input','tap',str(x),str(y)], capture_output=True, text=True)
    self.devices=devices
    self.output = result.stdout
  def send_key(self,text):
    keycodes = {
        'a': 29, 'b': 30, 'c': 31, 'd': 32, 'e': 33, 'f': 34, 'g': 35, 'h': 36, 'i': 37,
        'j': 38, 'k': 39, 'l': 40, 'm': 41, 'n': 42, 'o': 43, 'p': 44, 'q': 45, 'r': 46,
        's': 47, 't': 48, 'u': 49, 'v': 50, 'w': 51, 'x': 52, 'y': 53, 'z': 54,
        '0': 7, '1': 8, '2': 9, '3': 10, '4': 11, '5': 12, '6': 13, '7': 14, '8': 15, '9': 16,' ':62
    }
    list_keyevents = [str(keycodes[c]) for c in text if c in keycodes]
    str_keyevents=''
    for key in list_keyevents:
      keyevents =str_keyevents+str(key)+' '
      str_keyevents =keyevents
    result = subprocess.run(['adb', '-s',str(self.devices),'shell','input','keyevent ',str_keyevents], capture_output=True, text=True)
    return str_keyevents
  def __str__(self):
    return self.output
    
def screen_photo(devices,address_file_name):
  result = subprocess.run(['adb', '-s',str(devices),'shell','screencap',str(address_file_name)], capture_output=True, text=True)
  output = result.stdout
  if 'error' in output:
    return 'file address does not exist'
  else:
    return True
def create_xml(devices,address_file_name):
  result=subprocess.run(['adb','-s',
  str(devices),'shell','uiautomator','dump',address_file_name], capture_output=True, text=True)
  return result.stdout
def open_app(devices,name_package_app):
  result=subprocess.run(['adb','-s',
  str(devices),'shell','monkey','-p',name_package_app,'-c','android.intent.category.LAUNCHER','1'], capture_output=True, text=True)
def open_url(devices,url):
  result=subprocess.run(['adb','-s',
  str(devices),'shell','am','start','-a android.intent.action.VIEW','-d',f'"{url}"'], capture_output=True, text=True)
  return result.stdout
def wait(element,second):
  import time
  try:
    int(second)
  except:
    return 'int not str'
  for s in range(0,second):
    time.sleep(1)
    if element.status=='True':
      break
    else:
      continue