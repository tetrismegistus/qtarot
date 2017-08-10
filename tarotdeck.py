import collections

Card = collections.namedtuple('card', ['rank', 'kind', 'image'])

class TarotDeck:
    ranks = ['Ace'] + [str(n) for n in range(2, 11)] + 'Page Queen King Knight'.split()
    suits = 'swords wands coins cups'.split()
    numerals = [str(n) for n in range(0, 22)]
    titles = ['The Fool', 'The Magician', 'The Popess', 'The Empress', 'The Emperor',
              'The Pope', 'The Lover', 'The Chariot', 'Justice', 'The Hermit',
              'The Wheel of Fortune', 'Strength', 'The Hanged Man', 'Death',
              'Temperance', 'The Devil', 'The House of God', 'The Star', 'The Moon',
              'The Sun', 'Judgement', 'The World']

    def __init__(self):
        minor_image = 'images/{}/{}.jpg'
        major_image = 'images/majors/{}.jpg'
        self._cards = [Card(rank, suit, minor_image.format(suit, rank)) for suit in self.suits
                                                                        for rank in self.ranks]
        self._cards += [Card(c[0], c[1], major_image.format(c[0])) for c in zip(self.numerals, self.titles)]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __setitem__(self, key, value):
        self._cards[key] = value

    def pop(self, key=-1):
        card = self._cards.pop(key)
        return card
