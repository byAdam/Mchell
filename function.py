class Function():
    def __init__(self,relpath,lines):
        self.relpath = relpath
        self.commands = []
        self.process_lines(lines)

    def process_lines(self, lines):
        from world import main_world
        i = 0
        while i < len(lines):
            line = lines[i]

            if line.startswith("def"):
                subfunc_name = line[4:].strip()
                subfunc_lines = []

                j = i + 1
                while j < len(lines) and (lines[j].startswith("\t") or lines[j].isspace()):
                    subfunc_lines.append(lines[j][1:])
                    j += 1
                i = j - 1

                main_world.functions[subfunc_name] = Function(subfunc_name, subfunc_lines)
            else:
                self.commands.append(self.create_command_object(line))

            i += 1


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
