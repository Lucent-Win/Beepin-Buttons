import random
import os
from os import scandir
import json_handler as json_io





class keyperhive:
	'''
	Counts keystrokes across the system. 

	On start this will create a 'keypers' folder and a total.json.
	Total counts all the key presses your computer recieves.
	You can also make your own keypers for tracking keystrokes
	across many keyboards, stored in the same folder.
		
	'''



	save_folder = "./keypers/"
	total_keyper = "./keypers/total.json"
	
	# chars not allowed in filenames.
	# Renamed (as far as program knows) so custom sounds can be assigned to them anyway. 
	illegal_chars = {
	"/":"forward_slash" ,
	"\\": "backslash" ,
	"*" : "asterisk" ,
	"?":"question_mark" , 
	":" : "colon",
	'"':"double_quote" , 
	"|":"pipe" ,
	"<":"less_than", 
	">" : "greater_than" }
	def __init__(self):
		
		# the total.json logs data across all keypers, so its data is seperate.
		self.summary = {"total":0,"least":"","most":""}
		self.key_data = {} # key: count
		self.total_summary = {"total":0,"least":"","most":""}
		self.total_key_data = {}
		
		self.keypers = {} # name : path
		self.current_keyper = ""

		if not os.path.exists(self.save_folder):
			os.makedirs(self.save_folder)
			
		if not os.path.exists(self.total_keyper):
			self.add("total")
			
		self.scan()
		self.key_data.clear() # started full of garbage characters in testing. 
		self.init_total()



# General note, while lines can be broken up for readability
# this has a tendancy of breaking the script
	def scan(self):
		'''
		Search for all keyper files in save folder and load them to list. 
		Does not scan subdirectories.     
		
		'''
		
		self.keypers.clear()        
		save_folder = scandir(self.save_folder)            
		
		for file in save_folder:
			if file.is_file():         
				file_name = file.name.rsplit('.')[0]
				file_extension = os.path.splitext(file.name)[1][1:].strip().lower()
				
				if file_extension == "json":
					try:
						self.load(file_name) 
						self.keypers[file_name] = file
					except:
						continue   # not a valid json file. 
				else:
					pass       



	def add(self,name):
		'''
		Creates a new keyper
		'''
		if name == "":
			return
		
		keyper = self.get_keyper(name)
		if keyper != None:
			print("Keyper already exists")
			return


		self.save()
		self.key_data.clear()                  

		path = self.save_folder + name + ".json"
		open(path, "w")

		data_array = [self.summary,self.key_data]
		json_io.save_json(path,data_array)

		self.keypers.update({name:path})
		self.current_keyper = name
		self.save()


	def delete(self, keyper = ""):
		'''
		Deletes a specified keyper.
		'''

		if keyper == "total":
			print("Total cannot be removed.")
			return

		keyper = self.get_keyper(keyper)

		if keyper != None:
			self.keypers.pop(keyper)
			os.remove(self.save_folder + keyper + ".json")
			print("Deleted keyper " + keyper)
		else:
			print("Could not delete keyper")
			return


	def get_keyper(self, name):
		'''
		Returns the str(name) of a keyper.
		'''

		if name != "":
			if name in list(self.keypers.keys()):
				return name
		else:
			print("Could not find keyper.")
			return None # force error / error handling
							   

	def rename(self, old_name, new_name):
		'''
		Renames a keyper and it's json.
		'''
		if old_name == new_name:
			print("Names cannot be equal")
			return

		if old_name == "" or new_name == "":
			print("Names can't be empty")
			return  

		if old_name == "total" or new_name == "total":
			print("Cannot rename this file.")
			return

		keyper = self.get_keyper(new_name)
		if keyper != None:
			print("Keyper already exists")
			return


		try:
			os.rename(str(self.save_folder+old_name+".json"), str(self.save_folder+new_name+ ".json"))
			self.keypers.pop(old_name)
			self.keypers[new_name] = str(self.save_folder+new_name+ ".json")
			self.current_keyper = new_name
			if self.verbose:
				print(str("Renamed keyper "+old_name+ " to "+ new_name))
		except  KeyError:
				print("Keyper " + old_name + " doesn't exist.")
		except FileNotFoundError:
				print("Folder " + old_name + " doesn't exist.")
		except:
				print("Could not rename profile.")


	def init_total(self):
		
		# must load these values on start or else total will be wiped
		# since if total.json is not loaded, its variables are left blank
		# and those blank values then save. 
		if not os.path.exists(self.total_keyper):
			self.add("total")

		file_path = self.total_keyper
		data = json_io.open_json(file_path)

		self.total_summary.update(data[0])
		self.total_key_data.update(data[1])
		self.current_keyper = "total"
		self.sort()			

	
	def load(self, name = "", create_new = False):
		'''
		Loads data from a given keyper or makes a new one. 
		'''
  
		keyper = self.get_keyper(name)

		if keyper != None: 
			
			file_path = self.save_folder + name + ".json"
			data = json_io.open_json(file_path)

			self.key_data.clear()

			self.summary.update(data[0])
			self.key_data.update(data[1])

			self.current_keyper = name
			if self.current_keyper == "total":
				self.total_summary.update(data[0])
				self.total_key_data.update(data[1])	

			
			self.sort()			
			

		elif create_new == True: #keyper does not exist, make a new one
			try:
				self.add(name)
				self.load(name)
			except:
				return


	

	def save(self):
		'''
		Saves data for both loaded keyper and for total.json. 
		'''

		data_array = [self.summary, self.key_data]
		total_array = [self.total_summary, self.total_key_data]


		try:
			json_io.save_json(self.save_folder+self.current_keyper+".json",data_array)
			json_io.save_json(self.total_keyper, total_array)
		except:
			return
		
	
	def on_press(self,key):
		'''
		Should be called anytime key is pressed.
		Updates keystroke counter values. 
		'''

		save_key = self.filter_key(key)
		
		if save_key not in self.key_data.keys():
			self.key_data.update({save_key: 1})
		else:
			self.key_data[save_key] += 1
			
			
		if save_key not in self.total_key_data.keys():
			self.total_key_data.update({save_key: 1})
		else:
			self.total_key_data[save_key] += 1
			  
		
	

	def wipe_key_data(self):
		'''
		Clears all data from a keyper except total. 
		'''
		if self.current_keyper == "":
			return
		self.key_data.clear()

		self.sort()


	def sort(self):
		'''
		Updates the summary values for every keyper.
		If many keys tie for least or most pressed, a single of them is given. 
		'''

		if self.current_keyper == "total":
			if len(self.total_key_data) > 0:
				max_key = max(self.total_key_data, key=self.total_key_data.get)
				min_key = min(self.total_key_data, key=self.total_key_data.get)
				total = sum(self.total_key_data.values())
			
		
				self.total_summary["most"] = str(max_key)
				self.total_summary["least"] = str(min_key)
				self.total_summary["total"] = total
			else:
				self.total_summary["most"] = "None"
				self.total_summary["least"] = "None"
				self.total_summary["total"] = 0
		else:
			if len(self.key_data) > 0:
				max_key = max(self.key_data, key=self.key_data.get)
				min_key = min(self.key_data, key=self.key_data.get)
				total = sum(self.key_data.values())
			
				self.summary["most"] = str(max_key)
				self.summary["least"] = str(min_key)
				self.summary["total"] = total	
			else:
				self.summary["most"] = "None"
				self.summary["least"] = "None"
				self.summary["total"] = 0				

			
		self.save()
		


	def get_summary(self, name):
		'''
		Returns summary of most, least, and total pressed keys as a dictonary.
		'''

		dict_stats = {}
		self.sort()

		if name == "total":		
			dict_stats.update({"most" : self.total_summary["most"]})
			dict_stats.update({"least" : self.total_summary["least"]})
			dict_stats.update({"total" : str(self.total_summary["total"])})
		else:
			dict_stats.update({"most" : self.summary["most"]})
			dict_stats.update({"least" : self.summary["least"]})
			dict_stats.update({"total" : str(self.summary["total"])})				
		return dict_stats




	def filter_key(self,key):
		'''
		Strips keyname down.
		Keycodes delivered by pynput are unusable by the script as they are. 
		'''

		key = str(key)
		key = key.replace("Key.","")
		key = key.lower()

		# if its 'j' and not literally a '
		if key.startswith("'") and key != "'": 
			key = key[1:]
		if key.endswith("'")and key != "'":
			key = key[:-1]
			

		# if its "j"  and not literally a "
		if key.startswith('"') and key != '"':
			key = key[1:]
		if key.endswith('"')  and key != '"':
			key = key[:-1]

		if key in self.illegal_chars:
			return self.illegal_chars[key]
		else:
			return key









































############################################### Class seperation























	






class keyboardmixer:
	'''
	Turns music folders into soundbytes for your keyboard.

	Drop a folder(s) with sounds into the same directory as this script.
	Run it; a folder will be created automatically.
	It will contain json files named after your sound folders.
	Each profile will link to sounds in its respective library of sounds. 		
	'''
	
	
	
	supported_audio_formats = ["wav","ogg","mp3"]
	custom_key_prefix = ["cst_"]
	ignored_folders = ["profiles","keyper"]
	save_folder = "./profiles/"
	


	def __init__(self):
		self.generic_beeps = []
		self.custom_beeps = {}

		self.profiles = {} # name: path
		self.current_profile = ""

		if not os.path.exists(self.save_folder):
			os.makedirs(self.save_folder)

		self.scan()



									

	def scan(self):
		'''
		Finds all directories in same folder as this script
		, then sends each folder to be searched.
		'''


		self.generic_beeps.clear()
		self.custom_beeps.clear()

		ls_local_folders = [x[1] for x in os.walk(".")][0] # names of folders
		
		i = 0
		while i <= len(ls_local_folders)-1:
			folder_name = str(ls_local_folders[i])                       
			if folder_name != "" and folder_name != ".":
				path = "./" + ls_local_folders[i]
				self.search_folder(str(path), ls_local_folders[i])
			i +=1
				



# does NOT support random sounds for custom keys as of yet. 
	def search_folder(self,folder_path,folder_name):
		'''
		If there is supported audio, a profile is created with the same name
		as that folder.
		Otherwise the folder is ignored.
		'''                
		self.generic_beeps.clear()
		self.custom_beeps.clear()
		prev_profile = self.current_profile

		#temporary variables for each folders custom keys and custom sound respectively. 
		key_buffer = []
		sound_file_buffer = []

		folder_files = scandir(folder_path)    

		for file in folder_files:
			if file.is_file():
			 
				file_name = file.name.rsplit('.')[0]
				file_extension = os.path.splitext(file.name)[1][1:].strip().lower()
				
							  
				if file_extension in self.supported_audio_formats:
					new_folder_name = folder_name.replace("'","")
					self.profiles[folder_name] = self.save_folder + new_folder_name + ".json"
					sound_file = folder_path + "/" + file.name

					if self.__is_custom_sound(file_name) == True:

						custom_key_name = self.__to_lower_letters(file_name.replace(str(self.custom_key_prefix[0]),""))                        
						custom_sound_file = folder_path + "/" + file.name
						
						key_buffer.append(custom_key_name)
						sound_file_buffer.append(custom_sound_file)
						
						self.custom_beeps[custom_key_name] = []
						self.custom_beeps[custom_key_name].append(custom_sound_file)

						self.save(folder_name)
						
					else:
						self.generic_beeps.append(sound_file)
						self.save(folder_name)

				else: #this is not a valid folder
					pass
				
		#called after folder is read. 
		self.load(prev_profile)


		



	def load(self,name = ""):
		'''
		Loads in requested sound profile. 
		'''

		try:
			profile = str(self.get_profile(name))
			file_path = str(self.profiles[profile])
			data = json_io.open_json(file_path)
			#wipe settings from previous sound profile
			self.generic_beeps.clear()
			self.custom_beeps.clear()
			#update sounds with new profile's
			self.generic_beeps.extend(data[0])
			self.custom_beeps.update(data[1])

			self.current_profile = profile
		except:
			return
			
	
	def random_sound(self, custom_key = ""):
		'''
		Returns a random sound for the presented key. 
		'''
		try:
			if custom_key in list(self.custom_beeps.keys()):
				sound_files = list(self.custom_beeps[custom_key])
				song = random.choice(sound_files)
				return song
			else:
				song = random.choice(self.generic_beeps)
				return song
		except: # no sounds in profile
			return None
			

	def save(self, file_name):
		try:
			file_path = self.save_folder + file_name + ".json"
			data_array = [self.generic_beeps, self.custom_beeps]
			json_io.save_json(file_path,data_array)
		except:
			raise Exception
				


	def get_profile(self, name = ""):
		'''
		Returns the name of a profile.
		'''
		if name != "":
			if name in list(self.profiles.keys()):
				return name
			else:
				return None
		else:
			return None



	def get_current(self):
		'''
		Returns the currently loaded profile as a string. 
		'''
		if self.current_profile != "":
			return self.current_profile
		else:
			return None


			
	def __is_custom_sound(self, file_name):
		if(file_name)[0:len(self.custom_key_prefix[0])] in self.custom_key_prefix:
			return True
		return False

# leftover method from many iterations ago. 
# used by scan once, add lower() before removing. 
	def __to_lower_letters(self,string):
		new_str = string.lower()
		
		return new_str


