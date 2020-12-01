from collections import deque

def load_deck(f):
	first_line = f.readline()
	deck = deque()
	while True:
		line = f.readline().strip()
		if line.isdigit():
			deck.append(int(line))
		else:
			return deck

def load_decks(filename):
	with open('advent/input_files/'+filename) as f:
		deck1 = load_deck(f)
		deck2 = load_deck(f)
	return (deck1, deck2)

def play_game(deck1, deck2):
	r = 1
	while len(deck1) and len(deck2):
		print(f'-- Round {r} --')
		print(f"Player 1's deck: {deck1}")
		print(f"Player 2's deck: {deck2}")
		p1c = deck1.popleft()
		p2c = deck2.popleft()
		print(f"Player 1 plays: {p1c}")
		print(f"Player 2 plays: {p2c}")
		if p1c > p2c:
			print("Player 1 wins the round")
			deck1.extend([p1c, p2c])
		else:
			print("Player 2 wins the round")
			deck2.extend([p2c, p1c])
		r += 1
	print("== Post-game results == ")
	print(f"Player 1's deck: {deck1}")
	print(f"Player 2's deck: {deck2}")
	return deck1 if deck1 else deck2

def solve_p1(filename):
	decks = load_decks(filename)
	winning_deck = play_game(*decks)
	result = 0
	for i, card in enumerate(reversed(winning_deck), start=1):
		result += i * card
	print(result)

# solve_p1('22.txt')

game_count = 1
def play_game_2(deck1, deck2, p=False):
	global game_count
	current_game = game_count
	if p:
		print(f'++++ Game {current_game} +++++')
	game_count += 1
	r = 1
	deck_configurations = set()
	while len(deck1) and len(deck2):
		deck_configuration = str((deck1, deck2))
		if deck_configuration in deck_configurations:
			return 1, deck1
		else:
			deck_configurations.add(deck_configuration)
		if p:
			print(f'-- Round {r} (Game {current_game}) --')
			print(f"Player 1's deck: {deck1}")
			print(f"Player 2's deck: {deck2}")
		p1c = deck1.popleft()
		p2c = deck2.popleft()
		if p:
			print(f"Player 1 plays: {p1c}")
			print(f"Player 2 plays: {p2c}")
		if len(deck1) >= p1c and len(deck2) >= p2c:
			if p:
				print("Playing a sub-game to determine the winner...\n")
			winner, _ = play_game_2(
				deque(list(deck1)[:p1c]),
				deque(list(deck2)[:p2c]),
			)
			if p:
				print(f"\n...anyway, back to game {current_game}.")
			if winner == 1:
				deck1.extend([p1c, p2c])
			else:
				deck2.extend([p2c, p1c])
		elif p1c > p2c:
			winner = 1
			deck1.extend([p1c, p2c])
		else:
			winner = 2
			deck2.extend([p2c, p1c])
		if p:
			print(f"Player {winner} wins round {r} of game {current_game}")
		r += 1
	if deck1:
		result = 1, deck1
	else:
		result = 2, deck2
	if p:
		print(f'The winner of game {current_game} is player {result[0]}!')
	return result

def solve_p2(filename):
	decks = load_decks(filename)
	winner, winning_deck = play_game_2(*decks)
	print("winning deck: " +str(winner) + "  " + str(winning_deck))
	result = 0
	for i, card in enumerate(reversed(winning_deck), start=1):
		result += i * card
	print(result)

solve_p2("22.txt")