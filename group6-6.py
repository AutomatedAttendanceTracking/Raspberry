import pifacecad
import os
import signal
import qrtools
import requests
import time

urls = []

# you can ignore these three lines of code
# they are needed so that you can end the
# program by pressing Ctrl+C
def signal_handler(signal, frame):
	os._exit(0)
signal.signal(signal.SIGINT, signal_handler)

# event handler that is called after a button is
# pressed. The event handler is linked to the
# button press by listener.register(...) below
def scanQR(event):
	print 'Start Scanning'
	qr = qrtools.QR()
	qr.decode_webcam()
	timestamp = str(time.time()).split('.')[0]+'000'
	send(timestamp, qr.data)
	print 'Stopped Scanning'

def send(timestamp, qrCode):
	global urls
	studentNumber, randomNumber = qrCode.split(',')
	url = 'https://aat6-6.appspot.com/qrcode/valid/'+ studentNumber + '/'+ timestamp + '/' + randomNumber
	print url
	r = requests.put(url)
	if (r.status_code != 200):
		print 'Send failed'
		urls.append(url)

def retry(event):
	global urls
	print 'Retrying...'
	urls2 = []
	for url in urls:
		r = request.put(url)
		if(r.status_code != 200):
			print('Retry failed for ' + url)
			urls2.append(url)
	urls = urls2
		
cad = pifacecad.PiFaceCAD()
listener = pifacecad.SwitchEventListener(chip=cad)
# the display has eight buttons: 
# five dip switchtes 
# left, right and push for the three-way dip dwitch
listener.register(0, pifacecad.IODIR_FALLING_EDGE, scanQR)
listener.register(1, pifacecad.IODIR_FALLING_EDGE, retry)
listener.activate()
