"""
This module provides the BirthingPodMaster class and some of the associated
functionality.
"""

import random

class Match(object):
    """
    This represents a match between two decks.
    """

    def __init__(self, first_deck, second_deck):
        self.first_deck = first_deck
        self.second_deck = second_deck

class DeckIndividual(object):
    """
    This class is created by the GeneticController and represents a single
    deck. This class also holds stats about how the deck is performing in
    the current generation.
    """

    def __init__(self, deck):
        self.deck = deck # The actual cards in the deck.
        self.win_count = 0
        self.lose_count = 0

class GeneticController(object):
    """
    This class runs the actual genetic algorithm.
    """

    def __init__(self, population_size=10):
        self.population_size = population_size
        self.population = []

    def initialize(self):
        """
        Create the initial gene pool.
        """

        self.population = [
            DeckIndividual(["Forest"] * random.randint(7, 15)) for _ in range(self.population_size)
        ]

    def get_matches(self):
        """
        Get the matches that should be run for this generation.
        """

        return [
            Match(random.choice(self.population), random.choice(self.population))
            for _ in range(20)
        ]

    def evolve(self):
        """
        This function will update the gene pool, weeding out the week add
        promoting the strong.
        """

        print "EVOLVE!"
        scores = [(x.win_count - x.lose_count, x.deck) for x in self.population]
        scores.sort(reverse=True)
        # Take the top third and replicate
        new_population = []
        for i in range(len(scores) / 3):
            new_population.append(DeckIndividual(scores[i][1]))
            new_population.append(DeckIndividual(scores[i][1]))
            new_population.append(DeckIndividual(scores[i][1]))
        self.population = new_population

class BirthingPodMaster(object):
    """
    This is the catch all master class for bithing pod. It tracks current decks,
    stats, etc.
    """

    def __init__(self):
        self.genetic_controller = GeneticController()
        self._matches = []
        self._job_id = 0
        # Map from jobs to their decks
        self._current_jobs = {}

    def initialize(self):
        """
        Set up the birthing pod master.
        """

        self.genetic_controller.initialize()
        self._matches = self.genetic_controller.get_matches()

    def get_job(self):
        """
        Get the next job. This will return a dictionary of the important
        information for the next game to play.

        Returns
            {
                'deck1': First deck, should go first in the game
                'deck2': Second deck, should go second.
                'job_id': Unique id for this job
            }
        """

        if self._matches == []: # We need some more matches. Evolve!
            # (It's possible we don't have all of the data. We'll have to live)
            self.genetic_controller.evolve()
            self._matches = self.genetic_controller.get_matches()


        match = self._matches.pop()
        deck1 = match.first_deck
        deck2 = match.second_deck
        job_id = self._job_id
        self._job_id += 1
        self._current_jobs[job_id] = match

        return {
            'deck1': deck1.deck,
            'deck2': deck2.deck,
            'job_id': job_id
        }



    def report(self, stats):
        """
        This takes in a dictionary of stats and updates the proper deck object.

        Format is
        {
            'job_id': JOB_ID,
            'won': 1 if deck1 won, 2 if deck2 won.
        }
        """

        job_id = stats['job_id']
        match = self._current_jobs[job_id]
        if stats['won'] == 1:
            match.deck1.win_count += 1
            match.deck2.lose_count += 1
        else:
            match.deck2.win_count += 1
            match.deck1.lose_count += 1
        del self._current_jobs[job_id]
