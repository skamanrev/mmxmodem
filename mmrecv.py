#!/usr/local/bin/python3
import sys
from os import remove, rename, unlink
from os.path import isfile, dirname, realpath
from time import sleep
import logging
import serial
from xmodem import XMODEM

real_path = dirname(realpath(__file__))
sys.path.insert(0, real_path + '/modules')
from mmconnect import mmconnect


if len(sys.argv) < 3:
  print ('Usage: ' + sys.argv[0] + ' <serial-port> <source-filename> [<local-filename>]\n')
  quit()

sp = sys.argv[1]
fn = sys.argv[2]
dfn = fn
if len(sys.argv) == 4: dfn = sys.argv[3]

try:
    stream = open(dfn+'.incoming', 'wb')
except:
    print ('Oops! Could not create local file %s\n' % (fn))
    quit()
    
def getc(size, timeout=1):
  data = s.read(size)
  return data or None
def putc(data, timeout=1):
  sent = s.write(data)
  s.flush()
  return sent or None
xmodem = XMODEM(getc, putc)

log = logging.getLogger()
log.setLevel(logging.WARNING)
ch = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

s = mmconnect(sp)

print ("Picomite connected. Setting up XMODEM transfer ...")

xmodemSend='xmodem send "' + fn + '"\r'
s.write(xmodemSend.encode())
sleep(0.2)
e = s.readline(); # our own command is echoed back first
e = s.readline(); # should timeout if no error on MM side
if e[:18] == "Error: Cannot":
    print ('Oops! Remote file %s not found!' % (fn))
    s.close()
    stream.close()
    remove(dfn+'.incoming')
    quit()
    
sleep(0.5)
s.flushInput()

print ('Receiving  ' + fn + ' as ' + dfn + ' ...')

bytes = xmodem.recv(stream, quiet=0, retry=8)
stream.close()

if (bytes != None):
    if isfile(dfn): unlink(dfn)
    rename(dfn+'.incoming', dfn)
    print ("Done! (%d bytes received)\n" % (bytes))
else:
    print ("There could be a problem :-(\n")
    if (bytes == 0):
        remove(dfn+'.incoming')
    else:
        print ("Partial(?) transfer retained in: %s.incoming" % (dfn))
    quit();

s.close()
