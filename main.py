from player import *
import time

def serve(team: list[Player], opponent: list[Player], team_colour: str, opp_colour: str):
    """
    Function to operate the serve portion of the volleyball simulation.
    Returns the team that won the point either directly (on a serve value
    less than 10), or indirectly (through continuing the point).
    Next step is receive.
    :param team: List containing Players, at least length 6
    :param opponent: List containing Players at least length 6
    :param team_colour: A string (using escape codes to colour the terminal)
    :param opp_colour: A string (using escape codes to colour the terminal)
    :return: The team that won the point.
    """
    server = team[0]

    target = random.choice(opponent)
    while target.get_position() not in ['MB', 'WS', 'O']:
        target = random.choice(opponent)

    serve_score = server.serve()

    if serve_score:
        print(f'{team_colour}Served by {server} \033[0;0m')
        return receive(opponent, team, serve_score - 5, target, opp_colour, team_colour)

    else:
        print(f'{team_colour}{server} misses the serve \033[0;0m')
        return opponent

def receive(team: list[Player], opponent: list[Player], difficulty: int, target: Player, team_colour: str, opp_colour: str):
    """
    Simulates the receive portion of the volleyball simulator.
    Either continues onto the set function if receive score is
    greater than the difficulty or returns the opponent otherwise.
    :param team: List of Players. At least length 6
    :param opponent: List of Players. At least length 6
    :param difficulty: Integer (generally between 1 and 30)
    :param target: A Player object (generally in the team variable)
    :param team_colour: A string (using escape codes to colour the terminal)
    :param opp_colour: A string (using escape codes to colour the terminal)
    :return: The team that won the point.
    """
    time.sleep(0.8)
    receive_score = target.receive(difficulty)

    if receive_score:
        print(f'{team_colour}Passed by {target} \033[0;0m')
        return set(team, opponent, target, team_colour, opp_colour)

    else:
        print(f'{team_colour}{target} misses the receive. \033[0;0m')
        return opponent

def set(team: list[Player], opponent: list[Player], receiver: Player, team_colour: str, opp_colour: str):
    """
    A function that simulates the set portion of the volleyball
    simulator.
    :param team: List of Players. At least length 6
    :param opponent: List of Players. At least length 6
    :param receiver: A Player (generally in team variable)
    :param team_colour: A string (using escape codes to colour the terminal)
    :param opp_colour: A string (using escape codes to colour the terminal)
    :return: The team that won the point (through the use of the block function)
    """
    time.sleep(0.8)
    # Selects the setter. Cannot be the same as the receiver but prefered to be position: 'S'
    if receiver.get_position() != 'S':
        setters = [player for player in team if player.get_position() == 'S']
        setter = random.choice(setters)
    else:
        setter = random.choice([player for player in team if player != receiver])

    #Chooses a Player to set to. Cannot be the setter or a Player with position: 'L'
    set_choice = []
    for index, player in enumerate(team):
        if player != setter and player.get_position() != 'L':
            for i in range(round(player.jumping + player.power + player.sense)):
                set_choice.append(player)
                if index in [1,2,3]:
                    set_choice.append(player)

    set_rating = setter.set()
    spiker = random.choice(set_choice)

    print(f'{team_colour}Set by {setter} \033[0;0m')

    return block(opponent, team, set_rating, spiker, opp_colour, team_colour)

def block(team: list[Player], opponent: list[Player], set_score: int, spiker: Player, team_colour: str, opp_colour: str):
    """
    A function that operates the block portion of the volleyball
    simulator.
    :param team: List of Players. At least length 6
    :param opponent: List of Players. At least length 6
    :param set_score: An integer (generally between 1 and 30)
    :param spiker: A Player (generally in team variable)
    :param team_colour: A string (using escape codes to colour the terminal)
    :param opp_colour: A string (using escape codes to colour the terminal)
    :return: The team that won the point (through the spike function)
    """
    blockers = [player for index, player in enumerate(team) if index in [1,2,3]]
    blocker = random.choice(blockers)
    block_score = blocker.block(set_score)

    return spike(opponent, team, block_score, spiker, blocker, opp_colour, team_colour)

def spike(team: list[Player], opponent: list[Player], block_score: int, spiker: Player, blocker: Player, team_colour: str, opp_colour: str):
    """
    A function that operates the spike portion of the volleyball
    simulator.
    :param team: List of Players. At least length 6
    :param opponent: List of Players. At least length 6
    :param block_score: An integer (generally between 1 and 30)
    :param spiker: A Player (generally in team variable)
    :param blocker: A Player (generally in opponent variable)
    :param team_colour: A string (using escape codes to colour the terminal)
    :param opp_colour: A string (using escape codes to colour the terminal)
    :return: The team that won the point (through the receive function). May either
    utilise the receive function for team or opponent depending on whether the block
    score is higher than the spike score.
    """
    time.sleep(0.8)
    spike_score = spiker.spike(block_score)

    if block_score and block_score > spike_score:
        print(f'{opp_colour}{spiker} is blocked by {blocker}! \033[0;0m')
        target = random.choice([player for index, player in enumerate(team) if index in [0,4,5]])
        return receive(team, opponent, block_score, target, team_colour, opp_colour)
    else:
        print(f'{team_colour}Spiked by {spiker}. \033[0;0m')
        target = random.choice([player for index, player in enumerate(opponent) if index in [0,4,5]])
        return receive(opponent, team, spike_score, target, opp_colour, team_colour)



def game_set(team_one: list, team_two: list, team_name_one: str, team_name_two: str, colours: dict, reserves_one: list, reserves_two: list):
    """
    Operates a set of the volleyball simulator. Repeatedly calls the serve
    function until a team has at least 25 points and a lead of 2.
    :param team_one: List of Players. At least length 6
    :param team_two: List of Players. At least length 6
    :param team_name_one: A string.
    :param team_name_two: A string.
    :param colours: A dictionary containing keys (team_name_one and team_name_two)
    that map to strings that are escape codes to colour the terminal.
    :param reserves_one: List of Players.
    :param reserves_two: List of Players.
    :return: The team that won the set. (i.e. at least 25 points and leads by 2)
    """
    # Set up points, sort teams into correct starting rotation.
    points = {
        team_name_one: 0,
        team_name_two: 0
    }
    team_one.sort(key=lambda player: player.get_start_position())
    team_two.sort(key=lambda player: player.get_start_position())
    serve_team = team_one
    receive_team = team_two


    # The main loop. Runs until one team has 25 points and leads by two.
    while (points[team_name_one] < 25 and points[team_name_two] < 25) or -2 < points[team_name_one] - points[team_name_two] < 2:
        # Runs the point simulation
        if serve_team == team_one:
            winner = serve(serve_team, receive_team, colours[team_name_one], colours[team_name_two])
        else:
            winner = serve(serve_team, receive_team, colours[team_name_two], colours[team_name_one])

        # Adds points to the winner
        if winner == team_one:
            points[team_name_one] += 1
        else:
            points[team_name_two] += 1

        # Prints the score to the user and waits for the user to press ENTER to continue
        time.sleep(0.8)
        input(f'\n{colours[team_name_one]}{team_name_one}: {points[team_name_one]}{colours['Clear']}\n'
              f'{colours[team_name_two]}{team_name_two}: {points[team_name_two]}{colours['Clear']}\n')

        # Rotate winning team if serve change.
        if winner != serve_team:
            winner.append(winner.pop(0))

            receive_team = serve_team
            serve_team = winner


        # Checks for automatic substitutes. If player position 'MB' in rotation position 0,4,5: should
        # be swapped for player position 'L' in subs. If player position 'L' in rotation position 1,2,3:
        # should be swapped for player position 'MB' in subs. Runs this for both teams.
        for index, player in enumerate([player for index, player in enumerate(team_one) if index in [0,4,5]]):
            if player.get_position() == 'MB':
                for sub in reserves_one:
                    if sub.get_position() == 'L':
                        reserves_one.append(player)
                        team_one[index] = sub

        for index, player in enumerate([player for index, player in enumerate(team_one) if index in [1,2,3]]):
            if player.get_position() == 'L':
                for sub in reserves_one:
                    if sub.get_position() == 'MB':
                        reserves_one.append(player)
                        team_one[index + 1] = sub

        for index, player in enumerate([player for index, player in enumerate(team_one) if index in [0,4,5]]):
            if player.get_position() == 'MB':
                for sub in reserves_two:
                    if sub.get_position() == 'L':
                        reserves_two.append(player)
                        team_two[index] = sub

        for index, player in enumerate([player for index, player in enumerate(team_two) if index in [1,2,3]]):
            if player.get_position() == 'L':
                for sub in reserves_two:
                    if sub.get_position() == 'MB':
                        reserves_two.append(player)
                        team_two[index + 1] = sub


    # Returns the team that won.
    if points[team_name_one] > points[team_name_two]:
        return team_one
    else:
        return team_two


def match(team_name_one: str, team_name_two: str):
    """
    Simulates a match in the volleyball simulator.
    :param team_name_one: A string (Should have associated text file i.e. team_name_one.txt)
    :param team_name_two: A string (Should have associated text file i.e. team_name_two.txt)
    :return: Nothing
    """

    # Sets up the teams, gets team colours.
    colours = {}
    print('Colours: \n'
          '0 - Black\n'
          '1 - Red\n'
          '2 - Green\n'
          '3 - Yellow\n'
          '4 - Blue\n'
          '5 - Purple\n'
          '6 - Cyan\n'
          '7 - Gray')

    team_one = team_setup(f'{team_name_one}.txt')

    colours[team_name_one] = f'\033[30;4{input(f'{team_name_one} colour: ')};1m '

    team_two = team_setup(f'{team_name_two}.txt')

    colours[team_name_two] = f'\033[30;4{input(f'{team_name_two} colour: ')};1m '

    colours['Clear'] = f' \033[0;0m'

    # Separates reserves from starters (Any player outside the first 6 in each team)

    reserves_one = []

    team_one.sort(key=lambda player: player.get_start_position())
    team_two.sort(key=lambda player: player.get_start_position())

    if len(team_one) > 6:
        for player in [player for index, player in enumerate(team_one) if index > 5]:
            reserves_one.append(player)
    for player in reserves_one:
        team_one.remove(player)

    reserves_two = []

    if len(team_two) > 6:
        for player in [player for index, player in enumerate(team_two) if index > 5]:
            reserves_two.append(player)
    for player in reserves_two:
        team_two.remove(player)


    sets = {
        team_name_one: 0,
        team_name_two: 0
    }

    # Runs the game until one team has won three sets.

    while sets[team_name_one] < 3 and sets[team_name_two] < 3:
        winner = game_set(team_one, team_two, team_name_one, team_name_two, colours, reserves_one, reserves_two)
        if winner == team_one:
            sets[team_name_one] += 1
        else:
            sets[team_name_two] += 1

        print(f'{colours[team_name_one]}{team_name_one}: {sets[team_name_one]}{colours['Clear']}\n'
              f'{colours[team_name_two]}{team_name_two}: {sets[team_name_two]}{colours['Clear']}')

match(input('Team Name One: '), input('Team Name Two: '))

