import math  

class IllegalPositionError(RuntimeError):
   def __init__(self, arg):
      self.args = arg

class WorldCoherenceError(RuntimeError):
   def __init__(self, arg):
      self.args = arg

class NoModelError(RuntimeError):
   def __init__(self, arg):
      self.args = arg

class NoElemError(RuntimeError):
   def __init__(self, arg):
      self.args = arg

class Elem:

    _next_id = 0
    _color = "White"
    _type = "Elem"

    def __init__(self, model, *, typology= "Elem", color = "White"):

        self.id = Elem._next_id
        Elem._next_id += 1
        self.model = model
        self.set_type(typology)
        self.set_color(color)
        

    def get_id(self):
        return self.id

    def get_pos(self):
        if self.model == None:
            raise NoModelError("Element "+str(self.id)+" has no model")
        return self.model.get_pos(self.id)

    def get_row(self):
        return self.get_pos()[0]

    def get_column(self):
        return self.get_pos()[1]

    def set_type(self, typology):
        self.type = typology
        
    def get_type(self):
        return self.type

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def detach(self):
        if self.mode != None
            self.model = None
            self.remove(self.Id)

    def attach(self, model):
        self.model = model
        self.model.add_elem(self)

    def move(self, dx, dy):
        if self.model == None:
            raise NoModelError("Element "+str(self.id)+" has no model") 
        pos = self.get_pos()
        return self.model.move_elem(self.id, (pos[0]+dx, pos[1]+dy))

    def set_pos(self, pos):
        if self.model == None:
            raise NoModelError("Element "+str(self.id)+" has no model") 
        return self.model.move_elem(self.id, pos)

    def view(self, depth):
        if self.model == None:
            raise NoModelError("Element "+str(self.id)+" has no model") 

        elems = self.model.get_elems()
        newList = []

        for elem in elems:
            if elem[1] != self and Model.distance(self.get_pos(),elem[0]) <= depth:
                newList.append(elem)
        return newList


class Agent():
    
    _next_id = 0
    _color = "Red"
    _type = "Agent"

    def __init__(self, elem, *, speed = 1, typology = "Agent", color = "Red"):

        self.id = Agent._next_id
        Agent._next_id += 1
        self.type = typology
        self.color = color
        self.attach(elem)
        self.angle = 0
        self.speed = speed
        

    def get_id(self):
        return self.id

    def attach(self, elem):
        self.elem = elem
        self.set_type(self.type)

        self.set_color(self.color)

    def detach(self):
        self.elem = None

    def get_elem_id(self):
        if self.elem == None:
            raise NoElemError("Agent "+str(self.id)+" has no elem") 
        return self.elem.get_id()

    def get_pos(self):
        if self.elem == None:
            raise NoElemError("Agent "+str(self.id)+" has no elem") 
        return self.elem.get_pos()

    def get_row(self):
        return self.get_pos()[0]

    def get_column(self):
        return self.get_pos()[1]

    def set_type(self, typology):
        if self.elem == None:
            raise NoElemError("Agent "+str(self.id)+" has no elem") 
        self.type = typology
        self.elem.set_type(typology)

    def get_type(self):
        return self.type

    def set_speed(self, speed):
        self.speed = speed
    
    def get_speed(self):
        return self.speed

    def set_color(self, color):
        if self.elem == None:
            raise NoElemError("Agent "+str(self.id)+" has no elem") 
        self.color = color
        self.elem.set_color(color)

    def get_color(self):
        return self.color

    def turn(self, dt):
        if dt > 180:
            dt = dt - 360
        elif dt < -180:
            dt = dt + 360
        self.angle += dt

    def move(self, dx, dy):
        if self.elem == None:
            raise NoElemError("Agent "+str(self.id)+" has no elem") 
        return self.elem.move(dx, dy)

    def set_pos(self, pos):
        if self.elem == None:
            raise NoElemError("Agent "+str(self.id)+" has no elem") 
        return self.elem.set_pos(pos)

    def view(self, depth, angle):
        if self.elem == None:
            raise NoElemError("Agent "+str(self.id)+" has no elem") 
        elems = self.elem.view(depth)
        angle = angle/2
        newList = []

        for elem in elems:
            my_angle = Model.angle(self.get_pos(),elem[0])-self.angle # -self.angle per implementare rotazioni mediante turn
            if my_angle > 180:
                my_angle = my_angle - 360
            elif my_angle < -180:
                my_angle = my_angle + 360
            if my_angle >= -angle and my_angle <= angle:
                newList.append(elem)
        return newList

    def run(self):
        print(self.id)


class Simulator:

    def __init__(self):

        self.agents = {} #id -> Agent
        self.disabled = {}

    def get_agent(self, Id):
        try:
            return self.agents[Id]
        except KeyError:
            return None

    def add_agent(self, elem, *, typology= Agent._type, color = Agent._color):
        agent = Agent(elem, typology = typology, color = color)
        self.agents[agent.get_id()] = agent
        return agent

    def disable(self, Id):
        agent = None
        try:
            agent = self.agents[Id]
        except KeyError:
            return None
        self.disabled[Id] = agent
        self.agents.pop(Id)
        return agent

    def enable(self, Id):
        agent = None
        try:
            agent = self.disabled[Id]
        except KeyError:
            return None
        self.agents[Id] = agent
        self.disabled.pop(Id)
        return agent
        
    def run(self):
        for a in self.agents.values():
            for _ in range(a.get_speed()):
                a.run()

    def __str__(self):
        return str(self.agents)

class Model:

    def __init__(self, row, column):

        self.row = row
        self.column = column
        self.grid = [[None for i in range(column)] for i in range(row)] # (x,y) -> Elem
        self.elems = {} #id -> (x,y)
        
        self.f_update = lambda x: None

    def __str__(self):
        w = "" 
        for r in range(self.row):
            for c in range(self.column):
                elem = self.grid[r][c]
                if  elem != None:
                    w += str(elem.get_id()) + " "
                else:
                    w += "* "
            w += "\n"
        w += "\n"

        for k in self.elems:
            elem = self.get_elem(self.elems[k])
            w += str(k) + " -> " + str(elem.get_type()) + " " + str(elem.get_color()) + "\n"
        
        return w

    def get_free_pos(self):
        for r in range(self.row):
            for c in range(self.column):
                if self.grid[r][c] == None:
                    return (r,c)
        return None

    def is_free_pos(self, pos):
        self._check_pos(pos)
        if self.grid[pos[0]][pos[1]] == None:
            return True
        return False

    def add_elem(self, elem):
        pos = self.get_free_pos()
        if pos != None:
            self.elems[elem.get_id()] = pos
            self.grid[pos[0]][pos[1]] = elem
            return elem
        else:
            raise WorldCoherenceError("No more space in the grid")

    def new_elem(self, *, typology= Elem._type, color = Elem._color):
        elem = Elem(self, typology = typology, color = color)
        return self.add_elem(elem)

    def remove(self, Id):
        try:
            pos = self.get_pos(Id)
            elem = self.get_elem(pos)
            elem.detach()
            self.grid[pos[0]][pos[1]] = None
            self.elems.pop(Id)
            return elem
        except KeyError:
            return None

    def get_pos(self, Id):
        try:
            return self.elems[Id]
        except KeyError:
            return None

    def get_elem(self, pos):
        self._check_pos(pos)
        return self.grid[pos[0]][pos[1]]

    def get_elem_id(self, Id):
        return self.get_elem(self.get_pos(Id))

    def get_elems(self):
        elemList = []
        for pos in self.elems.values():
            elem = self.get_elem(pos)
            elemList.append((pos,elem))
        return elemList

    def move_elem(self, Id, newPos):
       
         try:
            self._check_pos(newPos)
         except IllegalPositionError:
            return False

         oldPos = self.get_pos(Id)
         elem = self.get_elem(oldPos)

         if self.is_free_pos(newPos):
            self.grid[oldPos[0]][oldPos[1]] = None
            self.grid[newPos[0]][newPos[1]] = elem
            self.elems[Id] = newPos
            self._update(Id, oldPos, newPos)
            return True

         return self.get_elem(newPos)

    def _update(self, Id, oldPos, newPos):
        self.f_update(Id, oldPos, newPos)

    def on_update(self, f):
        self.f_update = f

    def _check_pos(self, pos):
        if int(pos[0]) < 0 or int(pos[1]) < 0 or int(pos[0]) >= self.row or int(pos[1]) >= self.column:
            raise IllegalPositionError(pos)

    @staticmethod
    def distance(p1, p2):
       dist = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)  
       return dist

    @staticmethod
    def angle(p1, p2):
       radians = math.atan2(p1[1]-p2[1], p1[0]-p2[0])
       degrees = math.degrees(radians)
       return degrees


class World:
    pass

m = Model(3,3)
w = Simulator()

def f(i, o, n):
   print(str(i) +" "+str(o)+" "+str(n))

m.on_update(f)

agents = [w.add_agent(m.new_elem()) for i in range(9)]

w.get_agent(4).turn(-180)

pos = w.get_agent(4).get_pos()

"""for i in range(9):
    print(str(i)+" -> "+str(Model.angle((pos), w.get_agent(i).get_pos())))

print(agents[4].view(math.inf,360))"""
