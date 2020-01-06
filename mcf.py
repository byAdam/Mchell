import os, sys, atexit, time
from function import Function
from command import Command
from world import main_world

def exit_handler():
    main_world.save_world()

def return_options(args):
    options = {"help":False,"loop":False,"write":False,"read":False,"path":False,"dir":False}

    for a in args:
        ## Splits arguments if they have a "=" in them
        if "=" in a:
            o, v = a.split("=")
        else:
            o = a

        if o[0] == "-":
            if o in ("-h","--help"):
                options["help"] = True
            elif o in ("-l","--loop"):
                options["loop"] = True
            elif o in ("-w","--write"):
                options["write"] = True
            elif o in ("-r","--read"):
                options["read"] = True
            elif o in ("-d","--dir"):
                options["dir"] = v
            else:
                raise Exception("Unknown option: {}".format(o))
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

if __name__ == "__main__":
    args = sys.argv[1:]

    options = return_options(args)
    
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