import uuid, random, os,json
from math import sqrt
from function import Function

class World:
    def __init__(self):
        self.blocks = {}
        self.entities = {}
        self.scoreboards = {}
        self.functions = {}
        self.command_stack = []
        self.is_processing = False
        self.directory = ""

    def save_world(self):
        world = {"blocks":self.blocks,"entities":self.entities,"scoreboards":self.scoreboards}
        with open(os.path.join(self.directory,"world.json"),"w+") as f:
            json.dump(world,f)

    def load_world(self,directory,do_save):
        self.directory = directory
        if do_save:
            if os.path.isfile(os.path.join(directory,"world.json")):
                with open(os.path.join(directory,"world.json")) as f:
                    try:
                        world = json.load(f)
                        self.blocks = world["blocks"]
                        self.entities = world["entities"]
                        self.scoreboards = world["scoreboards"]
                    except:
                        pass

    def process_command_stack(self):
        self.is_processing = True
        while self.command_stack:
            command_info = self.command_stack.pop(0)
            command_info["command"].execute(command_info["executed_by"],command_info["executed_at"])
        self.is_processing = False

    def load_function(self,relpath):
        path = os.path.join(self.directory,relpath) + ".mcfunction"
        if os.path.isfile(path):
            with open(path) as f:
                self.functions[relpath] = Function(relpath,f.readlines())
                return True
        return False


    def place_block(self,coordinates,block,data=False):
        if not data:
            data = 0
        self.blocks[coordinates] = {"block":block,"data":data}

    def get_block(self,coordinates):
        if coordinates in self.blocks:
            return self.blocks[coordinates]
        else:
            return {"block":"air","data":0}

    def get_blocks(self,coordinates_a,coordinates_b,is_relative=True):
        min_x = min(coordinates_a[0],coordinates_b[0])
        min_y = min(coordinates_a[1],coordinates_b[1])
        min_z = min(coordinates_a[2],coordinates_b[2])     
        max_x = max(coordinates_a[0],coordinates_b[0])
        max_y = max(coordinates_a[1],coordinates_b[1])
        max_z = max(coordinates_a[2],coordinates_b[2])

        blocks = {} 

        x = min_x
        while x <= max_x:
            y = min_y
            while y <= max_y:
                z = min_z
                while z <= max_z:
                    if is_relative:
                        k = (x-coordinates_a[0],y-coordinates_a[1],z-coordinates_a[2])
                    else:
                        k = (x,y,z)
                    blocks[k] = self.get_block((x,y,z))   
                    z += 1
                y += 1
            x += 1

        return blocks

    def place_entity(self,coordinates,entity,name=False,u=False):
        if not name:
            name = entity
        if not u:
            u = str(uuid.uuid4())
        self.entities[u] = {"coordinates":coordinates,"entity":entity,"uuid":u,"name":name,"tags":[]}

    def remove_entity(self,u):
        if u in self.entities:
            del self.entities[u]

    def move_entity(self,u,coordinates):
        self.entities[u]["coordinates"] = coordinates

    def add_objective(self,objective):
        if objective not in self.scoreboards:
            self.scoreboards[objective] = {}

    def remove_objective(self,objective):
        if objective in self.scoreboards:
            del self.scoreboards[objective]

    def reset_entity_scores(self,u,objective=False):
        if objective and objective in self.scoreboards:
            if u in self.scoreboards[objective]:
                del self.scoreboards[objective][u]
        else:
            for o in self.scoreboards:
                if u in self.scoreboards[o]:
                    del self.scoreboards[o][u]

    def set_entity_score(self,u,method,objective,count):
        if objective in self.scoreboards:
            if u not in self.scoreboards[objective]:
                self.scoreboards[objective][u] = 0
            if method == "set":
                self.scoreboards[objective][u] = int(count)
            elif method == "add":
                self.scoreboards[objective][u] += int(count)
            elif method == "remove":
                self.scoreboards[objective][u] -= int(count)

    def get_entity_score(self,u,objective):
        if objective in self.scoreboards:
            if u in self.scoreboards[objective]:
                return self.scoreboards[objective][u]

    def add_tag(self,u,tag):
        if tag not in self.entities[u]["tags"]:
            self.entities[u]["tags"].append(tag)

    def remove_tag(self,u,tag):
        if tag in self.entities[u]["tags"]:
            self.entities[u]["tags"].remove(tag)

    def get_entities(self,kwargs):
        valid_entities = {}
        coordinates = kwargs["coordinates"]
        for u, e in self.entities.items():
            if "u" in kwargs and u != kwargs["u"]:
                continue

            is_valid = True
            for k, v in kwargs.items():
                if k == "dx":
                    if abs(e["coordinates"][0] - coordinates[0]) > float(v):
                        is_valid = False
                        break
                elif k == "dy":
                    if abs(e["coordinates"][1] - coordinates[1]) > float(v):
                        is_valid = False
                        break
                elif k == "dz":
                    if abs(e["coordinates"][2] - coordinates[2]) > float(v):
                        is_valid = False
                        break
                elif k == "name":
                    if e["name"] != v:
                        is_valid = False
                        break
                elif k == "r":
                    if self.get_distance(coordinates,e["coordinates"]) > float(v):
                        is_valid = False
                        break
                elif k == "rm":
                    if self.get_distance(coordinates,e["coordinates"]) <= float(v):
                        is_valid = False
                        break
                elif k == "scores":
                    for s in v:
                        score = self.get_entity_score(u,s["objective"])
                        if "not" in s:
                            if score == s["not"]:
                                is_valid = False
                                break
                        if "min" in s and s["min"] != None:
                            if score == None or score < s["min"]:
                                is_valid = False
                                break
                        if "max" in s and s["max"] != None:
                            if score == None or score > s["max"]:
                                is_valid = False
                                break

                elif k == "tags":
                    for t in v:
                        if t[0] != "!" and t not in e["tags"]:
                            is_valid = False
                            break
                        elif t[0] == "!" and t in e["tags"]:
                            is_valid = False
                            break
                elif k == "type":
                    if e["entity"] != v:
                        is_valid = False
                        break
            if is_valid:
                valid_entities[u] = e

        if "c" in kwargs or ("random" in kwargs and kwargs["random"]):
            c = kwargs["c"]
            distances = []
            for u, e in valid_entities.items():
                distances.append((self.get_distance(e["coordinates"],coordinates),u))

            if "random" in kwargs and kwargs["random"]:
                random.shuffle(distances)
            else:
                distances.sort()

            i = int(c)
            while i < len(distances):
                del distances[i]

            return [e[1] for e in distances]

        else:
            return list(valid_entities.keys())

    def get_distance(self,coordinates_a,coordinates_b):
        dist = 0
        for i in [0,1,2]:
            diff = coordinates_a[i]-coordinates_b[i]
            dist += diff * diff
        return sqrt(dist)

main_world = World()

if __name__ == "__main__":
    print(main_world.calculare_coordinates((1,0,0),("~","~","")))