class GameStats():
    """tracking of statistic for Alien Invasion game"""

    def __init__(self, ai_game):
        """initialise of statistic"""
        self.settings = ai_game.settings
        self.reset_stats()
        
        #game starts in inactive status
        self.game_active = False

        self.read_record()


    def reset_stats(self):
        """initialize of statistic in game"""
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def read_record(self):
        """read record from file and initialize it in game"""
        filename = 'text_files/record.txt'
        with open(filename) as f:
            self.high_score = int(f.read())
        return self.high_score

    def write_record(self):
        """write record to file"""
        filename = 'text_files/record.txt'
        with open(filename) as f:
            exist_rec = int(f.read())

            if self.high_score > exist_rec:
                filename = 'text_files/record.txt'
                with open(filename, 'w') as f:
                    new_rec = str(self.high_score)
                    f.write(new_rec)
    


