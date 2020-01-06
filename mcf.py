import os, sys, atexit, time, json
from function import Function
from command import Command
from world import main_world

def exit_handler():
    main_world.save_world()

def return_options(args):
    options = {"help":False,"loop":False,"write":False,"read":False,"path":False,"dir":False}

    for a in args:
        ## Splits arguments if they have a "=" in them
        v = False
        if "=" in a:
            o, v = a.split("=")
        else:
            o = a

        if o[0] == "-":
            valid_option = False
            for option in option_schema:
                option_data = option_schema[option]
                if o in option_data["flags"]:
                    if option_data["has_value"]:
                        if v:
                            options[option] = v
                        else:
                            raise Exception("Missing Value: {}".format(o))
                    else:
                        options[option] = True

                    valid_option = True
                    break

            if not valid_option:
                raise Exception("Unknown Option: {}".format(o))

        elif not options["path"]:
            options["path"] = o

    if not options["dir"]:
        if options["path"]:
            options["dir"] = os.path.dirname(options["path"])
        else:
            # Sets dir the current working directory
            options["dir"] = os.getcwd()

    return options

def run_function(f):
    main_world.functions[f].add_to_command_stack("primary")
    main_world.process_command_stack()

def shell():
    while True:
        inp = input("> ")
        command = Command(inp).execute("primary")

def return_option_schema():
    if hasattr(sys, "frozen"):
        p = os.path.dirname(sys.executable)
    else:
        p = os.path.dirname(__file__)

    if p:
        path = "{}/schemas/option.json".format(p)
    else:
        path = "schemas/option.json"

    with open(path) as f:
        return json.load(f)

def help():
    for option in option_schema:
        option_data = option_schema[option]
        flags = ", ".join(option_data["flags"])
        if option_data["has_value"]:
            flags += " = VALUE"
        description = option_data["description"]
        print("{}: {}".format(flags, description))
    sys.exit(0)

if __name__ == "__main__":
    args = sys.argv[1:]

    option_schema = return_option_schema()
    options = return_options(args)
    
    if options["help"]:
        help()

    if options["read"]:
        main_world.load_world(options["dir"],True)
    else:
        main_world.load_world(options["dir"],False)

    if options["write"]:
        atexit.register(exit_handler)

    main_world.place_entity((0,0,0),"player","main","primary")

    if options["path"]:
        if os.path.isfile(options["path"]):
            main_function = os.path.relpath(options["path"],main_world.directory)
            ## Remove file type
            main_function = ".".join(main_function.split(".")[:-1])

            main_world.load_function(main_function)
            run_function(main_function)
            # If loop is true
            while options["loop"]:
                run_function(main_function)
        else:
            raise Exception("Unknown File: {}".format(options["path"]))
    else:
        shell()