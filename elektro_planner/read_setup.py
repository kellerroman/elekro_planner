#!/usr/bin/env python3

from elektro_planner.data import  *
from elektro_planner.read_anschluesse import read_anschluesse
from elektro_planner.read_struktur import read_struktur
from elektro_planner.read_kabel import read_kabel, autogenerate_kabel
from elektro_planner.connect_walls import create_nodes_from_walls
import yaml
import os

def read_setup(yaml_file):
    with open(yaml_file, 'r') as stream:
        data = yaml.safe_load(stream)
    # print("Reading Setup for {}".format(data["config"]["name"]))

    folder = os.path.dirname(os.path.abspath(yaml_file))+ "/"
    file_anschluesse = folder + data["config"]["anschluesse"]
    file_struktur = folder + data["config"]["struktur"]
    file_kabel = folder + data["config"]["kabel"]
    if not os.path.isfile(file_struktur):
        raise RuntimeError("File not found: {}".format(file_struktur))
    if not os.path.isfile(file_anschluesse):
        raise RuntimeError("File not found: {}".format(file_anschluesse))
    if not os.path.isfile(file_kabel):
        raise RuntimeError("File not found: {}".format(file_kabel))
    haus = Haus()

    # Read YAML filess
    with open(file_struktur, 'r') as stream:
        yaml_struktur = yaml.safe_load(stream)
    with open(file_anschluesse, 'r') as stream:
        yaml_anschluesse = yaml.safe_load(stream)
    with open(file_kabel, 'r') as stream:
        yaml_kabel = yaml.safe_load(stream)

    read_struktur(haus,yaml_struktur)
    read_anschluesse(haus,yaml_anschluesse)
    read_kabel(haus,yaml_kabel)
    autogenerate_kabel(haus)

    create_nodes_from_walls(haus)

    return haus
if __name__ == '__main__':
    yaml_file = "data/setup.yaml"
    haus = read_setup(yaml_file)
