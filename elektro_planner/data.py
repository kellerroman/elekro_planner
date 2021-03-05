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
        if label in ("decke", "Decke"):
            return VerticalPosition.Decke
        elif label in ("unten", "Unten", "Steckdose", "steckdose"):
            return VerticalPosition.Unten
        elif label in ("mitte", "Mitte", "Schalter", "schalter"):
            return VerticalPosition.Mitte
        elif label in ("oben", "Oben"):
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
        if label in ("NoKnx", "noknx", "empty", "Empty"):
            return KnxType.NoKnx
        elif label in ("Rolladen", "rolladen", "Motor", "motor"):
            return KnxType.Rolladen
        elif label in ("Input", "input"):
            return KnxType.Input
        elif label in ("Schaltbar", "schaltbar"):
            return KnxType.Schaltbar
        elif label in ("Dimmbar", "dimmbar"):
            return KnxType.Dimmbar
        else:
            raise NotImplementedError


class KnxAnschluss(Enum):
    Reserve = 0
    Praesenzmelder = 1
    Glastaster = 2

    @staticmethod
    def from_str(label):
        if label in ("re", "unused", "empty", "reserve"):
            return KnxAnschluss.Reserve
        elif label in ("pm", "PM"):
            return KnxAnschluss.Praesenzmelder
        elif label in ("gt", "glastaster"):
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
        if label in ("nym5x15", "NYM5x15", "nym5x1.5", "NYM5x1.5"):
            return KabelType.NYM5x15
        elif label in ("nym5x25", "NYM5x25", "nym5x2.5", "NYM5x2.5"):
            return KabelType.NYM5x25
        elif label in ("cat7", "CAT7", "Netzwerk", "netzwerk"):
            return KabelType.CAT7
        elif label in ("knx", "Knx", "eib", "Eib"):
            return KabelType.KNX
        elif label in ("fernmelde", "FMK", "Kontakte", "Fernmelde"):
            return KabelType.FMK
        else:
            raise NotImplementedError


def read_value_from_yaml(yaml, value, throw=True):
    if yaml != None and value in yaml:
        return yaml[value]
    else:
        if throw:
            raise RuntimeError("{} in YAML nich gesetzt: {}".format(value, yaml))
        else:
            return None


def read_value_from_yaml_to_enum(yaml, value, enum, throw=True):
    if yaml != None and value in yaml:
        return enum.from_str(yaml[value])
    else:
        if throw:
            raise RuntimeError("{} in YAML nich gesetzt: {}".format(value, yaml))
        else:
            return enum(0)


class Position:
    def __init__(self, yaml):
        self.horizontal = [0, 0]
        if yaml != None:
            st = "hori"
            if st in yaml:
                self.horizontal = [
                    float(eval(str(yaml[st][0]))),
                    float(eval(str(yaml[st][1]))),
                ]
        self.vertical = read_value_from_yaml_to_enum(
            yaml, "vert", VerticalPosition, False
        )


class Haus:
    def __init__(self):
        self.geschosse = []
        self.book = dict()
        self.geschoss_count = 0
        self.room_count = 0
        self.kabel = []
        self.nodes = dict()

    def add_node(self, node):
        self.nodes[node.id] = node

    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)

    def find_object(self, cid):
        pos = cid.split(".")
        return (
            self.geschosse[int(pos[0]) - 1]
            .rooms[int(pos[1]) - 1]
            .objects[int(pos[2]) - 1]
        )


class Geschoss:
    def __init__(self, yaml, z, parent):
        self.id = read_value_from_yaml(yaml, "id")
        self.cid = self.id
        self.name = read_value_from_yaml(yaml, "name")
        # starthöhe des stockwerks
        self.z0 = z
        self.height = read_value_from_yaml(yaml, "height")
        self.z1 = self.z0 + self.height
        self.parent = parent
        self.rooms = []
        self.walls = []
        self.windows = []
        self.doors = []
        self.nodes = []
        self.book = dict()

    def add_node(self, node):
        if node in self.nodes:
            raise RuntimeError(" Node Already in List: {} ".format(node))
        self.nodes.append(node)
        self.parent.add_node(node)

    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)


class Room:
    def __init__(self, yaml, parent):
        self.id = read_value_from_yaml(yaml, "id")
        self.cid = str(parent.cid) + "." + str(self.id)
        self.name = read_value_from_yaml(yaml, "name")
        self.objects = []
        self.book = dict()
        self.parent = parent


class Point:
    def __init__(self, yaml, parent):
        self.id = read_value_from_yaml(yaml, "id")
        self.cid = str(parent.cid) + "." + str(self.id)
        self.pos = Position(yaml["pos"])
        self.parent = parent
        self.x = self.pos.horizontal[0]
        self.y = self.pos.horizontal[1]
        values = [30, 105, 200, 230]
        self.z = values[self.pos.vertical.value]


class Object(Point):
    def __init__(self, yaml, parent):
        super().__init__(yaml, parent)
        self.name = read_value_from_yaml(yaml, "name")
        self.connection_type = KabelType.NYM5x15
        self.associated_wall = None
        self.associated_node = None
        self.print_name = "Object"

    def draw(self, dwg):
        x = self.pos.horizontal[0] * 10
        y = self.pos.horizontal[1] * 10
        xe = 50
        ye = 50
        xs = x - xe * 0.5
        ys = y - ye * 0.5
        draw_obj = dwg.rect(
            (xs, ys), (xe, ye), style="cursor:crosshair", stroke="blue", fill="blue"
        )
        draw_obj["class"] = "object"
        dwg.add(draw_obj)

    def __str__(self):
        return "{}: {} ({},{},{}[{}] Name: {})".format(
            self.print_name,
            self.cid,
            self.x,
            self.y,
            self.z,
            self.pos.vertical,
            self.name,
        )


class Stromanschluss(Object):
    def __init__(self, yaml, parent):
        super().__init__(yaml, parent)
        self.anzahl = read_value_from_yaml(yaml, "anzahl")
        self.stromstaerke = 0
        self.voltage = 230
        self.knx = read_value_from_yaml_to_enum(yaml, "knx", KnxType, False)
        self.connection_type = read_value_from_yaml_to_enum(
            yaml, "kabelanschluss", KabelType, False
        )
        self.print_name = "Stromanschluss"


class Steckdose(Stromanschluss):
    def __init__(self, yaml, parent):
        super().__init__(yaml, parent)
        self.print_name = "Steckdose"


class Licht(Stromanschluss):
    def __init__(self, yaml, parent):
        super().__init__(yaml, parent)
        if self.knx != KnxType.Schaltbar:
            raise RuntimeError("Licht nicht schaltbar: {}".format(self.cid))
        self.color = "yellow"
        self.print_name = "Licht"

    def draw(self, dwg):
        x = self.pos.horizontal[0] * 10
        y = self.pos.horizontal[1] * 10
        line_width = 15
        r = 100
        xs = x
        ys = y
        draw_obj = dwg.circle(
            (xs, ys),
            r,
            style="cursor:crosshair",
            stroke=self.color,
            stroke_width=line_width,
            fill="none",
            id="licht_" + str(self.id),
        )
        draw_obj["class"] = "led"
        xes = x - r / sqrt(2)
        yes = y + r / sqrt(2)
        xss = x + r / sqrt(2)
        yss = y - r / sqrt(2)
        line1 = dwg.line(
            start=(xss, yss),
            end=(xes, yes),
            style="cursor:crosshair",
            stroke=self.color,
            stroke_width=line_width,
            fill=self.color,
        )
        yes = y - r / sqrt(2)
        yss = y + r / sqrt(2)
        line2 = dwg.line(
            start=(xss, yss),
            end=(xes, yes),
            style="cursor:crosshair",
            stroke=self.color,
            stroke_width=line_width,
            fill=self.color,
        )
        line1["class"] = "led"
        line2["class"] = "led"
        xes = x - r / sqrt(2)
        xes = x - r / sqrt(2)
        dwg.add(line1)
        dwg.add(line2)
        dwg.add(draw_obj)


class Led(Licht):
    def __init__(self, yaml, parent):
        super().__init__(yaml, parent)
        self.voltage = 24
        self.knx = KnxType.Dimmbar
        self.color = "orange"
        self.print_name = "Led"


class LedStrip(Led):
    def __init__(self, yaml, parent):
        super().__init__(yaml, parent)
        self.color = "purple"
        self.len = read_value_from_yaml(yaml, "len")

    def draw(self, dwg):
        x = self.pos.horizontal[0] * 10
        y = self.pos.horizontal[1] * 10
        line_width = 45
        xe = x + self.len[0] * 10
        ye = y + self.len[1] * 10
        line1 = dwg.line(
            start=(x, y),
            end=(xe, ye),
            style="cursor:crosshair",
            stroke=self.color,
            stroke_width=line_width,
            fill=self.color,
        )
        line1["class"] = "led"
        dwg.add(line1)
        len_strip = sqrt(self.len[0] ** 2 + self.len[1] ** 2)
        dx = self.len[1] * 100 / len_strip
        dy = self.len[0] * 100 / len_strip
        xs = x + dx
        ys = y + dy
        xe = x - dx
        ye = y - dy
        line2 = dwg.line(
            start=(xs, ys),
            end=(xe, ye),
            style="cursor:crosshair",
            stroke=self.color,
            stroke_width=line_width,
            fill=self.color,
        )
        line2["class"] = "led"
        dwg.add(line2)
        x += self.len[0] * 10
        y += self.len[1] * 10
        xs = x + dx
        ys = y + dy
        xe = x - dx
        ye = y - dy
        line3 = dwg.line(
            start=(xs, ys),
            end=(xe, ye),
            style="cursor:crosshair",
            stroke=self.color,
            stroke_width=line_width,
            fill=self.color,
        )
        line3["class"] = "led"
        dwg.add(line3)
        self.print_name = "LedStrip"


class Kontakt(Object):
    def __init__(self, yaml, parent):
        super().__init__(yaml, parent)
        self.anzahl = read_value_from_yaml(yaml, "anzahl")
        self.knx = read_value_from_yaml_to_enum(yaml, "knx", KnxType, False)
        self.connection_type = KabelType.FMK
        self.print_name = "Kontakt"

    def draw(self, dwg):
        xs = self.pos.horizontal[0] * 10
        ys = self.pos.horizontal[1] * 10
        xe = xs + 100
        ye = ys - 100
        draw_obj = dwg.line(
            start=(xs, ys),
            end=(xe, ye),
            style="cursor:crosshair",
            stroke="purple",
            stroke_width=30,
            fill="purple",
        )
        draw_obj["class"] = "kontakt"
        dwg.add(draw_obj)


class Knx(Object):
    def __init__(self, yaml, parent):
        super().__init__(yaml, parent)
        self.knx_anschluss = read_value_from_yaml_to_enum(
            yaml, "knx-component", KnxAnschluss
        )
        self.connection_type = KabelType.KNX
        self.print_name = "KNX"

    def draw(self, dwg):
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
            draw_obj = dwg.circle(
                (xs, ys), r, style="cursor:crosshair", stroke="green", fill="none"
            )
            draw_obj["class"] = "knx_pm_radius"
            dwg.add(draw_obj)
            r = 1500
            xs = x
            ys = y
            draw_obj = dwg.circle(
                (xs, ys), r, style="cursor:crosshair", stroke="green", fill="none"
            )
            draw_obj["class"] = "knx_pm_dist_licht"
            dwg.add(draw_obj)
            xe = 85
            ye = 85
            xs = x - xe * 0.5
            ys = y - ye * 0.5
            draw_obj = dwg.rect(
                (xs, ys),
                (xe, ye),
                style="cursor:crosshair",
                stroke="green",
                fill="green",
            )
            draw_obj["class"] = "knx"
        else:
            xe = xs + 100
            ye = ys + 100
            draw_obj = dwg.line(
                start=(xs, ys),
                end=(xe, ye),
                style="cursor:crosshair",
                stroke="green",
                stroke_width=30,
                fill="green",
            )
            draw_obj["class"] = "knx"
        dwg.add(draw_obj)


class Netzwerk(Object):
    def __init__(self, yaml, parent):
        super().__init__(yaml, parent)
        self.anzahl = read_value_from_yaml(yaml, "anzahl")
        self.connection_type = KabelType.CAT7
        self.print_name = "Netzwerk"

    def draw(self, dwg):
        xs = self.pos.horizontal[0] * 10
        ys = self.pos.horizontal[1] * 10
        xe = xs + 100
        ye = ys
        draw_obj = dwg.line(
            start=(xs, ys),
            end=(xe, ye),
            style="cursor:crosshair",
            stroke="red",
            stroke_width=30,
            fill="red",
        )
        draw_obj["class"] = "netzwerk"
        dwg.add(draw_obj)


class Wall(Point):
    def __init__(self, yaml, parent):
        self.dx = 0
        self.dy = 0
        super().__init__(yaml, parent)
        self.nodes = []
        st = "ende"
        if yaml != None and st in yaml:
            self.dx = float(eval(str(yaml[st][0])))
            self.dy = float(eval(str(yaml[st][1])))
        self.waagrecht = self.dx > self.dy

    def add_node(self, node, recursive=False):
        self.nodes.append(node)
        if recursive:
            self.parent.add_node(node)

    def add_nodes(self, nodes, recursive=False):
        for node in nodes:
            self.add_node(node, recursive)

    def __str__(self):
        return "Wall {}: {},{} to {},{}".format(
            self.cid, self.x, self.y, self.x + self.dy, self.y + self.dy
        )


class Window(Point):
    def __init__(self, yaml, parent):
        self.dx = 0
        self.dy = 0
        super().__init__(yaml, parent)
        self.x = self.pos.horizontal[0]
        self.y = self.pos.horizontal[1]
        st = "ende"
        if yaml != None and st in yaml:
            self.dx = float(eval(str(yaml[st][0])))
            self.dy = float(eval(str(yaml[st][1])))


class Door(Point):
    def __init__(self, yaml, parent):
        self.dx = 0
        self.dy = 0
        super().__init__(yaml, parent)
        self.x = self.pos.horizontal[0]
        self.y = self.pos.horizontal[1]
        st = "ende"
        if yaml != None and st in yaml:
            self.dx = float(eval(str(yaml[st][0])))


class NodeType(Enum):
    Unknown = 0
    StartBottom = 1
    EndBottom = 2
    StartTop = 3
    EndTop = 4
    Object = 5
    ObjectBottom = 6
    ObjectTop = 7

    def __str__(self):
        return str(self.name)


class Node:
    id_counter = 0

    def __init__(self, x, y, z, parent, node_type=NodeType.Unknown):
        self.x = x
        self.y = y
        self.z = z
        self.n = 1
        self.id = Node.id_counter
        Node.id_counter += 1
        self.parent = parent
        self.type = node_type
        # self.connections = []
        self.edges = []

    def __str__(self):
        return "Node {} Position: {} {} {}, N: {} T: {} P: {}".format(
            self.id, self.x, self.y, self.z, self.n, self.type, self.parent
        )

    def info(self):
        text = self.__str__()
        for node in self.get_connected_nodes():
            text += "\n --  connected to {} distance: {}".format(
                node, self.distance(node)
            )
        return text

    def is_node(self, node):
        if not isinstance(node, Node):
            raise RuntimeError("An Node must be passe to Node routine")

    def connect(self, node):
        self.is_node(node)
        e = Edge(self, node)
        self.n += 1
        node.n += 1
        self.edges.append(e)
        node.edges.append(e)

    def is_connected(self, node):
        self.is_node(node)
        return node in self.get_connected_nodes()

    def get_edge_that_connects_to(self, node):
        self.is_node(node)
        for e in self.edges:
            if e.get_con_node(self) == node:
                return e
        raise RuntimeError(
            "Node {}: is not connected to Node {}".format(self.id, node.id)
        )

    def distance(self, node):
        self.is_node(node)
        return self.get_edge_that_connects_to(node).length

    def get_connected_nodes(self):
        list_of_nodes = []
        for e in self.edges:
            list_of_nodes.append(e.get_con_node(self))
        return list_of_nodes

    def replace_connection(self, node_old, node_new):
        self.is_node(node_old)
        self.is_node(node_new)
        if self.is_connected(node_old):
            # find the edge that makes the connection:
            for e in self.edges:
                if e.get_con_node(self) == node_old:
                    node_old.edges.remove(e)
                    node_old.n -= 1
                    e.replace_node(node_old, node_new)
                    node_new.edges.append(e)
                    node_new.n += 1
                    return
        else:
            dntp = []
            for n in self.parent.associated_wall.nodes:
                if n.z == self.z:
                    dntp.append(n)

            if self.parent.associated_wall.waagrecht:
                dntp = sorted(dntp, key=lambda node: node.x * 10000 + node.id)
            else:
                dntp = sorted(dntp, key=lambda node: node.y * 10000 + node.id)

            for n in dntp:
                print(n.info())

            raise RuntimeError(
                "In Replace Conection of Node {}: Replacing Node {} with {} is not connected possible (not connected) \n {} \n {} \n {}".format(
                    self.id,
                    node_old.id,
                    node_new.id,
                    self.info(),
                    node_old.info(),
                    node_new.info(),
                )
            )


class Edge:
    id_counter = 0

    def __init__(self, node1, node2):
        self.node = [node1, node2]
        self.length = self.calc_length()
        self.id = Edge.id_counter
        Edge.id_counter += 1

    def __str__(self):
        return "Edge {} Connecting-Edges: {} {} len: {}".format(
            self.id, self.node[0], self.node[1], self.length
        )

    def calc_length(self):
        n1 = self.node[0]
        n2 = self.node[1]
        dx = n1.x - n2.x
        dy = n1.y - n2.y
        dz = n1.z - n2.z
        self.length =  sqrt(dx * dx + dy * dy + dz * dz)
        return self.length

    def get_con_node(self, node):
        if self.node[0].id == node.id:
            return self.node[1]
        return self.node[0]

    def replace_node(self, node_old, node_new):
        if self.node[0].id == node_old.id:
            self.node[0] = node_new
        elif self.node[1].id == node_old.id:
            self.node[1] = node_new
        self.calc_length()


class Kabel:
    def __init__(self, start, end):
        self.is_obj(start)
        self.start = start
        if type(end) is list:
            for o in end:
                self.is_obj(o)
            self.end = end
        else:
            self.is_obj(end)
            self.end = [end]

        self.type = None
        self.length = 0.0

    def is_obj(self, obj):
        pass
        # if not isinstance(obj,Object):
        #     raise RuntimeError("An Object must be passe to Kabel")

    @classmethod
    def from_yaml(cls, yaml):
        start = read_value_from_yaml(yaml, "start")
        end = read_value_from_yaml(yaml, "end")
        return cls(start, end)
        # print(" Kabel from {} to {}: {}".format(self.start,len(self.end),self.end))

    def __str__(self):
        return "Kabel from {} to {}".format(self.start, self.end[0])
