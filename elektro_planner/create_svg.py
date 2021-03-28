#!/usr/bin/env python3
import svgwrite
from math import sqrt
from elektro_planner.data import NodeType, Knx, Netzwerk


def create_svg(haus):
    svgs = []
    for geschoss in haus.geschosse:
        output_file = geschoss.name + ".svg"
        WIDTH, HEIGHT = 1900, 900
        BORDER = 5

        max_val_x = 0
        min_val_x = WIDTH
        max_val_y = 0
        min_val_y = HEIGHT
        for wall in geschoss.walls:
            max_val_x = max(wall.x, wall.x + wall.dx, max_val_x)
            max_val_y = max(wall.y, wall.y + wall.dy, max_val_y)
            min_val_x = min(wall.x, wall.x + wall.dx, min_val_x)
            min_val_y = min(wall.y, wall.y + wall.dy, min_val_y)

        WIDTH = max_val_x * 10
        HEIGHT = max_val_y * 10
        dwg = svgwrite.Drawing(output_file, (WIDTH, HEIGHT), id="svg_" + geschoss.name)
        dwg.add(dwg.rect((0, 0), (WIDTH - 1, HEIGHT - 1), stroke="red", fill="none"))
        for wall in geschoss.walls:
            xs = wall.x * 10
            ys = wall.y * 10
            xe = wall.dx * 10
            ye = wall.dy * 10
            text = str(wall.id)
            # rect = dwg.rect((xs,ys), (xe,ye), style="cursor:crosshair", stroke="black", fill="none", id="wall_"+text)
            rect = dwg.rect(
                (xs, ys), (xe, ye), stroke="black", fill="black", id="wall_" + text
            )
            rect["class"] = "wall"
            dwg.add(rect)
        for window in geschoss.windows:
            xs = window.x * 10
            ys = window.y * 10
            xe = window.dx * 10
            ye = window.dy * 10
            text = str(window.id)
            rect = dwg.rect(
                (xs, ys),
                (xe, ye),
                stroke="blue",
                stroke_width=10,
                fill="white",
                id="window_" + text,
            )
            rect["class"] = "window"
            dwg.add(rect)
        for door in geschoss.doors:
            xs = door.x * 10
            ys = door.y * 10
            xe = door.dx * 10
            ye = door.dy * 10
            text = str(door.id)
            rect = dwg.rect(
                (xs, ys),
                (xe, ye),
                stroke="brown",
                stroke_width=10,
                fill="white",
                id="door_" + text,
            )
            rect["class"] = "door"
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
            draw_obj = dwg.text(
                text,
                insert=(xs + 0.5 * (xe - font_size), ys + 0.5 * (ye + font_size)),
                fill="red",
                id="wall_test_" + text,
                style=text_style,
            )
            draw_obj["class"] = "wall_ids"
            dwg.add(draw_obj)

        edges_drawn = []
        for node in geschoss.nodes:
            for con in node.get_connected_nodes():
                edge = node.get_edge_that_connects_to(con)
                if edge in edges_drawn:
                    continue
                edges_drawn.append(edge)
                xs = node.x * 10
                ys = node.y * 10
                xe = con.x * 10
                ye = con.y * 10
                draw_obj = dwg.line(
                    start=(xs, ys),
                    end=(xe, ye),
                    stroke="green",
                    stroke_width=30,
                    fill="green",
                    id="edge_" + str(con.id),
                )
                draw_obj["class"] = "edge"
                dwg.add(draw_obj)
                if sqrt((xs - xe) ** 2 + (ys - ye) ** 2) > 1000:
                    dy = +100
                    if node.type in [
                        NodeType.StartBottom,
                        NodeType.EndBottom,
                        NodeType.ObjectBottom,
                    ]:
                        dy = -100
                    text = len(con.kabel)
                    text_style = "font-size:%ipx; font-family:%s" % (
                        font_size,
                        "Courier New",
                    )
                    draw_obj = dwg.text(
                        text,
                        insert=(
                            0.5 * (xs + xe) - font_size,
                            0.5 * (ys + ye) - dy,
                        ),
                        fill="green",
                        id="edge_text_" + str(con.id),
                        style=text_style,
                    )
                    draw_obj["class"] = "edge edge_number"
                    dwg.add(draw_obj)
                elif node.type == NodeType.Connector:
                    text = len(edge.kabel)
                    text_style = "font-size:%ipx; font-family:%s" % (
                        font_size,
                        "Courier New",
                    )
                    draw_obj = dwg.text(
                        text,
                        insert=(
                            xs,
                            ys,
                        ),
                        fill="red",
                        id="edge_text_" + str(con.id),
                        style=text_style,
                    )
                    draw_obj["class"] = "edge edge_number"
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
            draw_obj = dwg.circle(
                (node.x * 10, node.y * 10),
                r,
                stroke=color,
                stroke_width=line_width,
                fill=color,
            )
            draw_obj["class"] = "node"
            dwg.add(draw_obj)

            text = str(len(node.kabel))
            text_style = "font-size:%ipx; font-family:%s" % (font_size, "Courier New")
            if node.type in [NodeType.StartBottom, NodeType.EndBottom]:
                color = "red"
                dx = 200
                dy = 200
            elif node.type in [NodeType.StartTop, NodeType.EndTop]:
                color = "green"
                dx = 200
                dy = -200
            elif node.type in [NodeType.ObjectBottom]:
                color = "magenta"
                dx = -200
                dy = 200
            elif node.type in [NodeType.ObjectTop]:
                color = "brown"
                dx = -200
                dy = -200
            elif node.type == NodeType.Connector:
                color = "yellow"
                dx = 0
                dy = -200
            else:
                color = "blue"
                dx = 0
                dy = 400
            draw_obj = dwg.text(
                text,
                insert=(node.x * 10 + dx, node.y * 10 + dy),
                fill=color,
                id="node_text_" + str(node.id),
                style=text_style,
            )
            draw_obj["class"] = "node_text"
            dwg.add(draw_obj)

        kabel_drawn = []
        for room in geschoss.rooms:
            for obj in room.objects:
                if obj.pos.horizontal != [0, 0]:
                    obj.draw(dwg)
                    k = obj.getKabel()
                    # if type(obj) != Knx:
                    #     continue
                    if k != None:
                        if k in kabel_drawn:
                            continue
                        kabel_drawn.append(k)
                        # raise RuntimeError("test {} {}".format(k, obj))
                        for e in range(len(k.path) - 1):
                            n1 = k.path[e]
                            n2 = k.path[e + 1]
                            xs = n1.x * 10
                            ys = n1.y * 10
                            xe = n2.x * 10
                            ye = n2.y * 10
                            draw_obj = dwg.line(
                                start=(xs, ys),
                                end=(xe, ye),
                                stroke="red",
                                stroke_width=30,
                                fill="red",
                            )
                            draw_obj["class"] = "kabel kabel_for_obj_" + str(
                                obj.cid
                            ).replace(".", "_")
                            dwg.add(draw_obj)

        dwg.viewbox(minx=0, miny=0, width=WIDTH, height=HEIGHT)
        dwg.save()
        svgs.append(dwg.tostring())
    return svgs


if __name__ == "__main__":
    yaml_file = "data/setup.yaml"
    from read_setup import *

    print(len(create_svg(read_setup(yaml_file))))
