def define_testcase():
    yaml = dict()
    yaml["struktur"] = {
        "geschosse": [
            {
                "id": 1,
                "name": "G1",
                "height": 200,
                "walls": [
                    {"id": 1, "pos": {"hori": [0, 0]}, "ende": [20, 300]},
                    {"id": 2, "pos": {"hori": [0, 0]}, "ende": [500, 20]},
                ],
            },
            {
                "id": 2,
                "name": "G2",
                "height": 300,
                "walls": [
                    {"id": 1, "pos": {"hori": [0, 0]}, "ende": [20, 300]},
                    {"id": 2, "pos": {"hori": [0, 0]}, "ende": [400, 20]},
                    {"id": 3, "pos": {"hori": [380, 20]}, "ende": [150, 20]},
                    {"id": 4, "pos": {"hori": [100, 0]}, "ende": [20, 150]},
                ],
            },
        ]
    }
    yaml["anschluesse"] = {
        "geschosse": [
            {
                "id": 1,
                "name": "G1",
                "rooms": [
                    {
                        "id": 1,
                        "name": "R11",
                        "objects": [
                            {
                                "id": 1,
                                "name": "O111",
                                "con-type": "steckdose",
                                "anzahl": 1,
                                "pos": {"hori": [50, 10], "vert": "oben"},
                            },
                            {
                                "id": 2,
                                "name": "O112",
                                "con-type": "steckdose",
                                "anzahl": 2,
                                "pos": {"hori": [10, 250], "vert": "oben"},
                            },
                            {
                                "id": 3,
                                "name": "O113",
                                "con-type": "steckdose",
                                "anzahl": 3,
                                "pos": {"hori": [350, 10], "vert": "oben"},
                            },
                        ],
                    }
                ],
            },
            {
                "id": 2,
                "name": "G2",
                "rooms": [
                    {
                        "id": 1,
                        "name": "R21",
                        "objects": [
                            {
                                "id": 1,
                                "name": "O211",
                                "con-type": "steckdose",
                                "anzahl": 1,
                                "pos": {"hori": [50, 10], "vert": "oben"},
                            },
                            {
                                "id": 2,
                                "name": "O212",
                                "con-type": "steckdose",
                                "anzahl": 2,
                                "pos": {"hori": [10, 250], "vert": "oben"},
                            },
                        ],
                    },
                    {
                        "id": 2,
                        "name": "R22",
                        "objects": [
                            {
                                "id": 1,
                                "name": "O221",
                                "con-type": "steckdose",
                                "anzahl": 1,
                                "pos": {"hori": [350, 10], "vert": "oben"},
                            },
                            {
                                "id": 2,
                                "name": "O222",
                                "con-type": "steckdose",
                                "anzahl": 2,
                                "pos": {"hori": [110, 100], "vert": "oben"},
                            },
                            {
                                "id": 3,
                                "name": "O223",
                                "con-type": "steckdose",
                                "anzahl": 3,
                                "pos": {"hori": [450, 30], "vert": "oben"},
                            },
                            {
                                "id": 4,
                                "name": "O224",
                                "con-type": "steckdose",
                                "anzahl": 3,
                                "pos": {"hori": [470, 30], "vert": "oben"},
                            },
                            {
                                "id": 5,
                                "name": "O225",
                                "con-type": "steckdose",
                                "anzahl": 3,
                                "pos": {"hori": [490, 30], "vert": "oben"},
                            },
                        ],
                    },
                ],
            },
        ]
    }
    yaml["kabel"] = {
        "kabel": [
            {
                "id": 1,
                "name": "SK1 R22",
                "start": "1.1.1",
                "end": ["2.2.3", "2.2.4", "2.2.5"],
            }
        ]
    }
    return yaml


def define_testcase_simple1():
    yaml = dict()
    yaml["struktur"] = {
        "geschosse": [
            {
                "id": 1,
                "name": "G1",
                "height": 200,
                "walls": [
                    {"id": 1, "pos": {"hori": [0, 0]}, "ende": [20, 300]},
                    {"id": 2, "pos": {"hori": [0, 0]}, "ende": [500, 20]},
                ],
            }
        ]
    }
    yaml["anschluesse"] = {
        "geschosse": [
            {
                "id": 1,
                "name": "G1",
                "rooms": [
                    {
                        "id": 1,
                        "name": "R11",
                        "objects": [
                            {
                                "id": 1,
                                "name": "O111",
                                "con-type": "steckdose",
                                "anzahl": 1,
                                "pos": {"hori": [50, 20], "vert": "unten"},
                            },
                            {
                                "id": 2,
                                "name": "O112",
                                "con-type": "steckdose",
                                "anzahl": 2,
                                "pos": {"hori": [20, 250], "vert": "unten"},
                            },
                        ],
                    }
                ],
            }
        ]
    }
    yaml["kabel"] = {
        "kabel": [
            {
                "id": 1,
                "name": "SK1 R22",
                "start": "1.1.1",
                "end": ["2.2.3", "2.2.4", "2.2.5"],
            }
        ]
    }
    return yaml


def single_wall():
    yaml = dict()
    yaml["struktur"] = {
        "geschosse": [
            {
                "id": 1,
                "name": "G1",
                "height": 200,
                "walls": [
                    {"id": 1, "pos": {"hori": [0, 0]}, "ende": [20, 500]},
                ],
            }
        ]
    }
    yaml["anschluesse"] = {
        "geschosse": [
            {
                "id": 1,
                "name": "G1",
                "rooms": [
                    {
                        "id": 1,
                        "name": "R11",
                        "objects": [
                            {
                                "id": 1,
                                "name": "O111",
                                "con-type": "steckdose",
                                "anzahl": 1,
                                "pos": {"hori": [20, 100], "vert": "unten"},
                            },
                            {
                                "id": 2,
                                "name": "O112",
                                "con-type": "steckdose",
                                "anzahl": 2,
                                "pos": {"hori": [20, 300], "vert": "unten"},
                            },
                            {
                                "id": 3,
                                "name": "O113",
                                "con-type": "steckdose",
                                "anzahl": 2,
                                "pos": {"hori": [20, 300], "vert": "mitte"},
                            },
                            {
                                "id": 4,
                                "name": "O114",
                                "con-type": "steckdose",
                                "anzahl": 2,
                                "pos": {"hori": [20, 300], "vert": "oben"},
                            },
                        ],
                    }
                ],
            }
        ]
    }
    yaml["kabel"] = {"kabel": []}
    return yaml
