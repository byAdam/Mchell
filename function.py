class Function():
	def __init__(self,relpath,lines):
		self.relpath = relpath

		self.commands = []
		for line in lines:
			self.commands.append(self.create_command_object(line))

	def create_command_object(self,line):
		from command import Command
		return Command(line.strip())

	def add_to_command_stack(self,executed_by=False,executed_at=False):
		from world import main_world
		command_stack = []
		for command in self.commands:
			if command.is_valid:
				command_stack.append({"command":command,"executed_by":executed_by,"executed_at":executed_at})

		main_world.command_stack = command_stack + main_world.command_stack
