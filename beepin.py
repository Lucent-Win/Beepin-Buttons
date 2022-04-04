import math # inside joke
import os.path
import platform
import sys
import tkinter as tk
# custom modules
import json_handler as json_io
import beepInfo
import beepUI
# 3rd party modules
import win32api # none
import win32con # none
import pygame  # GNU Lesser General Public License v3.0
from pynput import keyboard # GNU Lesser General Public License v3.0




#			 UPDATES NOW, NEXT VERSION MUST 
#   Close all threads properly
#   Application Icon when opened. 
# add padding to reset label
# remove border from x button lockbar 


class beepin:
	"""
	Class that makes your buttons beep!
	Your OS might tag a couple scripts as keyloggers. 
	To be clear, this application is a keylogger but is not malicious.

	https://usa.kaspersky.com/resource-center/definitions/keylogger
	"""


	#determined by pygame audio
	max_vol = 1
	min_vol = 0
	
	fg_color = "#586087"
	bg_color = "#4d5877" 
	dk_color = "#242938"

	high_text_color = "#fbff00"
	reg_text_color = "#ffffff"

	title_size = 12
	reg_text_size = 12

	title_font = "consolas"
	reg_font = "arial"


	root = tk.Tk() 
	root.title("beepin' buttons' Ver 2.48 -- by Lucent Win")

	icon = tk.PhotoImage(master=root, data='iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAABb2lDQ1BpY2MAACiRdZE7SwNBFIU/Y0TRSARTiFhsEcXCgCiIpUTQRi1iBF/N7maTCLtx2U0QsRVsLAQL0cZX4T/QVrBVEARFELHyB/hqRNY7JpAgOsvs/Tgz5zJzBkITtun44X5wCkUvNZ7UZufmtcZnwoSIMUSbbvru5PRYmn/Hxy11qt4kVK//9/05WjKWb0Jdk/CQ6XpF4RHhiZWiq3hTOGbm9YzwgXCfJwcUvlS6UeYnxbkyvyn20qlRCKmeWq6GjRo2854j3Cscd+ySWTmPuknEKsxMS+2U2YVPinGSaBiUWMKmSEJqQTL729f/45tiWTym/F1W8cSRIy/ePlFL0tWSmhXdks9mVeX+O08/OzhQ7h5JQsNjELx2Q+M2fG0FwedhEHwdQf0DnBeq/mXJafhd9K2qFt+H6DqcXlQ1YwfONqDj3tU9/UeqlxnKZuHlBFrnoP0amhfKWVXWOb6D9Jo80RXs7kGP7I8ufgP45GgH0CvLIQAAAAlwSFlzAAALEgAACxIB0t1+/AAAAsdJREFUeAHtm+FuwyAMhNdpz9WH74t18qSLjGMTEs4pYdkfCMH23YfLpkl9fNV/3vXXl3n7iJRGL2Yxbn2v/NqFWY2HIDQA1/zr9bLBl3p+Pp+R3j/vIYCrG7euHRAFgOL0ZzMPGB6Eb7zEOKt58ed5EwDF6QPEPxnfRQd4hGYDYT0WAGYz2+Lnp2UTe49zGS0l7AktL5ImpwGomdbe7L5sIOkArCFttmWO+CwQaXeACIf4FqNbe5i5dK2UDtgSWzvNWqy8q8VqY63zFABR8Rbx2FMDEeU/sk7/CETCYaxVZLQ/yt+a1+6jAojERWasGPscxUV1bHzLMxWAVzAy4e311nrjvZx6jQbAOxWWeFYebRxzGgAkxMgWbfN5wFF7z5gGYI+IT+69AXyS/gi17w7IOgXWJQV97HzIS+sAe0ujwOgjDYBnlHVqrDyeRioArwt6xffGe6b1GhWAJGZBEOPZ5kUvHYAk9X72GDrDODSmAPC6AAVr5vZAQr7eMe0fIgIhMhut95o5Ep/SARBS6wTs2RolByNPVCetA1AQ4veeOuKQJ2tMBwDh2lAEQ+9BXPZ4GgBt5BNGdX09T70DdKFR5zeAUU/mLF13B7BIy80e3e69NbLyii56B2SC0CBZv0noACCSdWqsPNBlxzQAUqhXfG+8Nes90/4Qkpb0BHtrtfb19nvCWWs0ACIogmDF9pqsAbS1tp7pHwGmOE88Oz+1AyAYIntPGvlkRE69xpjTO0CLYolm5dHaME/pACSXEeKPdANidT72PB0ABGszNRh6H2Izx9MAaBNnm9S17Tz1DrDFRny+AYx4KmdqKjqgdjmdKSqzlvUoAPQXpzJrj5j7UXSAKLSERlR9VJPnTZ9+8d2hkX5VHTWs4xzzxdfmZG8BAMFXB+EYh7UVgBACIiYal85fJsac2w1mzxUfV35XC8bVLCBCn7+2I7hkoheA/QAAAABJRU5ErkJggg==PS')
	root.wm_iconphoto(True, icon)	
	root.configure(background= bg_color) 


	def __init__(self):
		self.mod_keys = False # can keys sounds be added/removed by user each keypress?
		self.key_down = False
		self.pnl_adv_settings = None
		self.lockbar = None
		self.key_silencing = False

		self.ind_settings = {
		"caps" : True ,
		"num": True , 
		"scroll": True , 
		"start_x": 0 , 
		"start_y" : 0}
		# Repeat protection plays a sound only once even if you hold a key down. 
		self.vol_settings = {
		"curr_vol": 2 , 
		"muted": False, 
		"rpt_protection": True}

		self.muted_keys = { } 	 

		self.defaults = {"profile":"" , "keyper":""} 

		# initialize
		pygame.mixer.init()
		self.kbmixer = beepInfo.keyboardmixer()
		self.kyhive = beepInfo.keyperhive()
		self.save_path = os.getcwd() + "/settings.json"
		self.save_path = json_io.fix_dir(self.save_path)
		self.load_settings(self.save_path)
		

		self.frame_stg = beepUI.settingsFrame(self.root, self)
		self.frame_pf = beepUI.profilesFrame(self.root, self)
		self.frame_pf.update(list(self.kbmixer.profiles.keys())) 
		self.frame_ky = beepUI.keypersFrame(self.root, self)
		self.frame_ky.update(list(self.kyhive.keypers.keys())) 
		self.frame_dt_ky = beepUI.kydetailsFrame(self.root, self)

		# load directly from scripts @ start. Using load_pf/ky() will
		# make the default value blank on start
		self.kbmixer.load(self.defaults["profile"])
		self.defaults["profile"] = self.kbmixer.current_profile
		self.frame_pf.set_label(self.defaults["profile"])

		self.kyhive.load(self.defaults["keyper"])
		self.defaults["keyper"] = self.kyhive.current_keyper
		self.frame_ky.sel_in_list(self.defaults["keyper"])
		self.frame_ky.set_current(self.defaults["keyper"])
		
		self.mk_lockbar()
		self.save()


	

	def mk_lockbar(self):
		'''
		Brings up digital lock light indicators. 
		'''
		self.lockbar = beepUI.lockbar(self.root)
		self.lockbar.update()
		window_geometry = str(self.lockbar.winfo_width()) + 'x' + str(self.lockbar.winfo_height() ) + '+' + str(self.ind_settings["start_x"]) + '+' + str(self.ind_settings["start_y"]) #Creates a geometric string argument
		self.lockbar.geometry(window_geometry)
		self.show_lock_light("caps", self.ind_settings["caps"])
		self.show_lock_light("num", self.ind_settings["num"])
		self.show_lock_light("scroll", self.ind_settings["scroll"])
		self.chk_locks()



# SETTINGS FRAME FUNCTIONS
#
# 
# 
# 
# 
# 
# 	

	def mk_advanced_settings(self):
		'''
		Brings up advanced settings window. 
		'''
		self.pnl_adv_settings = beepUI.adv_settings(self.root, self)
		self.send_muted_keys()
		self.mod_keys = True
		window_geometry = str(self.root.winfo_width()) + 'x' + str(self.root.winfo_height() ) + '+' + str(self.root.winfo_x()) + '+' + str(self.root.winfo_y()) #Creates a geometric string argument
		self.pnl_adv_settings.geometry(window_geometry)

	def toggle_rpt_prot(self):
		'''
		If you hear precisely one sound, then silence, enable. 
		'''

		# Turn off for keyboards without keyup events. 
		# Otherwise you hear precisely one thing and never again. 
		self.vol_settings["rpt_protection"] = not self.vol_settings["rpt_protection"]


	def show_lock_light(self, name, show):
		'''
		Enable a specific lock light.
		'''
		if self.lockbar == None:
			self.mk_lockbar()

		if show == True:
			self.lockbar.show_light(name)
		else:
			self.lockbar.hide_light(name)
		self.ind_settings[name] = show
		self.save()
			


					
	def reset_lockbar(self):
		'''
		Moves lockbar to top left corner of application. 
		'''
		if self.lockbar == None:
			return
		self.lockbar.update()
		window_geometry = str(self.lockbar.winfo_width()) + 'x' + str(self.lockbar.winfo_height() ) + '+' + str(self.root.winfo_x()) + '+' + str(self.root.winfo_y()) #Creates a geometric string argument
		self.lockbar.geometry(window_geometry)
		self.chk_locks()
		
			

	def toggle_debeep(self, value):
		'''
		Toggles if keys should be silenced on press. 
		'''
		self.key_silencing = value 
			

	def send_muted_keys(self):
		'''
		Updates UI with list of keys without sound. 
		'''
		if self.pnl_adv_settings != None:
			self.pnl_adv_settings.update_muted_keys(self.muted_keys)

	def add_silent_key(self,key):
		'''
		Removes sound from specified key. 
		'''
		if key not in self.muted_keys.keys() and self.key_silencing == True and self.mod_keys == True:
			self.muted_keys[key] = True
			self.save()
			self.send_muted_keys()
			print("Silenced " + str(key))
		else:
			return

	def remove_silent_key(self,key):
		'''
		Re-enables sound for specified key. 
		'''
		if key in self.muted_keys.keys()  and self.key_silencing == False and self.mod_keys == True:
			del self.muted_keys[key]
			self.send_muted_keys()
			self.save()
		else:
			return


	def clear_muted_keys(self):
		'''
		Re-enables sound for all keys. 
		'''
		self.muted_keys.clear()
		self.send_muted_keys()
		self.save()
		

	def set_vol(self, new_vol):
		'''
		Controls how loud sounds are. 
		'''		
		new_vol = int(new_vol) / int(100)
		curr_vol = round(self.clamp(new_vol,self.min_vol, self.max_vol),2)

		self.vol_settings["curr_vol"] = curr_vol
		self.save()


	def toggle_mute(self):
		'''
		Enables/Disables sound. 
		'''
		self.vol_settings["muted"] = not self.vol_settings["muted"]
		self.save()


# PROFILE METHODS
#
#
#
#
#
#
#

	def load_pf(self, ignore_this_var):
		'''
		Loads profile and updates UI. 
		'''
		profile = self.frame_pf.get_selected()
		self.kbmixer.load(profile)
		self.defaults["profile"] = profile
		self.frame_pf.set_label(self.kbmixer.current_profile)
		self.save()

				
# KEYPER METHODS 
#
#
#
#
#

	def add_ky(self, name):
		'''
		Adds keyper and updates UI. 
		'''
		self.kyhive.add(name)
		self.frame_ky.update(list(self.kyhive.keypers.keys())) 
		self.frame_ky.set_current(self.kyhive.current_keyper)

	
	def del_ky(self):
		'''
		Deletes keyper and updates UI. 
		'''
		self.kyhive.delete(self.kyhive.current_keyper)
		self.frame_ky.update(list(self.kyhive.keypers.keys())) 
		self.frame_ky.set_current("TERMINATED!")
	
	def rnm_ky(self,new_name):
		'''
		Renames keyper and update UI. 
		'''
		self.kyhive.rename(self.kyhive.current_keyper,new_name)
		self.frame_ky.update(list(self.kyhive.keypers.keys())) 
		self.frame_ky.set_current(self.kyhive.current_keyper)


	
	def load_ky(self, ignore_this_var):
		'''
		Loads keyper and updates UI.
		'''
		keyper = self.frame_ky.get_selected()
		self.kyhive.load(keyper)
		self.defaults["keyper"] = keyper
		self.frame_ky.set_current(str(self.kyhive.current_keyper))
		self.update_ky_dt_frame()
		

		self.save()
		
		
	def wipe_key_data(self):
		'''
		Clears data from current keyper and updates UI.
		'''
		self.kyhive.wipe_key_data()
		ls = ["(None)"]
		self.frame_dt_ky.update(ls)

		stat_dict = self.kyhive.get_summary(self.kyhive.current_keyper)
		self.frame_dt_ky.set_stats(stat_dict["least"], stat_dict["most"], stat_dict["total"])
		self.save()

	def update_ky_dt_frame(self):
		list_keys = list(self.kyhive.key_data.keys())
		list_key_count = list(self.kyhive.key_data.values())
		ls = []
		i = 0
		for element in list_keys:
			ls.append(str(element) + " : " + str(list_key_count[i]))
			i += 1

		self.frame_dt_ky.update(ls)		
		stat_dict = self.kyhive.get_summary(self.kyhive.current_keyper)
		self.frame_dt_ky.set_stats(stat_dict["least"], stat_dict["most"], stat_dict["total"])


	
# KEY BASED METHODS
#
#
#
#
#
#
#




	def on_press(self, key):
		'''
		Makes beepin' happin'
		A sound is picked and played or it is not. 
		'''

		key = self.kyhive.filter_key(key)
		self.frame_stg.display_key(key)
		self.chk_locks()
			
		if self.key_silencing == False:
			self.remove_silent_key(key)
			
		if self.key_silencing == True:
			self.add_silent_key(key)
		

		if self.key_down == False:
			self.kyhive.on_press(key)

		self.update_ky_dt_frame()

		
		if self.vol_settings["muted"] == False and key not in self.muted_keys.keys() and self.key_down == False:
			try:
				if self.vol_settings["rpt_protection"] == True:
					self.key_down = True
				song_path = json_io.fix_dir(self.kbmixer.random_sound(key))
				song = pygame.mixer.Sound(song_path)
				song.set_volume(self.vol_settings["curr_vol"])
				song.play()

			except Exception as e:
				pass
		else: # debugging print statements. 
			if self.vol_settings["muted"] == True:
				print("Keys are muted")
			elif self.vol_settings["curr_vol"] == 0:
				print("Volume is zero.")
			elif key in self.muted_keys.keys():
				print("Key is silenced.")
			elif self.key_down == True:
				print("Key is held down")               
			else:
				print("Why?")
				pass
  
        

# OTHER METHODS
# 
# 
# 
# 
# 
# 
#     
            



	# Not always be called since some keyboards dont send key up. (old ones)
	# Hence key up variable 
	def on_release(self,key):
		self.key_down = False

		
	def clamp(self, num, min, max): #thanks internet
		return min if num < min else max if num > max else num







	def chk_locks(self):
		if self.lockbar == None:
			return
	
		if platform.system() == "Windows":
			caps = False
			num = False
			scroll = False
			# -127 means it is pressed down. 1 is returned initially
			if win32api.GetKeyState(win32con.VK_CAPITAL) == -127 or win32api.GetKeyState(win32con.VK_CAPITAL) == 1:
				caps = True
			if win32api.GetKeyState(win32con.VK_NUMLOCK) == -127 or win32api.GetKeyState(win32con.VK_NUMLOCK) == 1:
				num = True
			if win32api.GetKeyState(win32con.VK_SCROLL) == -127 or win32api.GetKeyState(win32con.VK_SCROLL) == 1:
				scroll = True

			
			self.lockbar.set_locks(caps,num,scroll)
		else:
			return



	def load_settings(self, file_path):
		'''
		Loads user settings. Uses defaults on error
		'''
		try:
			data_sent = json_io.open_json(file_path)
			self.ind_settings.update(data_sent[0])
			self.vol_settings.update(data_sent[1]) 
			self.muted_keys.update(data_sent[2]) 
			self.defaults.update(data_sent[3])
		except:
			open(self.save_path, "w")
			self.save()




	def save(self):     
		data_array = [
			self.ind_settings,
			self.vol_settings,
			self.muted_keys,
			self.defaults
			]
		json_io.save_json(self.save_path,data_array)
			
        
	
	def close_window(self):
		'''
		Saves and exits application immediately.
		'''
		coords_ls = self.lockbar.get_coords()
		self.ind_settings["start_x"] = coords_ls[0]
		self.ind_settings["start_y"] = coords_ls[1]

		self.kyhive.save()
		self.save()
		
		pygame.mixer.stop()
		pygame.quit()
		self.lockbar.destroy()
		self.root.destroy()
		self.root.quit() # only here to be thorough
		sys.exit(0)



'''
bpr = beepin()

listener = keyboard.Listener(on_press=bpr.on_press,on_release= bpr.on_release)
listener.start()

bpr.root.protocol("WM_DELETE_WINDOW", bpr.close_window)
bpr.root.mainloop()
'''

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

