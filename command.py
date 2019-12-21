import json, sys
from world import main_world
import re, random
import os

class Command:
	def __init__(self,line):
		self.line = line
		self.is_valid = False

		if line == "" or line[0] == "#":
			return None

		self.command_type = self.get_command_type()
		self.raw_arguments = self.get_raw_arguments()
		self.parsed_arguments = False

		if self.command_type in command_schema:
			for variant in command_schema[self.command_type]:
				## Loops through and see if any of the different variants of the commands apply for the arguments
				if type(variant) != int:
					var_args = variant[1:] 
					parsed_arguments = self.get_parsed_arguments(variant[0],var_args)
				else:
					parsed_arguments = {}
				if parsed_arguments != False:
					self.parsed_arguments = parsed_arguments
					self.is_valid = True

		if not self.is_valid:
			raise Exception("Invalid command: {}".format(self.line))

	def get_parsed_arguments(self,min_len,variant):
		command_arguments = {}
		for a in variant:
			command_arguments[a[0]] = False
		i = 0
		j = 0
		## i is variant arg and j is raw arg 
		while j < len(variant) and i < len(self.raw_arguments):
			arg_name = variant[j][0]
			arg_type = variant[j][1]

			if type(arg_type) == list:
				if self.raw_arguments[i] in arg_type or len(arg_type) == 0:
					command_arguments[arg_name] = self.raw_arguments[i]
				else:
					return False
			elif arg_type in argument_types:
				if arg_type == "string":
					command_arguments[arg_name] = " ".join(self.raw_arguments[i:])
					i = len(self.raw_arguments)
				elif arg_type == "block":
					command_arguments[arg_name] = self.raw_arguments[i]
				elif arg_type == "entity":
					command_arguments[arg_name] = self.raw_arguments[i]
				elif arg_type == "coordinates":
					if i + 2 < len(self.raw_arguments):
						x = self.raw_arguments[i]
						y = self.raw_arguments[i + 1]
						z = self.raw_arguments[i + 2]
						if self.are_valid_coordinates((x,y,z)):
							command_arguments[arg_name] = (x,y,z)
							i += 2
						else:
							return False
					else:
						return False
				elif arg_type == "command":
					command_arguments[arg_name] = Command(" ".join(self.raw_arguments[i:]))
					i = len(self.raw_arguments)
				elif arg_type == "data" or arg_type == "int":
					if self.is_int(self.raw_arguments[i]):
						command_arguments[arg_name] = int(self.raw_arguments[i])
					else:
						return False
				elif arg_type == "boolean":
					if self.raw_arguments[i] == "true":
						command_arguments[arg_name] = True
					elif self.raw_arguments[i] == "false":
						command_arguments[arg_name] = False
					else:
						return False
				elif arg_type == "target":
					command_arguments[arg_name] = self.parse_target(self.raw_arguments[i])
			else:
				raise Exception("Unknown arg_type {}".format(arg_type))

			i += 1
			j += 1

		## If the command didn't form a command of the minimum length
		if i < min_len or i < len(self.raw_arguments):
			return False
		return command_arguments

	def is_int(self,c):
		try:
			int(c)
			return True
		except:
			return False

	def are_valid_coordinates(self,coordinates):
		def is_valid(c):
			## If ((~ or ^) and (is int or is only that symbol)) or is int
			return ((c[0] == "~" or c[0] == "^") and (self.is_int(c[1:]) or len(c) == 1)) or self.is_int(c)
		return is_valid(coordinates[0]) and is_valid(coordinates[1]) and is_valid(coordinates[2])

	def get_command_type(self):
		return self.line.split()[0]

	def get_raw_arguments(self):
		return self.line.split()[1:]

	def parse_target(self,target):
		if target[0] == "@":
			target_parsed = {"tags":[],"scores":[]}

			selector = target[:2]
			args = target[3:-1]

			scores = re.findall("scores={.*}",args)
			args = re.sub("scores={.*}","",args).split(",")

			x = "~"
			y = "~"
			z = "~"

			for a in args:
				if not a:
					continue
				k, v = a.split("=")
				if k in ["r","rm","dx","dy","dz","name","type","c"]:
					target_parsed[k] = v
				if k == "x":
					x = v
				elif k == "y":
					y = v
				elif k == "z":
					z = v
				if k == "tag":
					target_parsed["tags"].append(v)

			if scores:

				scores = scores[0][8:-1].split(",")
				for s in scores:
					o, v = s.split("=")
					v_split = v.split("..")
					if len(v_split) == 1:
						if v[0] == "!":
							target_parsed["scores"].append({"objective":o,"not":int(v[1:])})
						else:
							target_parsed["scores"].append({"objective":o,"min":int(v),"max":int(v)})
					else:
						if v_split[0]:
							v_min = int(v_split[0])
						else:
							v_min = None

						if v_split[1]:
							v_max = int(v_split[1])
						else:
							v_max = None
						target_parsed["scores"].append({"objective":o,"min":v_min,"max":v_max})

			if selector == "@a":
				target_parsed["type"] = "player"
			elif selector == "@p":
				target_parsed["type"] = "player"
				target_parsed["c"] = "1"
			elif selector == "@r":
				target_parsed["random"] = True
				if "c" not in target_parsed:
					target_parsed["c"] = 1
			elif selector == "@s":
				target_parsed["u"] = True

			target_parsed["coordinates"] = (x,y,z)
			return target_parsed
		else:
			return target

	def get_entities(self,executed_by,executed_at,target):
		if "u" in target:
			if not executed_by:
				return []
			target["u"] = executed_by
		target["coordinates"] = self.calculate_coordinates(executed_at,target["coordinates"])
		return main_world.get_entities(target)

	def calculate_coordinates(self,executed_at,coordinates):
		def calc(c1,c2):
			if c2[0] == "~":
				if len(c2) > 1:
					return c1 + int(c2[1:])
				else:
					return c1
			elif c2[0] == "^":
				if len(c2) > 1:
					return c1 + int(c2[1:])
				else:
					return c1
			else:
				return int(c2)
		if coordinates:
			x = calc(executed_at[0],str(coordinates[0]))
			y = calc(executed_at[1],str(coordinates[1]))
			z = calc(executed_at[2],str(coordinates[2]))
		else:
			x = executed_at[0]
			y = executed_at[1]
			z = executed_at[2]
		return (x,y,z)

	def execute(self,executed_by=False,executed_at=False,depth=0):
		if not executed_at:
			if executed_by:
				try:
					executed_at = main_world.entities[executed_by]["coordinates"]
				except:
					executed_at = (0,0,0)
			else:
				executed_at = (0,0,0)

		if self.is_valid:
			if self.command_type == "execute":
				self.execute_execute(executed_by,executed_at,depth)
			elif self.command_type == "detect":
				self.execute_detect(executed_by,executed_at)
			elif self.command_type == "fill":
				self.execute_fill(executed_by,executed_at)
			elif self.command_type == "function":
				self.execute_function(executed_by,executed_at,depth)
			elif self.command_type == "kill":
				self.execute_kill(executed_by,executed_at)
			elif self.command_type == "say":
				self.execute_say(executed_by,executed_at)
			elif self.command_type == "setblock":
				self.execute_setblock(executed_by,executed_at)
			elif self.command_type == "summon":
				self.execute_summon(executed_by,executed_at)
			elif self.command_type == "tag":
				self.execute_tag(executed_by,executed_at)
			elif self.command_type == "tp":
				self.execute_tp(executed_by,executed_at)
			elif self.command_type == "scoreboard":
				self.execute_scoreboard(executed_by,executed_at)
			elif self.command_type == "exit":
				self.execute_exit()
		else:
			raise Exception("Invalid command: {}".format(self.line))

	def execute_exit(self):
		sys.exit(0)

	def execute_execute(self,executed_by,executed_at,depth):
		command = self.parsed_arguments["command"]
		for u in self.get_entities(executed_by,executed_at,self.parsed_arguments["target"]):
			coordinates = self.calculate_coordinates(main_world.entities[u]["coordinates"],self.parsed_arguments["coordinates"])
			command.execute(u,coordinates,depth + 1)

	def execute_detect(self,executed_by,executed_at):
		current_block = main_world.get_block(self.calculate_coordinates(executed_at,self.parsed_arguments["coordinates"]))
		if self.parsed_arguments["block"] == current_block["block"] and (self.parsed_arguments["data"] == current_block["data"] or self.parsed_arguments["data"] == -1):
			command = self.parsed_arguments["command"]
			command.execute(executed_by,executed_at)

	def execute_fill(self,executed_by,executed_at):
		to_coordinates = self.calculate_coordinates(executed_at,self.parsed_arguments["to_coordinates"])
		from_coordinates = self.calculate_coordinates(executed_at,self.parsed_arguments["from_coordinates"])

		x = min(to_coordinates[0],from_coordinates[0])
		while x <= max(to_coordinates[0],from_coordinates[0]):
			y = min(to_coordinates[1],from_coordinates[1])
			while y <= max(to_coordinates[1],from_coordinates[1]):
				z = min(to_coordinates[2],from_coordinates[2])
				while z <= max(to_coordinates[2],from_coordinates[2]):
					if self.parsed_arguments["place_type"] == "replace":
						current_block = main_world.get_block((x,y,z))
						if self.parsed_arguments["r_block"] == current_block["block"]:
							if not self.parsed_arguments["r_data"] or self.parsed_arguments["r_data"] == current_block["data"]:
								main_world.place_block((x,y,z),self.parsed_arguments["block"],self.parsed_arguments["data"])
					else:
						main_world.place_block((x,y,z),self.parsed_arguments["block"],self.parsed_arguments["data"])
					z += 1
				y += 1
			x += 1

	def execute_function(self,executed_by,executed_at,depth):
		if self.parsed_arguments["path"] in main_world.functions or main_world.load_function(self.parsed_arguments["path"]):
			main_world.functions[self.parsed_arguments["path"]].execute(executed_by,executed_at,depth + 1)
		else:
			raise Exception("Unknown Function: {}".format(self.parsed_arguments["path"]))

	def execute_kill(self,executed_by,executed_at):
		for u in self.get_entities(executed_by,executed_at,self.parsed_arguments["target"]):
			main_world.remove_entity(u)

	def execute_setblock(self,executed_by,executed_at):
			coordinates = self.calculate_coordinates(executed_at,self.parsed_arguments["coordinates"])
			main_world.place_block(coordinates,self.parsed_arguments["block"],self.parsed_arguments["data"])

	def execute_say(self,executed_by,executed_at):
		def evaluate_text(text):
			t = text.split(" ")
			i = 0
			while i < len(t):
				if len(t[i]) > 1 and t[i][:2] in ["@s","@p","@r","@a","@e"]:
					is_character = False
					objective = False
					if "*" in t[i]:
					 	target, objective = t[i].split("*")
					elif "#" in t[i]:
						target, objective = t[i].split("#")
						is_character = True
					else:
					 	target = t[i]

					entities = self.get_entities(executed_by,executed_at,self.parse_target(target))
					if entities:
						if objective:
							if is_character:
								t[i] = ", ".join([chr(main_world.get_entity_score(u,objective)) for u in entities])
							else:
								t[i] = ", ".join([str(main_world.get_entity_score(u,objective)) for u in entities])
						else:
							t[i] = ", ".join([main_world.entities[u]["name"] for u in entities])
					else:
						t[i] = ""

				if len(t[i]) > 2 and t[i][0] == "$":
					coordinates = t[i][2:-1].split(",")
					coordinates = self.calculate_coordinates(executed_at,coordinates)
					block = main_world.get_block(coordinates)
					t[i] = "{}:{}".format(block["block"],block["data"])
				i += 1

			return " ".join(t)

		executer = "@"
		if executed_by:
			executer = main_world.entities[executed_by]["name"]
		evaluated_text = evaluate_text(self.parsed_arguments["text"])

		say_text = "[{}] {}\n".format(executer,evaluated_text)
		sys.stdout.write(say_text)	

	def execute_summon(self,executed_by,executed_at):
		coordinates = self.calculate_coordinates(executed_at,self.parsed_arguments["coordinates"])
		main_world.place_entity(coordinates,self.parsed_arguments["entity"],self.parsed_arguments["name"])	

	def execute_tag(self,executed_by,executed_at):
		target = self.parsed_arguments["target"]
		if self.parsed_arguments["option"] == "add":
			for u in self.get_entities(executed_by,executed_at,target):
				main_world.add_tag(u,self.parsed_arguments["name"])
		elif self.parsed_arguments["option"] == "remove":
			for u in self.get_entities(executed_by,executed_at,target):
				main_world.remove_tag(u,self.parsed_arguments["name"])

	def execute_tp(self,executed_by,executed_at):
		if "victim" in self.parsed_arguments:
			victim = self.parsed_arguments["victim"]
		else:
			victim = self.parse_target("@s")

		for u in self.get_entities(executed_by,executed_at,victim):
			if "coordinates" in self.parsed_arguments:
				coordinates = self.calculate_coordinates(executed_at,self.parsed_arguments["coordinates"])
			else:
				destination_u = self.get_entities(executed_by,executed_at,self.parsed_arguments["destination"])
				if len(destination_u) > 1:
					return False
				else:
					coordinates = main_world.entities[destination_u[0]]["coordinates"]

			if self.parsed_arguments["check_block"] and main_world.get_block(coordinates)["block"] != "air":
				return False
			main_world.move_entity(u,coordinates)

	def execute_scoreboard(self,executed_by,executed_at):
		if self.parsed_arguments["type"] == "objectives":
			if self.parsed_arguments["method"] == "add":
				main_world.add_objective(self.parsed_arguments["objective"])
			elif self.parsed_arguments["method"] == "remove":
				main_world.add_objective(self.parsed_arguments["objective"])
		else:
			if self.parsed_arguments["method"] == "reset":
				for u in self.get_entities(executed_by,executed_at,self.parsed_arguments["target"]):
					main_world.reset_entity_scores(u,self.parsed_arguments["objective"])
			elif self.parsed_arguments["method"] in ["set","add","remove"]:
				for u in self.get_entities(executed_by,executed_at,self.parsed_arguments["target"]):
					main_world.set_entity_score(u,self.parsed_arguments["method"],self.parsed_arguments["objective"],self.parsed_arguments["count"])
			elif self.parsed_arguments["method"] == "random":
				for u in self.get_entities(executed_by,executed_at,self.parsed_arguments["target"]):
					main_world.set_entity_score(u,"set",self.parsed_arguments["objective"],random.randint(int(self.parsed_arguments["max"]),int(self.parsed_arguments["min"])))
			elif self.parsed_arguments["method"] == "operation":
				for u_a in self.get_entities(executed_by,executed_at,self.parsed_arguments["target_a"]):
					for u_b in self.get_entities(executed_by,executed_at,self.parsed_arguments["target_b"]):
						score_a = main_world.get_entity_score(u_a,self.parsed_arguments["objective_a"])
						score_b = main_world.get_entity_score(u_b,self.parsed_arguments["objective_b"])
						if not score_a:
							score_a = 0
						if not score_b:
							score_b = 0
						op = self.parsed_arguments["operator"]
						if op == "%=":
							score_a %= score_b
						elif op == "*=":
							score_a *= score_b
						elif op == "+=":
							score_a += score_b
						elif op == "-=":
							score_a -= score_b
						elif op == "/=":
							score_a /= score_b
						elif op == "<":
							score_a = min(score_a,score_b)
						elif op == "=":
							score_a = score_b
						elif op == ">":
							score_a = max(score_a,score_b)
						elif op == "><":
							tmp = score_a
							score_a = score_b
							main_world.set_entity_score(u_b,"set",self.parsed_arguments["objective_b"],tmp)
						main_world.set_entity_score(u_a,"set",self.parsed_arguments["objective_a"],score_a)
			elif self.parsed_arguments["method"] == "input":
				inp = sys.stdin.readline()[:-1]
				if self.is_int(inp):
					count = int(inp)
				elif len(inp) == 1:
					count = ord(inp)
				elif not inp:
					count = 0
				else:
					raise Exception("Invalid Input: {}".format(inp))

				for u in self.get_entities(executed_by,executed_at,self.parsed_arguments["target"]):
					main_world.set_entity_score(u,"set",self.parsed_arguments["objective"],count)


argument_types = ["target","command","coordinates","block","data","string","int","boolean","entity"]

if hasattr(sys, "frozen"):
    p = os.path.dirname(sys.executable)
else:
	p = os.path.dirname(__file__)

with open("{}/schemas/command.json".format(p)) as f:
	command_schema = json.load(f)
