#!/usr/bin/env python3

from data import  *
from read_anschluesse import read_anschluesse
from read_struktur import read_struktur
import yaml
import os

def read_setup(yaml_file):
    with open(yaml_file, 'r') as stream:
        data = yaml.safe_load(stream)
    # print("Reading Setup for {}".format(data["config"]["name"]))

    folder = os.path.dirname(os.path.abspath(yaml_file))+ "/"
    yaml_anschluesse = folder + data["config"]["anschluesse"]
    yaml_struktur = folder + data["config"]["struktur"]
    if not os.path.isfile(yaml_struktur):
        raise RuntimeError("File not found: {}".format(yaml_struktur))
    if not os.path.isfile(yaml_anschluesse):
        raise RuntimeError("File not found: {}".format(yaml_anschluesse))
    haus = Haus()

    read_struktur(haus,yaml_struktur)
    read_anschluesse(haus,yaml_anschluesse)


    return haus
if __name__ == '__main__':
    yaml_file = "data/setup.yaml"
    haus = read_setup(yaml_file)
