"""Saving settings"""

import json

SETTINGS = {}
TEXT = {
        'eng': "!add + quote adds neue quote with current date and new number, !random returns a random quote, exciting, isn't it?, !quote + a number retrieves that quote",
        'ger': "!neu + Zitat fügt neues Zitat mit heutigem Datum und neuer ID ein, !zufall gibt ein zufälliges Zitat aus, spannend, was?, !zitat + eine Nummer gibt das spezifische Zitat aus'"
        }

def load_config():
    """
    Load config.json
    :return: Dict
    """
    with open('config.json') as config:
        return json.load(config)


def config_get(item):
    """
    Get information from config.json
    :param item: Json Key
    :return: String
    """
    with open('config.json') as config:
        return json.load(config)[item]
