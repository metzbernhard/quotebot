import os
import sqlite3
import logging
from datetime import datetime
from settings import SETTINGS as settings
from settings import TEXT

# open connection to sqlite database
db = sqlite3.connect('quotes.sqlite')
cursor = db.cursor()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def addQuote(text):
    text = text[5:]
    date = datetime.now().strftime('%d.%m.%Y')

    command = f"INSERT INTO quotes(text, date) VALUES('{text}', '{date}')"
    logger.info(command)
    cursor.execute(command)

    db.commit()

    cursor.execute(f"SELECT id FROM quotes WHERE text = '{text}' and date = '{date}'")
    id = cursor.fetchone()[0]

    return "Done! ID = " + str(id)


def getQuote(quote):
    if settings['language'] == 'english':
        try:
            result = f'Quote #{quote[0]}: |{quote[1]}| from the {quote[2]}'
        except TypeError:
            result = 'This quote does not exist'
    else:
        try:
            result = f'Zitat #{quote[0]}: |{quote[1]}| vom {quote[2]}'
        except TypeError:
            result = 'Zitat existiert nicht'
    return result


def randomQuote():
    cursor.execute('SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1')
    quote = cursor.fetchone()
    result = getQuote(quote)
    return result


def numQuote(text):
    try:
        id = text[text.index(' '):].strip()
        command = f"SELECT * FROM quotes WHERE id = '{id}'"
        logger.info(command)
        cursor.execute(command)
        result = getQuote(cursor.fetchone())
        return result
    except ValueError:
        return randomQuote()


def infoQuote():
    if settings['language'] == 'english':
        result = TEXT['eng']
    else:
        result = TEXT['ger']
    return result


def allQuotes():
    command = "SELECT * FROM quotes"
    cursor.execute(command)
    with open("C:\\Users\\ad\\ownCloud\\Code\\quote\\Legendarymarvin Zitate.html", "r") as f:
        text = f.readlines()

    table = []
    for row in cursor.fetchall():
        newrow = f"Zitat {row[0]} vom {row[2]}: {row[1]}\n"
        table.append(newrow)

    with open("zitate.txt", 'w+') as f:
        f.writelines(table)



def close():
    db.close
    return None

def printfile(file):
    """
    Reads out goal.txt and gives out the content
    :return: String
    """
    goal = os.path.join(os.path.dirname(os.path.realpath(__file__)), file)
    with open(goal, 'r') as f:
        text = f.readlines()

    return ' '.join(text)
