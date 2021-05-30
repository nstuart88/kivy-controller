from kivy.utils import platform
if (platform == "android"):
	from jnius import *
	WifiManager = autoclass('android.net.wifi.WifiManager')
	WifiInfo = autoclass('android.net.wifi.WifiInfo')
	PythonActivity = autoclass('org.kivy.android.PythonActivity')
	Intent = autoclass('android.content.Intent')
	Context = autoclass('android.content.Context')
	ConnectionManager = autoclass('android.net.ConnectivityManager')
	WifiConfiguration = autoclass('android.net.wifi.WifiConfiguration')
	String = autoclass('java.lang.String')
	Uri = autoclass('android.net.Uri')
	context1 = Context.WIFI_SERVICE
	activity = PythonActivity.mActivity
	wifiA = WifiInfo
	wifiB = WifiManager
	
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.joystick import Joystick
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.properties import DictProperty
from kivy.properties import ListProperty
from kivy.properties import OptionProperty
from kivy.clock import Clock
import threading
import sys
import time
import socket
import subprocess
import os
from time import sleep

	
	


kv = '''

BoxLayout:
	#on_size: if app.runServer.is_alive() == False: app.runServer.start()
	id: main_box
	orientation: 'vertical'
	padding: 5
		
	GridLayout:
		spacing: 10
		#id: box1
		cols:1
		rows:6
	#	padding: [100,10,100,100]
		#orientation: 'vertical'
		size_hint:1,.3
		
		Label:
			text: app.data
			size_hint:1,.3
		Label:
			text: app.my_ssid
			size_hint:1,.1
		Label:
			text: app.my_rssi
			size_hint:1,.1
		
		Button:
			id: startBtn
			#pad_y: '100px'
			text: 'Start / Reset'
			size_hint:1,.1
			on_press: app.button_state('startBtn',1)
			on_release: app.button_state('startBtn',0)
			
		
		Button:
			id: cntrlBtn
			text: 'Take Control'
			size_hint:1,.1
			on_press: app.button_state('cntrlBtn',1)
			on_release: app.button_state('cntrlBtn',0)

		ToggleButton:
		    id: lockControls
		    text: 'lock controls'
		    size_hint:1,.1
		    on_state: if self.state == 'down': \
		    app.toggle_state('1') 
		    on_state: if self.state == 'normal': \
		    app.toggle_state('0')		    		
		    	
	GridLayout:
        spacing: .1
        cols: 3
        rows: 5
	    size_hint:1,.3
	    padding: [0,200,0,0]
	    
	    Label:
			bold: True
			outline_color:(200,200,200)
			text: 'Port Spud'
		#	halign: 'center'
	#		valign:'middle'
			size_hint:.5,.1
			
		Label:
			bold: True
			outline_color:(200,200,200)
			text: 'Stern Spud'
			#halign: 'center'
			#valign:'middle'
			size_hint:.1,.1
			
		Label:
			bold: True
			outline_color:(200,200,200)
			text: 'Stbd  Spud'
		#	halign: 'center'
	#		valign:'middle'
			size_hint:.1,.1
		
		Joystick:
			id: portJoy
			size_hint:1,.1
			#halign: 'left'
		#	valign:'top'
			sticky: False
			outer_size: .50
			inner_size: 0.45
			pad_size: 0.4
			outer_line_width: 0.01
			inner_line_width: 0.01
			pad_line_width: 0.01
			outer_background_color: (0.75, 0.75, 0.75, 0.3)
			outer_line_color: (0.25, 0.25, 0.25, 0.3)
			inner_background_color: (0.75, 0.75, 0.75, 0.5)
			inner_line_color: (0.7, 0.7, 0.7, 0.1)
			pad_background_color: (0.1, .8, 0.1, 1)
			pad_line_color: (0.35, 0.35, 0.35, 1)
			touch_is_active: app.update_coordinates(portJoy, portJoy.pad, 1,0,0)
			
		Joystick:
			id: sternJoy
			#halign: 'right'
		    #valign:'top'
			sticky: False 
			outer_size: .50
			inner_size: 0.45
			pad_size: 0.4
			outer_line_width: 0.01 
			inner_line_width: 0.01 
			pad_line_width: 0.01
			outer_background_color: (0.75, 0.75, 0.75, 0.3)
			outer_line_color: (0.25, 0.25, 0.25, 0.3)
			inner_background_color: (0.75, 0.75, 0.75, 0.5)
			inner_line_color: (0.7, 0.7, 0.7, 0.1)
			pad_background_color: (0.1, .8, 0.1, 1)
			pad_line_color: (0.35, 0.35, 0.35, 1)
			touch_is_active: app.update_coordinates(sternJoy, sternJoy.pad, 0,0,1)
			
		Joystick:
			id: stbdJoy
		#	halign: 'right'
			sticky: False 
			outer_size: .50
			inner_size: 0.45
			pad_size: 0.4
			outer_line_width: 0.01 
			inner_line_width: 0.01 
			pad_line_width: 0.01
			outer_background_color: (0.75, 0.75, 0.75, 0.3)
			outer_line_color: (0.25, 0.25, 0.25, 0.3)
			inner_background_color: (0.75, 0.75, 0.75, 0.5)
			inner_line_color: (0.7, 0.7, 0.7, 0.1)
			pad_background_color: (0.1, .8, 0.1, 1)
			pad_line_color: (0.35, 0.35, 0.35, 1)
			touch_is_active: app.update_coordinates(stbdJoy, stbdJoy.pad, 0,1,0)
			
		
#		Label:
#			bold: True
#			text: app.portJoyString
#			size_hint:1,.75
#		Label:
#			bold: True
#			text: app.sternJoyString
#			size_hint:1,.75
#		Label:
#			bold: True
#			text: app.stbdJoyString
#			size_hint:1,.75

'''

class spudControlsApp(App):
	wifiMain = cast(WifiManager, activity.getSystemService(context1))
	wifiCurrent = wifiMain.getConnectionInfo()
	ssid = wifiCurrent.getSSID()
	rssi = wifiCurrent.getRssi()
	print(ssid)
	print(rssi)
	portJoy = ObjectProperty(Joystick())
	stbdJoy = ObjectProperty(Joystick())
	sternJoy = ObjectProperty(Joystick())
	
	#lockControls = ObjectProperty(ToggleButton())
	cntrlBtn = ObjectProperty(Button())
	startBtn = ObjectProperty(Button())
	portJoyString = StringProperty()
	stbdJoyString = StringProperty()
	sternJoyString =StringProperty()
	dataString = StringProperty()
	my_rssi = StringProperty()
	my_ssid = StringProperty()
	data = StringProperty()
	buttonState = '0'
	startBtn_state = '0'
	cntrlBtn_state = '0'
	port = '0'
	stbd = '0'
	stern = '0'
	wifiKey = 'Dp_Dredge'
	#wifiKey = '
	connected = 0
		
	def connect(self):
		self.ssid = self.wifiCurrent.getSSID()
		self.rssi = self.wifiCurrent.getRssi()
		self.my_rssi = str(self.rssi)
		self.my_ssid = str(self.ssid)
		time.sleep(1)
		print('back in connect mainloop')
		#connected= 
		#HOST=''
		HOST = '192.168.1.140'
		PORT = 6543
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM)as s:
		  while self.connected == 0:
		  	#s.setblocking(0)
		  	print('connecting....')
		  	s.connect((HOST, PORT))
		  	self.connected = 1
		  	print('connected!!')
		  while self.connected == 1:
		  	try:
		  		s.sendall(self.dataString.encode('ascii'))
		  		time.sleep(.01)
		  		self.data = s.recv(1024).decode('utf-8')
		  		#time.sleep(.01)
		  		self.wifiCurrent = self.wifiMain.getConnectionInfo()
		  		self.rssi = self.wifiCurrent.getRssi()
		  		self.ssid = self.wifiCurrent.getSSID()
		  		self.my_rssi = str(self.rssi)
		  		self.my_ssid = str(self.ssid)
		  		
		  		
		  	except BrokenPipeError as e:
		  		while True:
			  		print('broken pipe')
			  		time.sleep(5)
			  		self.wifiCurrent = self.wifiMain.getConnectionInfo()
			  		self.ssid = self.wifiCurrent.getSSID()
			  		if self.wifiKey in self.ssid:
			  			self.connected = 0
			  			s.detach()
			  			self.connect()
		  			
		  		
		  	except ConnectionAbortedError as e:
		  		while True:
			  		time.sleep(3)
			  		print('connection aborted')
			  		self.wifiCurrent = self.wifiMain.getConnectionInfo()
			  		self.ssid = self.wifiCurrent.getSSID()
			  		if self.wifiKey in self.ssid:
			  			print('connection secured')
			  			self.connected = 0
			  			s.detach()
			  			self.connect()
		  			
		  	except TimeoutError as e:
		  		print('Time Out Error')
		  		time.sleep(3)
		  		self.wifiCurrent = self.wifiMain.getConnectionInfo()
		  		self.ssid = self.wifiCurrent.getSSID()
		  		print(self.ssid)
		  		if self.wifiKey in self.ssid:
		  			self.connected = 0
		  			s.detach()
		  			self.connect()
		  		
		  		
		  	except OSError as e:
		  		while True:
			  		print('os error')
			  		time.sleep(2)
			  		self.wifiCurrent = self.wifiMain.getConnectionInfo()
			  		self.ssid = self.wifiCurrent.getSSID()
			  		print(self.ssid)
			  		if self.wifiKey in self.ssid:
			  			self.connected = 0
			  			s.detach()
			  			self.connect()
		  			
		  			
		  		
	def toggle_state(self,a):
		
		self.buttonState = a
		#self.dataString = '{},{},{},{}\r\n\n'.format(self.port,self.stbd,self.stern, self.buttonState)
		
	def button_state(self,btn,val):
		if btn == 'startBtn':
			self.startBtn_state = val
			self.cntrlBtn_state = 0
			self.dataString = '{},{},{},{},{}\r\n\n'.format(self.port,self.stbd,self.stern, self.startBtn_state,self.cntrlBtn_state)
			
		if btn == 'cntrlBtn':
			self.cntrlBtn_state = val
			self.startBtn_state = 0
			self.dataString = '{},{},{},{},{}\r\n\n'.format(self.port,self.stbd,self.stern, self.startBtn_state,self.cntrlBtn_state)
		
	def key_handler(self):
		
		pass
	
		
	def update_coordinates(self, joystick, pad, a,b,c):		
		
		if pad[0] == 0:
			x = '0.000'
		if pad[0] != 0:
			x = str(pad[0])[0:5] 
		if pad[1] == 0:
			y= '0.000'
		if pad[1] != 0:
			y = str(pad[1])[0:5] 
		
		radians = str(joystick.radians)[0:5]
		magnitude = str(joystick.magnitude)[0:5]
		angle = str(joystick.angle)[0:5]
		text = "x: {}\ny: {}\nradians: {}\nmagnitude: {}\nangle: {}"
		
		if a == 1:
			self.portJoyString = text.format(x, y, radians, magnitude, angle)
			self.port = y			
			
		elif b == 1:
			self.stbdJoyString = text.format(x, y, radians, magnitude, angle) 
			self.stbd = y
		elif c ==1:
			self.sternJoyString = text.format(x, y, radians, magnitude, angle) 
			self.stern = y
		if self.buttonState == '0':
			self.dataString = '{},{},{},{},{}\r\n\n'.format(self.port,self.stbd,self.stern, self.startBtn_state, self.cntrlBtn_state)
		
		if self.buttonState == '1':
			self.dataString = '{},{},{},{},{}\r\n\n'.format(y,y,y, self.startBtn_state,self.cntrlBtn_state)
		
		
	def build(self):
	        	  self.runServer = threading.Thread(target= self.connect)
	        	  self.runServer.start()
	        	  
	        	  
	        	  return Builder.load_string(kv)
	
if __name__ == '__main__':
	pyatt_controlsApp = spudControlsApp()
	pyatt_controlsApp.run()
	
