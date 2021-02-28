#!/usr/bin/env python3
import svgwrite
from math import sqrt

def create_svg(haus):
    svgs = []
    for geschoss in haus.geschosse:
        output_file      = geschoss.name+".svg"
        WIDTH, HEIGHT = 1900, 900
        BORDER = 5

        max_val_x = 0
        min_val_x = WIDTH
        max_val_y = 0
        min_val_y = HEIGHT
        for wall in geschoss.walls:
            max_val_x = max(wall.x,wall.x+wall.dx,max_val_x)
            max_val_y = max(wall.y,wall.y+wall.dy,max_val_y)
            min_val_x = min(wall.x,wall.x+wall.dx,min_val_x)
            min_val_y = min(wall.y,wall.y+wall.dy,min_val_y)

        WIDTH = max_val_x * 10
        HEIGHT = max_val_y * 10
        dwg = svgwrite.Drawing(output_file, (WIDTH, HEIGHT),
                id="svg_"+geschoss.name)
        dwg.add(dwg.rect((0,0), (WIDTH-1,HEIGHT-1),
                    stroke="red",
                    fill="none"))
        for wall in geschoss.walls:
            xs = wall.x * 10
            ys = wall.y * 10
            xe = wall.dx * 10
            ye = wall.dy * 10
            text = str(wall.id)
            # rect = dwg.rect((xs,ys), (xe,ye), style="cursor:crosshair", stroke="black", fill="none", id="wall_"+text)
            rect = dwg.rect((xs,ys), (xe,ye), stroke="black", fill="black", id="wall_"+text)
            rect['class'] = 'wall'
            dwg.add(rect)
        for window in geschoss.windows:
            xs = window.x * 10
            ys = window.y * 10
            xe = window.dx * 10
            ye = window.dy * 10
            text = str(window.id)
            rect = dwg.rect((xs,ys), (xe,ye), stroke="blue", stroke_width=10, fill="white", id="window_"+text)
            rect['class'] = 'window'
            dwg.add(rect)
        for door in geschoss.doors:
            xs = door.x * 10
            ys = door.y * 10
            xe = door.dx * 10
            ye = door.dy * 10
            text = str(door.id)
            rect = dwg.rect((xs,ys), (xe,ye), stroke="brown", stroke_width=10, fill="white", id="door_"+text)
            rect['class'] = 'door'
            dwg.add(rect)
        # draw wall ids
        for wall in geschoss.walls:
            font_size = 150
            xs = wall.x * 10
            ys = wall.y * 10
            xe = wall.dx * 10
            ye = wall.dy * 10
            text = str(wall.id)
            text_style = "font-size:%ipx; font-family:%s" % (font_size, "Courier New")
            dwg.add(dwg.text(text, insert=(xs+0.5*(xe-font_size), ys+0.5*(ye+font_size)), fill='red', id="wall_test_"+text, style=text_style))

        for node in geschoss.nodes:
            for con in node.get_connected_nodes():
                xs = node.x*10
                ys = node.y*10
                xe = con.x*10
                ye = con.y*10
                draw_obj = dwg.line(start=(xs,ys), end=(xe,ye), stroke="green", stroke_width = 30, fill="green")
                dwg.add(draw_obj)
            r = 25
            line_width = 15
            color = "green"
            if node.n == 1:
                r = 75
            elif node.n == 2:
                color = "red"
            elif node.n == 3:
                color = "blue"
            elif node.n == 4:
                color = "yellow"
            elif node.n == 5:
                color = "white"
            elif node.n == 6:
                color = "magenta"
            # print(node.n)
            draw_obj = dwg.circle((node.x*10,node.y*10), r, stroke=color, stroke_width=line_width , fill=color)
            dwg.add(draw_obj)

        for room in geschoss.rooms:
            for obj in room.objects:
                if obj.pos.horizontal != [0,0]:
                    obj.draw(dwg)

        dwg.viewbox( minx   = 0, miny   = 0, width  = WIDTH, height = HEIGHT)
        dwg.save()
        svgs.append(dwg.tostring())
    return svgs
if __name__ == '__main__':
    yaml_file = "data/setup.yaml"
    from read_setup import *
    print(len(create_svg(read_setup(yaml_file))))
