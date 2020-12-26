#!/usr/bin/env python3

# Create simple SVG
import svgwrite
from read_setup import *

def create_svg(haus):
    output_file      = "simple.svg"
    WIDTH, HEIGHT = 1900, 900
    BORDER = 5

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

    WIDTH = max_val_x * 10
    HEIGHT = max_val_y * 10
    dwg = svgwrite.Drawing(output_file, (WIDTH, HEIGHT), id="svg_eg")
    dwg.add(dwg.rect((0,0), (WIDTH-1,HEIGHT-1),
                    stroke="red",
                    fill="none"))
    for geschoss in haus.geschosse:
        for wall in geschoss.walls:
            xs = wall.x * 10
            ys = wall.y * 10
            xe = wall.dx * 10
            ye = wall.dy * 10
            text = str(wall.id)
            # dwg.add(dwg.rect((xs,ys), (xe,ye), style="cursor:wait;", stroke="black", fill="white", id="wall_"+text))
            rect = dwg.rect((xs,ys), (xe,ye), style="cursor:crosshair", stroke="black", fill="black", id="wall_"+text)
            rect['class'] = 'wall'
            dwg.add(rect)
            # dwg.add(dwg.text(text , insert=(xs+0.5*xe, ys+0.5*ye), fill='red', id="wall_test_"+text))
        for window in geschoss.windows:
            xs = window.x * 10
            ys = window.y * 10
            xe = window.dx * 10
            ye = window.dy * 10
            text = str(window.id)
            rect = dwg.rect((xs,ys), (xe,ye), style="cursor:crosshair", stroke="blue", fill="white", id="window_"+text)
            rect['class'] = 'window'
            dwg.add(rect)
        for door in geschoss.doors:
            xs = door.x * 10
            ys = door.y * 10
            xe = door.dx * 10
            ye = door.dy * 10
            text = str(door.id)
            rect = dwg.rect((xs,ys), (xe,ye), style="cursor:crosshair", stroke="brown", fill="white", id="door_"+text)
            rect['class'] = 'door'
            dwg.add(rect)

    for geschoss in haus.geschosse:
        for room in geschoss.rooms:
            for obj in room.objects:
                if obj.pos.horizontal != [0,0]:

                    x = obj.pos.horizontal[0] * 10
                    y = obj.pos.horizontal[1] * 10
                    xs = x
                    ys = y
                    if type(obj) is Licht:
                        r = 100;
                        xs = x
                        ys = y
                        draw_obj = dwg.circle((xs,ys), r, style="cursor:crosshair", stroke="yellow", fill="yellow")
                        draw_obj['class'] = 'licht'
                    elif type(obj) is Knx:
                        r = 5000;
                        xs = x
                        ys = y
                        draw_obj = dwg.circle((xs,ys), r, style="cursor:crosshair", stroke="green", fill="none")
                        draw_obj['class'] = 'pm_radius'
                        dwg.add(draw_obj)
                        xe = 85;
                        ye = 85;
                        xs = x - xe * 0.5
                        ys = y - ye * 0.5
                        draw_obj = dwg.rect((xs,ys), (xe,ye), style="cursor:crosshair", stroke="green", fill="green")
                        draw_obj['class'] = 'knx'
                    else:
                        xe = 50;
                        ye = 50;
                        draw_obj = dwg.rect((xs,ys), (xe,ye), style="cursor:crosshair", stroke="blue", fill="blue")
                        draw_obj['class'] = 'object'
                    dwg.add(draw_obj)

    dwg.viewbox(
      minx   = 0,
      miny   = 0,
      width  = WIDTH,
      height = HEIGHT
    )
    dwg.save()
    return dwg.tostring()
if __name__ == '__main__':
    yaml_file = "data/setup.yaml"
    print(create_svg(read_setup(yaml_file)))
