def create_deck():
    return ["Forest"] * random.randint(7, 15)

class DeckStats(object):

    def __init__(self, deck):
        self.deck = deck
        self.win_count = 0
        self.lose_count = 0

    def update_stats(self, stats):
        """
        Update the stats for this deck.
        """

        if stats['lost']:
            self.lose_count += 1
        else:
            self.win_count += 1

class BirthingPod(object):
    """
    This is the overall manager class. It tracks decks that it's created, their current wins and
    loses, etc.
    """

    POOL_SIZE = 10

    def __init__(self):
        self.next_playback_id = 0 # The next playback id
        self.client = simple_client.SimpleClient()

        self.decks = []
        self.pending_game = None
        self.playbacks = {

        }

    def initialize(self):
        """
        Get everything set up properly.
        """

        self.client.initalize()

        # Create some random decks
        for _ in range(self.POOL_SIZE):
            self.decks.append(DeckStats(create_deck()))

    def get_game(self):
        """
        Get the data for the next worker.
        """

        if self.pending_game is None:
            self.client.create()
            response = self.client.listen()
            game_id = response.create_response.game_id
            self.pending_game = game_id
            start = False
        else:
            game_id = self.pending_game
            self.pending_game = None
            start = True

        playback_id = self.next_playback_id
        self.next_playback_id += 1


        deck = random.choice(self.decks)
        self.playbacks[playback_id] = deck

        return {
            'game_id': game_id,
            'deck': deck.deck,
            'start': start,
            'playback_id': playback_id
        }

    def update_stats(self, stats):
        """
        Update the stats when a game has completed.
        """

        self.playbacks[stats['playback_id']].update_stats(stats)
        del self.playbacks[stats['playback_id']]
