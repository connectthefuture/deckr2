Deckr2 (version 0.1a)
=====================

server
------
Run the server using the following command:
./bin/run_deckr_server.py

clients
-------
There are several different client available:
decrkcli: A simple command line interface for deckr. Good for low level commands.
deckrClient: A full python interface for deckr. Good for automation and building other tools.
onepage: A very simple single page client for deckr. This is mainly for debugging and development.


Notes:
You may need to hack txsockjs to get connection to work properly https://github.com/DesertBus/sockjs-twisted/issues/30
