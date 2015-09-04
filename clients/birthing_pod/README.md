BirthingPod is a system for developing new magic decks. It involves a central server that creates
decks, and several worker processes that play simulated games against one another. The server uses
win percentage data to construct better and better decks over time.

To run the server you'll need to do three things in order:

1) Start the deckr server (./bin/run_deckr_server)
2) Start the birthing pod server (./birthing_pod_server.py)
3) Start the workers (./run_workers.py NUM_WORKERS) I generally run with 8-16 workers.
