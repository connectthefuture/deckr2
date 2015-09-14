#!/usr/bin/env python
"""
This is a very simple CLI for deckr. It uses deckrclient as the primary backend.
"""

# pylint: skip-file

import readline
import traceback

import deckrclient.client


def printer_callback(message):
    """
    Just print out a message whenever we get it.
    """

    print message

def main():
    """
    Run main functionality.
    """

    client = deckrclient.client.DeckrClient(ip='127.0.0.1',
                                            port=8080,
                                            sync=False,
                                            callback=printer_callback)
    client.initialize()
    # Here is the poor man's REPL
    while True:
        try:
            print(input(">>> "))
        except (EOFError, KeyboardInterrupt): # These are actual exit conditions.
            break
        except SyntaxError: # For some reason a blank line causes a SyntaxError, just pass
            pass
        except: # Other exceptions should be logged and then we should continue the REPL
            traceback.print_exc()
    client.shutdown()

if __name__ == "__main__":
    main()
