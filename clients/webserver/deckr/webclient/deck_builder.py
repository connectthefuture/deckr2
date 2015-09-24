def build_deck(deck_text):
    deck = []
    for line in deck_text.split('\n'):
        card = line.split(' ')
        deck += [str(card[1]) for _ in range(int(card[0]))]
    return deck
