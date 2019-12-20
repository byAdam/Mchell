class Function():
	def __init__(self,relpath,lines):
		self.relpath = relpath

		self.commands = []
		for line in lines:
			self.commands.append(self.create_command_object(line))

	def create_command_object(self,line):
		from command import Command
		return Command(line.strip())

	def execute(self,executed_by=False,executed_at=False,depth=0):
		if depth > 300:
			return False

		for command in self.commands:
			if command.is_valid:
				command.execute(executed_by,executed_at,depth)