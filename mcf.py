import os, sys, atexit, time
from function import Function
from command import Command
from world import main_world

def exit_handler():
	main_world.save_world()

def shell():
	while True:
		inp = input("> ")
		command = Command(inp).execute(executed_by)

if __name__ == "__main__":
	args = sys.argv[1:]
	flags = []
	files = []
	for f in args:
		if f[0] == "-":
			flags.append(f)
		else:
			files.append(f)

	executed_by = False
	## Base Entity
	if "-e" in flags:
		main_world.place_entity((0,0,0),"player","main","primary")
		executed_by = "primary"

	if files:
		fname = files[0]
		if os.path.isfile(fname):
			# Save world file
			if "-s" in flags:
				atexit.register(exit_handler)

			## Load world file
			if "-l" in flags:
				main_world.load_world(os.path.dirname(fname),True)
			else:
				main_world.load_world(os.path.dirname(fname),False)


			main_world.load_function(os.path.basename(fname)[:-11])

			## Loops 20 times a second
			if "-t" in flags:
				while True:
					main_world.functions[os.path.relpath(fname[:-11],main_world.directory)].add_to_command_stack(executed_by)
					if not main_world.is_processing:
						main_world.process_command_stack()
			else:
				main_world.functions[os.path.relpath(fname[:-11],main_world.directory)].add_to_command_stack(executed_by)
				main_world.process_command_stack()
		else:
			raise Exception("Unknown File: {}".format(fname))
	else:
		shell()