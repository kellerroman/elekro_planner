#!/usr/bin/env python3

import svgwrite
from read_setup import *
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
        dwg = svgwrite.Drawing(output_file, (WIDTH, HEIGHT), id="svg_eg")
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
            rect = dwg.rect((xs,ys), (xe,ye), style="cursor:crosshair", stroke="black", fill="black", id="wall_"+text)
            rect['class'] = 'wall'
            dwg.add(rect)
        for window in geschoss.windows:
            xs = window.x * 10
            ys = window.y * 10
            xe = window.dx * 10
            ye = window.dy * 10
            text = str(window.id)
            rect = dwg.rect((xs,ys), (xe,ye), style="cursor:crosshair", stroke="blue", stroke_width=10, fill="white", id="window_"+text)
            rect['class'] = 'window'
            dwg.add(rect)
        for door in geschoss.doors:
            xs = door.x * 10
            ys = door.y * 10
            xe = door.dx * 10
            ye = door.dy * 10
            text = str(door.id)
            rect = dwg.rect((xs,ys), (xe,ye), style="cursor:crosshair", stroke="brown", stroke_width=10, fill="white", id="door_"+text)
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

        for room in geschoss.rooms:
            for obj in room.objects:
                if obj.pos.horizontal != [0,0]:

                    x = obj.pos.horizontal[0] * 10
                    y = obj.pos.horizontal[1] * 10
                    xs = x
                    ys = y
                    if type(obj) is Licht:
                        line_width = 15
                        r = 100
                        xs = x
                        ys = y
                        draw_obj = dwg.circle((xs,ys), r, style="cursor:crosshair", stroke="yellow", stroke_width=line_width , fill="none")
                        draw_obj['class'] = 'licht'
                        xes = x - r / sqrt(2)
                        yes = y + r / sqrt(2)
                        xss = x + r / sqrt(2)
                        yss = y - r / sqrt(2)
                        line1 = dwg.line(start=(xss,yss), end=(xes,yes), style="cursor:crosshair", stroke="yellow", stroke_width = line_width, fill="yellow")
                        yes = y - r / sqrt(2)
                        yss = y + r / sqrt(2)
                        line2 = dwg.line(start=(xss,yss), end=(xes,yes), style="cursor:crosshair", stroke="yellow", stroke_width = line_width, fill="yellow")
                        dwg.add(line1)
                        dwg.add(line2)
                    elif type(obj) is Knx:
                        xe = 50
                        ye = 50
                        if obj.knx_anschluss is KnxAnschluss.Praesenzmelder:
                            r = 5000
                            xs = x
                            ys = y
                            draw_obj = dwg.circle((xs,ys), r, style="cursor:crosshair", stroke="green", fill="none")
                            draw_obj['class'] = 'pm_radius'
                            dwg.add(draw_obj)
                            r = 1500
                            xs = x
                            ys = y
                            draw_obj = dwg.circle((xs,ys), r, style="cursor:crosshair", stroke="green", fill="none")
                            draw_obj['class'] = 'pm_dist_licht'
                            dwg.add(draw_obj)
                            xe = 85
                            ye = 85
                            xs = x - xe * 0.5
                            ys = y - ye * 0.5
                            draw_obj = dwg.rect((xs,ys), (xe,ye), style="cursor:crosshair", stroke="green", fill="green")
                        else:
                            xe = xs + 100
                            ye = ys + 100
                            draw_obj = dwg.line(start=(xs,ys), end=(xe,ye), style="cursor:crosshair", stroke="green", stroke_width = 30, fill="green")
                        draw_obj['class'] = 'knx'
                    elif type(obj) is Netzwerk:
                        xe = xs + 100
                        ye = ys
                        draw_obj = dwg.line(start=(xs,ys), end=(xe,ye), style="cursor:crosshair", stroke="red", stroke_width = 30, fill="red")
                        draw_obj['class'] = 'netzwerk'
                    elif type(obj) is Kontakt:
                        xe = xs + 100
                        ye = ys - 100
                        draw_obj = dwg.line(start=(xs,ys), end=(xe,ye), style="cursor:crosshair", stroke="purple", stroke_width = 30, fill="purple")
                        draw_obj['class'] = 'kontakt'
                    else:
                        xe = 50
                        ye = 50
                        xs = x - xe * 0.5
                        ys = y - ye * 0.5
                        draw_obj = dwg.rect((xs,ys), (xe,ye), style="cursor:crosshair", stroke="blue", fill="blue")
                        draw_obj['class'] = 'object'
                    dwg.add(draw_obj)

        dwg.viewbox( minx   = 0, miny   = 0, width  = WIDTH, height = HEIGHT)
        dwg.save()
        svgs.append(dwg.tostring())
    return svgs
if __name__ == '__main__':
    yaml_file = "data/setup.yaml"
    print(len(create_svg(read_setup(yaml_file))))
