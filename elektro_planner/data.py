from enum import Enum
from math import sqrt
class VerticalPosition(Enum):
     Unten = 0
     Mitte = 1
     Oben = 2
     Decke = 3
     def __str__(self):
        return str(self.name)
     @staticmethod
     def from_str(label):
        if label in ('decke', 'Decke'):
            return VerticalPosition.Decke
        elif label in ('unten', 'Unten','Steckdose','steckdose'):
            return VerticalPosition.Unten
        elif label in ('mitte', 'Mitte','Schalter','schalter'):
            return VerticalPosition.Mitte
        elif label in ('oben', 'Oben'):
            return VerticalPosition.Oben
        else:
            raise NotImplementedError

class KnxType(Enum):
     NoKnx = 0
     Rolladen = 1
     Input = 2
     Schaltbar = 3
     Dimmbar = 4
     def __str__(self):
        return str(self.name)
     @staticmethod
     def from_str(label):
        if label in ('NoKnx', 'noknx', 'empty', 'Empty'):
            return KnxType.NoKnx
        elif label in ('Rolladen', 'rolladen', 'Motor', 'motor'):
            return KnxType.Rolladen
        elif label in ('Input', 'input'):
            return KnxType.Input
        elif label in ('Schaltbar', 'schaltbar'):
            return KnxType.Schaltbar
        elif label in ('Dimmbar', 'dimmbar'):
            return KnxType.Dimmbar
        else:
            raise NotImplementedError

class KnxAnschluss(Enum):
     Reserve = 0
     Praesenzmelder = 1
     Glastaster = 2
     @staticmethod
     def from_str(label):
        if label in ('re', 'unused', 'empty', 'reserve'):
            return KnxAnschluss.Reserve
        elif label in ('pm', 'PM'):
            return KnxAnschluss.Praesenzmelder
        elif label in ('gt', 'glastaster'):
            return KnxAnschluss.Glastaster
        else:
            print("KnxAnschluss Type unkown: {}".format(label))
            raise NotImplementedError

class KabelType(Enum):
     NYM5x15 = 0
     NYM5x25 = 1
     CAT7 = 2
     KNX = 3
     FMK = 4
     def __str__(self):
        return str(self.name)
     @staticmethod
     def from_str(label):
        if label in ('nym5x15', 'NYM5x15','nym5x1.5', 'NYM5x1.5'):
            return KabelType.NYM5x15
        elif label in ('nym5x25', 'NYM5x25','nym5x2.5', 'NYM5x2.5'):
            return KabelType.NYM5x25
        elif label in ('cat7', 'CAT7','Netzwerk','netzwerk'):
            return KabelType.CAT7
        elif label in ('knx', 'Knx', 'eib', 'Eib'):
            return KabelType.KNX
        elif label in ('fernmelde', 'FMK', 'Kontakte', 'Fernmelde'):
            return KabelType.FMK
        else:
            raise NotImplementedError

def read_value_from_yaml(yaml,value,throw=True):
    if yaml != None and value in yaml:
        return yaml[value]
    else:
        if throw:
            raise RuntimeError("{} in YAML nich gesetzt: {}".format(value,yaml))
        else:
            return None

def read_value_from_yaml_to_enum(yaml,value,enum,throw=True):
    if yaml != None and value in yaml:
        return enum.from_str(yaml[value])
    else:
        if throw:
            raise RuntimeError("{} in YAML nich gesetzt: {}".format(value,yaml))
        else:
            return enum(0)

class Position:
    def __init__(self,yaml):
       self.horizontal = [0,0]
       if yaml != None:
         st = "hori"
         if st in yaml:
            self.horizontal = [float(eval(str(yaml[st][0]))),float(eval(str(yaml[st][1])))]
       self.vertical = read_value_from_yaml_to_enum(yaml,"vert",VerticalPosition,False)

class Haus:
    def __init__(self):
        self.geschosse = []
        self.book = dict()
        self.geschoss_count = 0
        self.room_count = 0
        self.kabel = []
        self.edges = dict()

class Geschoss:
    def __init__(self,yaml,z):
        self.id = read_value_from_yaml(yaml,"id")
        self.cid = self.id
        self.name = read_value_from_yaml(yaml,"name")
        # starthöhe des stockwerks
        self.z0 = z
        self.height = read_value_from_yaml(yaml,"height")
        self.z1 = self.z0 + self.height
        self.rooms = []
        self.walls = []
        self.windows = []
        self.doors = []
        self.edges = []
        self.book = dict()

class Room:
    def __init__(self,yaml,parent):
        self.id = read_value_from_yaml(yaml,"id")
        self.cid = str(parent.cid)+"."+str(self.id)
        self.name = read_value_from_yaml(yaml,"name")
        self.objects = []
        self.book = dict()

class Point:
    def __init__(self,yaml,parent):
        self.id = read_value_from_yaml(yaml,"id")
        self.cid = str(parent.cid)+"."+str(self.id)
        self.pos = Position(yaml["pos"])
        self.parent = parent
        self.x = self.pos.horizontal[0]
        self.y = self.pos.horizontal[1]
        values = [30, 105, 200, 230]
        self.z = values[self.pos.vertical.value]

class Object(Point):
    def __init__(self,yaml,parent):
        super().__init__(yaml,parent)
        self.name = read_value_from_yaml(yaml,"name")
        self.connection_type = KabelType.NYM5x15
        self.associated_wall = None
        self.associated_edge = None
    def draw(self,dwg):
        x = self.pos.horizontal[0] * 10
        y = self.pos.horizontal[1] * 10
        xe = 50
        ye = 50
        xs = x - xe * 0.5
        ys = y - ye * 0.5
        draw_obj = dwg.rect((xs,ys), (xe,ye), style="cursor:crosshair", stroke="blue", fill="blue")
        draw_obj['class'] = 'object'
        dwg.add(draw_obj)

class Stromanschluss(Object):
    def __init__(self,yaml,parent):
        super().__init__(yaml,parent)
        self.anzahl = read_value_from_yaml(yaml,"anzahl")
        self.stromstaerke = 0
        self.voltage = 230
        self.knx = read_value_from_yaml_to_enum(yaml,"knx",KnxType,False)
        self.connection_type = read_value_from_yaml_to_enum(yaml,"kabelanschluss",KabelType,False)

class Steckdose(Stromanschluss):
    def __init__(self,yaml,parent):
        super().__init__(yaml,parent)

class Licht(Stromanschluss):
    def __init__(self,yaml,parent):
        super().__init__(yaml,parent)
        if self.knx !=KnxType.Schaltbar:
            raise RuntimeError("Licht nicht schaltbar: {}".format(self.cid))
        self.color = "yellow"
    def draw(self,dwg):
        x = self.pos.horizontal[0] * 10
        y = self.pos.horizontal[1] * 10
        line_width = 15
        r = 100
        xs = x
        ys = y
        draw_obj = dwg.circle((xs,ys), r, style="cursor:crosshair", stroke=self.color, stroke_width=line_width , fill="none", id="licht_"+str(self.id))
        draw_obj['class'] = 'led'
        xes = x - r / sqrt(2)
        yes = y + r / sqrt(2)
        xss = x + r / sqrt(2)
        yss = y - r / sqrt(2)
        line1 = dwg.line(start=(xss,yss), end=(xes,yes), style="cursor:crosshair", stroke=self.color, stroke_width = line_width, fill=self.color)
        yes = y - r / sqrt(2)
        yss = y + r / sqrt(2)
        line2 = dwg.line(start=(xss,yss), end=(xes,yes), style="cursor:crosshair", stroke=self.color, stroke_width = line_width, fill=self.color)
        line1['class'] = 'led'
        line2['class'] = 'led'
        xes = x - r / sqrt(2)
        xes = x - r / sqrt(2)
        dwg.add(line1)
        dwg.add(line2)
        dwg.add(draw_obj)

class Led(Licht):
    def __init__(self,yaml,parent):
        super().__init__(yaml,parent)
        self.voltage = 24
        self.knx = KnxType.Dimmbar
        self.color = "orange"

class LedStrip(Led):
    def __init__(self,yaml,parent):
        super().__init__(yaml,parent)
        self.color = "purple"
        self.len = read_value_from_yaml(yaml,"len")
    def draw(self,dwg):
        x = self.pos.horizontal[0] * 10
        y = self.pos.horizontal[1] * 10
        line_width = 45
        xe = x + self.len[0] * 10
        ye = y + self.len[1] * 10
        line1 = dwg.line(start=(x,y), end=(xe,ye), style="cursor:crosshair", stroke=self.color, stroke_width = line_width, fill=self.color)
        line1['class'] = 'led'
        dwg.add(line1)
        len_strip = sqrt(self.len[0]**2 + self.len[1]**2)
        dx = self.len[1] * 100 / len_strip
        dy = self.len[0] * 100 / len_strip
        xs = x + dx
        ys = y + dy
        xe = x - dx
        ye = y - dy
        line2 = dwg.line(start=(xs,ys), end=(xe,ye), style="cursor:crosshair", stroke=self.color, stroke_width = line_width, fill=self.color)
        line2['class'] = 'led'
        dwg.add(line2)
        x += self.len[0] * 10
        y += self.len[1] * 10
        xs = x + dx
        ys = y + dy
        xe = x - dx
        ye = y - dy
        line3 = dwg.line(start=(xs,ys), end=(xe,ye), style="cursor:crosshair", stroke=self.color, stroke_width = line_width, fill=self.color)
        line3['class'] = 'led'
        dwg.add(line3)

class Kontakt(Object):
    def __init__(self,yaml,parent):
        super().__init__(yaml,parent)
        self.anzahl = read_value_from_yaml(yaml,"anzahl")
        self.knx = read_value_from_yaml_to_enum(yaml,"knx",KnxType,False)
        self.connection_type = KabelType.FMK
    def draw(self,dwg):
        xs = self.pos.horizontal[0] * 10
        ys = self.pos.horizontal[1] * 10
        xe = xs + 100
        ye = ys - 100
        draw_obj = dwg.line(start=(xs,ys), end=(xe,ye), style="cursor:crosshair", stroke="purple", stroke_width = 30, fill="purple")
        draw_obj['class'] = 'kontakt'
        dwg.add(draw_obj)

class Knx(Object):
    def __init__(self,yaml,parent):
        super().__init__(yaml,parent)
        self.knx_anschluss = read_value_from_yaml_to_enum(yaml,"knx-component",KnxAnschluss)
        self.connection_type = KabelType.KNX
    def draw(self,dwg):
        x = self.pos.horizontal[0] * 10
        y = self.pos.horizontal[1] * 10
        xs = x
        ys = y
        xe = 50
        ye = 50
        if self.knx_anschluss is KnxAnschluss.Praesenzmelder:
            r = 5000
            xs = x
            ys = y
            draw_obj = dwg.circle((xs,ys), r, style="cursor:crosshair", stroke="green", fill="none")
            draw_obj['class'] = 'knx_pm_radius'
            dwg.add(draw_obj)
            r = 1500
            xs = x
            ys = y
            draw_obj = dwg.circle((xs,ys), r, style="cursor:crosshair", stroke="green", fill="none")
            draw_obj['class'] = 'knx_pm_dist_licht'
            dwg.add(draw_obj)
            xe = 85
            ye = 85
            xs = x - xe * 0.5
            ys = y - ye * 0.5
            draw_obj = dwg.rect((xs,ys), (xe,ye), style="cursor:crosshair", stroke="green", fill="green")
            draw_obj['class'] = 'knx'
        else:
            xe = xs + 100
            ye = ys + 100
            draw_obj = dwg.line(start=(xs,ys), end=(xe,ye), style="cursor:crosshair", stroke="green", stroke_width = 30, fill="green")
            draw_obj['class'] = 'knx'
        dwg.add(draw_obj)

class Netzwerk(Object):
    def __init__(self,yaml,parent):
        super().__init__(yaml,parent)
        self.anzahl = read_value_from_yaml(yaml,"anzahl")
        self.connection_type = KabelType.CAT7
    def draw(self,dwg):
        xs = self.pos.horizontal[0] * 10
        ys = self.pos.horizontal[1] * 10
        xe = xs + 100
        ye = ys
        draw_obj = dwg.line(start=(xs,ys), end=(xe,ye), style="cursor:crosshair", stroke="red", stroke_width = 30, fill="red")
        draw_obj['class'] = 'netzwerk'
        dwg.add(draw_obj)

class Wall(Point):
    def __init__(self,yaml,parent):
        self.dx = 0
        self.dy = 0
        super().__init__(yaml,parent)
        self.edges = []
        st = "ende"
        if yaml != None and st in yaml:
            self.dx = float(eval(str(yaml[st][0])))
            self.dy = float(eval(str(yaml[st][1])))
        self.waagrecht = self.dx>self.dy

class Window(Point):
    def __init__(self,yaml,parent):
        self.dx = 0
        self.dy = 0
        super().__init__(yaml,parent)
        self.x = self.pos.horizontal[0]
        self.y = self.pos.horizontal[1]
        st = "ende"
        if yaml != None and st in yaml:
            self.dx = float(eval(str(yaml[st][0])))
            self.dy = float(eval(str(yaml[st][1])))
class Door(Point):
    def __init__(self,yaml,parent):
        self.dx = 0
        self.dy = 0
        super().__init__(yaml,parent)
        self.x = self.pos.horizontal[0]
        self.y = self.pos.horizontal[1]
        st = "ende"
        if yaml != None and st in yaml:
            self.dx = float(eval(str(yaml[st][0])))
            self.dy = float(eval(str(yaml[st][1])))
class Edge:
    id_counter = 0
    def __init__(self,x,y,z,parent):
        self.x = x
        self.y = y
        self.z = z
        self.n = 1
        self.id = Edge.id_counter
        Edge.id_counter += 1
        self.parent = parent
        self.connections = []
    def __str__(self):
        return "Edge {} Position: {} {} {}, N: {}".format(self.id, self.x,self.y,self.z,self.n)

class Kabel:
    def __init__(self,yaml):
        self.start = read_value_from_yaml(yaml,"start")
        self.end = read_value_from_yaml(yaml,"end")
        self.type = None
        self.length = 0.0
        # print(" Kabel from {} to {}: {}".format(self.start,len(self.end),self.end))
