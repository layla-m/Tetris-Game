class Colours:
    # Colours used in the game
    purple_background = (73, 35, 79)
    white_purple = (195, 151, 201)
    purple_empty_cell = (55, 26, 60)
    mint = (100, 156, 131)
    blue_grey = (100, 110, 156)
    lilac = (135, 100, 156)
    salmon = (227, 134, 109)
    yellow = (237, 204, 119)
    pink = (237, 145, 208)
    redish = (240, 60, 96)

    @classmethod
    def get_cell_colours(cls):
        return [cls.purple_empty_cell, cls.mint, cls.blue_grey, cls.lilac, cls.salmon, cls.yellow, cls.pink, cls.redish]