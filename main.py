import os, sys, atexit, time
from function import Function
from world import main_world

def exit_handler():
	main_world.save_world()

if __name__ == "__main__":
	args = sys.argv[1:]
	if len(args) > 0:
		if os.path.isfile(args[0]):
			## Load world file
			if "-l" in args:
				main_world.load_world(os.path.dirname(args[0]),True)
			else:
				main_world.load_world(os.path.dirname(args[0]),False)

			# Save world file
			if "-s" in args:
				atexit.register(exit_handler)

			executed_by = False
			if "-e" in args:
				main_world.place_entity((0,0,0),"player",False,"primary")
				executed_by = "primary"

			if "-t" in args:
				while True:
					main_world.functions[os.path.relpath(args[0][:-11],main_world.directory)].execute(executed_by)
					time.sleep(0.05)
			else:
				main_world.functions[os.path.relpath(args[0][:-11],main_world.directory)].execute(executed_by)
		else:
			raise Exception("Unknown File: {}".format(args[0]))

