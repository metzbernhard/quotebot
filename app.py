"""This module starts a forever running Python bot for quotes on IRC"""

import logging
import argparse
import sys

import quote
import settings
import pushsftp
from settings import SETTINGS as sett
from ircsocket import IrcSocket

def main():
    """
    Main method to get started
    opens connection and starts endless while loop for polling IRC Channel
    """

    # get arguments from command line
    args = parse()

    # set our settings for this run
    sett["language"] = args.language if args.language else settings.config_get("language")

    # language option
    commands = {'add': '!add', 'random': '!random', 'quote': '!quote', 'quotebot': '!quotebot'}
    if sett["language"] == 'german':
        commands = {'add': '!neu', 'random': '!zufall', 'quote': '!zitat', 'quotebot': '!quotebot'}

    # do some logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logging.info(commands)

    # open connection
    connection = IrcSocket(args)
    quote.allQuotes()

    # this'll run as long as you don't kill it
    while 1:
        text = connection.sock.recv(2040).decode()
        logger.info(text)

        # answer pings to stay connected
        if 'PING' in text:
            logger.info('Answer ping')
            connection.send_ping('PONG :tmi.twitch.tv\r\n')

        # ignore messages that aren't commands
        # only catches commmands if at the beginning of the message
        elif ':!' not in text:
            pass

        else:
            try:
                user = text[text.index('!') + 1:text.index('@')]
            except ValueError:
                continue
                #some default twitch messages don't fit the bill, but don't give us a user anyway

            text = text[text.rfind(':') + 1:].strip()

            # add quote
            if text.startswith(commands.get('add')):

                connection.send_msg(user.title() + ': ' + quote.addQuote(text))

            # random quote
            elif text.startswith(commands.get('random')):

                connection.send_msg(user.title() + ': ' + quote.randomQuote())

            # specific quote
            elif text.startswith(commands.get('quote')):

                connection.send_msg(user.title() + ': ' + quote.numQuote(text))
                #connection.send_msg(user.title() + ': kommt bald')

            # info
            elif text.startswith(commands.get('quotebot')):

                connection.send_msg(user.title() + ': ' + quote.infoQuote())

            # temp
            elif text.startswith('!marvinck2'):

                connection.send_msg(user.title() + ': ' + quote.printfile('ck2.txt'))

            elif text.startswith('!quit_now'):

                quote.close()
                sys.exit()



def parse():
    """
    Get arguments from the commandline
    :return:
    """
    parser = argparse.ArgumentParser(description='IRC Quote Bot')

    parser.add_argument('-b', dest='bot', action='store', help='Twitch Account used as bot')
    parser.add_argument('-c', dest='channel', action='store', help='Channel you want to use')
    parser.add_argument('-o', dest='auth', action='store', help='oauth "oauth:oauth_token"')
    parser.add_argument('-l', dest='language', action='store', help='english or german')

    return parser.parse_args()


if __name__ == '__main__':
    main()
