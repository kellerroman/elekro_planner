#!/usr/bin/env python3

# Create simple SVG
import svgwrite
from read_objecte import read_objects, Haus
from read_walls import read_walls

output_file      = "simple.svg"
WIDTH, HEIGHT = 1900, 900
BORDER = 5

haus = Haus()
yaml_file = "data/eg.yaml"
read_walls(haus,yaml_file)

dwg = svgwrite.Drawing(output_file, (WIDTH, HEIGHT))
dwg.add(dwg.rect((0,0), (WIDTH-1,HEIGHT-1),
                 stroke="red",
                 fill="none"))

max_val_x = 0
min_val_x = WIDTH
max_val_y = 0
min_val_y = HEIGHT
for geschoss in haus.geschosse:
    for wall in geschoss.walls:
        max_val_x = max(wall.x,wall.x+wall.dx,max_val_x)
        max_val_y = max(wall.y,wall.y+wall.dy,max_val_y)
        min_val_x = min(wall.x,wall.x+wall.dx,min_val_x)
        min_val_y = min(wall.y,wall.y+wall.dy,min_val_y)

# print (WIDTH,HEIGHT)
# print (min_val_x, max_val_x, min_val_y, max_val_y)

max_val_x = (WIDTH-2* BORDER ) / (max_val_x-min_val_x)
max_val_y = (HEIGHT-2* BORDER ) / (max_val_y-min_val_y)

# max_val_x,max_val_y,min_val_x,min_val_y,BORDER = 1,1,0,0,0
SCRIPT = """
var min_val_x = {};
var max_val_x = {};
var min_val_y = {};
var max_val_y = {};
var border = {};
function copy() {{
    var myline = document.getElementById("pos_test");
    if (myline){{
       myline.select();
       var result = document.execCommand('copy');
    }}
 }}

const round = (number, decimalPlaces) => {{
  const factorOfTen = Math.pow(10, decimalPlaces)
  return Math.round(number * factorOfTen) / factorOfTen
}}
window.onmousedown = function(e)
{{
    var myline = document.getElementById("pos_test");
    if (myline){{
        var x = round((e.layerX - border ) / max_val_x + min_val_x,2);
        var y = round((e.layerY - border ) / max_val_y + min_val_y,2);
        myline.textContent =  "        hori: ["+ x+","+y+"]";
        console.log(myline.textContent);
    }}
}}
"""
dwg.add(dwg.text("0,0" , insert=(int(WIDTH*0.9),20 ), fill='red', id="pos_test"))
for geschoss in haus.geschosse:
  for wall in geschoss.walls:
    xs = int((wall.x - min_val_x ) * max_val_x + BORDER)
    ys = int((wall.y - min_val_y ) * max_val_y + BORDER)
    xe = int((wall.dx ) * max_val_x)
    ye = int((wall.dy ) * max_val_y)
    text = str(wall.id)
    # print(xs,ys,xe,ye,text)
    # dwg.add(dwg.rect((xs,ys), (xe,ye), style="cursor:wait;", stroke="black", fill="white", id="wall_"+text))
    dwg.add(dwg.rect((xs,ys), (xe,ye), style="cursor:crosshair", stroke="black", fill="black", id="wall_"+text))
    # dwg.add(dwg.text(text , insert=(xs+0.5*xe, ys+0.5*ye), fill='red', id="wall_test_"+text))


yaml_file = "data/anschluesse.yaml"
read_objects(haus,yaml_file)
for geschoss in haus.geschosse:
    for room in geschoss.rooms:
        for obj in room.objects:
            if obj.pos.horizontal != [0,0]:
              x = obj.pos.horizontal[0]
              y = obj.pos.horizontal[1]
              xs = int((x - min_val_x ) * max_val_x + BORDER)
              ys = int((y - min_val_y ) * max_val_y + BORDER)
              xe = 5;
              ye = 5;
              dwg.add(dwg.rect((xs,ys), (xe,ye), style="cursor:crosshair", stroke="blue", fill="blue"))


dwg.defs.add(dwg.script(content=SCRIPT.format(min_val_x,max_val_x,min_val_y, max_val_y, BORDER)))
dwg.save()
