from pdf_annotate import PdfAnnotator, Location, Appearance
from elektro_planner.read_setup import read_setup
from elektro_planner.data import KnxType, KnxAnschluss

pdf_dim = [
    [42000, 42000, 7040, 24355, 21010, 35850],
    [42000, 42000, 7040, 24355, 13055, 29670],
    [42000, 42000, 7040, 24355, 8180, 32330],
]
dim_geschoss = [
    [1447.5 - 2 * 18, 1049],
    [1447.5 - 2 * 18, 1209 - 17 - 18],
    [1447.5 - 2 * 18, 883 + 292.5 + 31.5],
]
file_name = ["UG", "EG", "DG"]
yaml_file = "data/setup.yaml"
haus = read_setup(yaml_file)
for i in range(2, 3):
    geschoss = haus.geschosse[i]
    file_name_file = "{}.pdf".format(file_name[i])
    file_name_full = "data/plaene/{}".format(file_name_file)
    print("Reading:{} and storing to:{}".format(file_name_full, file_name_file))
    a = PdfAnnotator(file_name_full)
    a.set_page_dimensions((pdf_dim[i][0], pdf_dim[i][1]), 0)
    pos_x1 = pdf_dim[i][2]
    pos_x2 = pdf_dim[i][3]
    pos_y1 = pdf_dim[i][4]
    pos_y2 = pdf_dim[i][5]
    for wall in geschoss.walls:

        x = (wall.x) / (dim_geschoss[i][0]) * (pos_x2 - pos_x1) + pos_x1
        y = (wall.y) / (dim_geschoss[i][1]) * (pos_y1 - pos_y2) + pos_y2
        x2 = (wall.x + wall.dx) / (dim_geschoss[i][0]) * (pos_x2 - pos_x1) + pos_x1
        y2 = (wall.y + wall.dy) / (dim_geschoss[i][1]) * (pos_y1 - pos_y2) + pos_y2
        a.add_annotation(
            "square",
            Location(x1=x, y1=y, x2=x2, y2=y2, page=0),
            Appearance(stroke_color=(0, 0, 0), stroke_width=2),
        )
    for room in geschoss.rooms:
        for obj in room.objects:

            x = (obj.x) / (dim_geschoss[i][0]) * (pos_x2 - pos_x1) + pos_x1
            y = (obj.y) / (dim_geschoss[i][1]) * (pos_y1 - pos_y2) + pos_y2
            r = 100
            color = (0, 1, 1)
            if obj.print_name in ["Steckdose"]:
                pic_file = "steckdose_{}.png".format(obj.anzahl)
            elif obj.print_name in ["Stromanschluss"]:
                pic_file = "stromanschluss.png"
                if obj.knx == KnxType.Rolladen:
                    pic_file = "rolladen.png"
            elif obj.print_name == "KNX":
                pic_file = "taster.png"
                if obj.knx_anschluss == KnxAnschluss.Praesenzmelder:
                    pic_file = "prm.png"
            elif obj.print_name in ["Licht", "Led", "LedStrip"]:
                pic_file = "licht.png"
            elif obj.print_name == "Kontakt":
                pic_file = "kontakt.png"
            elif obj.print_name == "Netzwerk":
                pic_file = "netzwerk.png"
            else:
                raise RuntimeError("Unknown Type of Object {}".format(obj.print_name))
            a.add_annotation(
                "image",
                Location(x1=x - 150, y1=y - 150, x2=(x + 150), y2=y + 150, page=0),
                Appearance(image="data/plaene/schaltsymbole/{}".format(pic_file)),
            )
            # a.add_annotation(
            #     "circle",
            #     Location(x1=x - r, y1=y - r, x2=x + r, y2=y + r, page=0),
            #     Appearance(stroke_color=color, stroke_width=1),
            # )
            # a.add_annotation(
            #     "line",
            #     Location(points=[[x - r, y - r], [x + r, y + r]], page=0),
            #     Appearance(stroke_color=color, stroke_width=1),
            # )
    a.write(file_name_file)  # or use overwrite=True if you feel lucky
