class Settings():
    """class for storage all settings of a game Alien Invasion"""

    def __init__(self):
        """Initializing static settings of the game"""
        
        #display parameters
        self.screen_width = 1100
        self.screen_height = 700
        self.bg_color = (230, 230, 230)

        #ship parameters
        self.ship_limit = 3

        #bullet parameters
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 5

        #alien parameters
        self.fleet_drop_speed = 15

        #game acceleration rate
        self.speedup_scale = 1.1
        #pace of growing alien value
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """initialize changable parameters of game"""
        self.ship_speed = 10
        self.bullet_speed = 5.0
        self.alien_speed = 3.0

        # fleet_direction = 1 means moving to the right; "-1" - to the left
        self.fleet_direction = 1

        #count of score
        self.alien_points = 50

    def increase_speed(self):
        """increase game parameters and alien's value"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

