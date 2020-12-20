from enum import Enum
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
            self.horizontal = [yaml[st][0],yaml[st][1]]
       self.vertical = read_value_from_yaml_to_enum(yaml,"vert",VerticalPosition,False)

class Haus:
    def __init__(self):
        self.geschosse = []

class Geschoss:
    def __init__(self,yaml):
        self.id = read_value_from_yaml(yaml,"id")
        self.name = read_value_from_yaml(yaml,"name")
        self.height = read_value_from_yaml(yaml,"height",False)
        self.rooms = []
        self.walls = []

class Room:
    def __init__(self):
        self.objects = []

class Point:
    def __init__(self,yaml,parent):
        self.id = read_value_from_yaml(yaml,"id")
        self.pos = Position(yaml["pos"])
        self.parent = parent

class Object(Point):
    def __init__(self,yaml,parent):
        super().__init__(yaml,parent)
        self.name = read_value_from_yaml(yaml,"name")

class Stromanschluss(Object):
    def __init__(self,yaml,parent):
        super().__init__(yaml,parent)
        self.anzahl = read_value_from_yaml(yaml,"anzahl")
        self.stromstaerke = 0
        self.knx = read_value_from_yaml_to_enum(yaml,"knx",KnxType,False)

class Steckdose(Stromanschluss):
    def __init__(self,yaml,parent):
        super().__init__(yaml,parent)
        # print( "Adding Steckdose: {}".format(self.id) )
        pass

class Licht(Stromanschluss):
    def __init__(self,yaml,parent):
        super().__init__(yaml,parent)
        # print( "Adding Licht: {}".format(self.id) )
        pass

class Kontakt(Object):
    def __init__(self,yaml,parent):
        super().__init__(yaml,parent)
        self.anzahl = read_value_from_yaml(yaml,"anzahl")
        self.knx = read_value_from_yaml_to_enum(yaml,"knx",KnxType,False)

class Knx(Object):
    def __init__(self,yaml,parent):
        super().__init__(yaml,parent)
        self.knx_anschluss = read_value_from_yaml_to_enum(yaml,"knx-component",KnxAnschluss)

class Netzwerk(Object):
    def __init__(self,yaml,parent):
        super().__init__(yaml,parent)
        self.anzahl = read_value_from_yaml(yaml,"anzahl")

class Wall(Point):
    def __init__(self,yaml,parent):
        self.dx = 0
        self.dy = 0
        super().__init__(yaml,parent)
        self.x = self.pos.horizontal[0]
        self.y = self.pos.horizontal[1]
        st = "ende"
        if yaml != None and st in yaml:
            self.dx = yaml[st][0]
            self.dy = yaml[st][1]
