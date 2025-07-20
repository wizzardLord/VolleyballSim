import random

class Player:
    """
    Player is a class representing a player in the volleyball
    simulator. A Player is represented by its name, contains six numerical
    'stats', a position (what role this player plays), and a start position
    (where to start this player in the rotation.
    """

    def __init__(self, string: str):
        self.string = string
        string = string.split('|')
        self.name = string[0]
        self.position = string[1]

        self.power = int(string[2])
        self.jumping = int(string[3])
        self.stamina = (6 - int(string[4]))/100
        self.sense = int(string[5])
        self.technique = int(string[6])
        self.speed = int(string[7])

        self.start_position = int(string[8])


    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Player({self.name}|{self.position}|{self.power}|{self.jumping}|{self.stamina}|{self.sense}|{self.technique}|{self.speed}|{self.start_position})'

    def get_position(self):
        """
        Returns card position
        :return: The card's position (str)
        """
        return self.position

    def get_start_position(self):
        """
        Returns cards start rotation position.
        :return: The card's start position (int)
        """
        return self.start_position

    def spike(self, block: bool):
        """
        Simulates this player spiking. Takes a random integer between 1 and 20 and
        adds either jumping and power or power and sense depending on whether the
        previous block succeeded.
        Then lowers the player's power by their stamina rating.
        :param block: Either a positive integer or False (used for boolean purposes)
        :return: A rating for the spike (random number plus relevant stats)
        """
        spike_rating = random.randint(1, 20)
        if block:
            spike_rating += round(self.power + self.sense)
        else:
            spike_rating += round(self.jumping + self.power)

        self.power -= self.stamina

        return spike_rating

    def block(self, set: int):
        """
        Takes a random integer between 1 and 20 and adds this player's
        jumping and speed. Lowers this player's jumping by their stamina.
        :param set: An integer (generally between 1 and 30)
        :return: Either the block rating (if greater than the input int)
        or False (if not greater).
        """
        block_rating = random.randint(1,20) + round(self.jumping + self.speed)

        self.jumping -= self.stamina

        if block_rating > set:
            return block_rating
        else:
            return False

    def serve(self):
        """
        Takes a random integer from 1 to 20 and adds this player's
        power and technique. Lowers technique by stamina.
        :return: Either the serve rating (if greater than 9) or
        False (if less than 10)
        """
        serve_rating = random.randint(1,20) + round(self.power + self.technique)

        self.technique -= self.stamina

        if serve_rating >= 10:
            return serve_rating
        else:
            return False

    def set(self):
        """
        Takes a random integer between 1 and 20 and adds this player's
        technique and sense. Lowers sense by half stamina.
        :return: The set rating (random int plus relevant stats)
        """
        set_rating = random.randint(1,20) + round(self.technique + self.sense)

        self.sense -= self.stamina/2

        return set_rating

    def receive(self, spike: int):
        """
        Takes a random integer between 1 and 20 and adds speed and
        sense. Lowers speed by stamina.
        :param spike: An integer (generally between 1 and 30)
        :return: True if the random integer is greater than or equal to
        the input, False otherwise.
        """
        receive_rating = random.randint(1,20) + round(self.speed + self.sense)

        self.speed -= self.stamina

        if receive_rating >= spike:
            return True
        else:
            return False


def team_setup(file: str):
    """
    Takes a text file containing the stats for a team and
    extrapolates it into the intended team.
    :param file: The string name of a text file containing only
    lines that follow the following pattern:
    Name|Position|Power|Jumping|Stamina|Sense|Technique|Speed|Start-Position
    Name and position should be strings, all others should be convertible to
    integers.
    :return: A list of the players created by each line of the text file.
    """
    file = open(file, 'r')
    file = file.read()
    file = file.split('\n')
    team = []
    for player in file:
        team.append(Player(player))
    return team
