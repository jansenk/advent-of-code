import re
input_pattern = re.compile(r'(?P<ingredients>.*?)\(contains (?P<allergens>.*?)\)')
def parseline(line):
	match = input_pattern.match(line)
	ingredients = match.group('ingredients')
	allergens = match.group('allergens')
	ingredients = ingredients.split()
	allergens = allergens.split(', ')
	return ingredients, allergens

from collections import defaultdict, Counter
def solve_p1(filename):
	f = open('advent/input_files/'+filename)
	result = dict()
	ingredients_counter = Counter()
	for line in f:
		ingredients, allergens = parseline(line)
		ingredients_counter.update(ingredients)
		for allergen in allergens:
			if allergen not in result:
				result[allergen] = set(ingredients)
			else:
				result[allergen] = result[allergen].intersection(set(ingredients))
	possible_ingredients = set()
	for allergen, possibilities in result.items():
		possible_ingredients.update(possibilities)
	n = 0
	for ingredient in ingredients_counter:
		if ingredient not in possible_ingredients:
			n += ingredients_counter[ingredient]
	print(n)
solve_p1('21.txt')

def solve_p2(filename):
	f = open('advent/input_files/'+filename)
	result = dict()
	for line in f:
		ingredients, allergens = parseline(line)
		for allergen in allergens:
			if allergen not in result:
				result[allergen] = set(ingredients)
			else:
				result[allergen] = result[allergen].intersection(set(ingredients))
	canonical = dict()
	while result:
		confirmed_items = set()
		finished_allergens = []
		for allergen, pi in result.items():
			if len(pi) == 1:
				finished_allergens.append(allergen)
				ingredient = pi.pop()
				confirmed_items.add(ingredient)
				canonical[allergen] = ingredient
		for allergen in finished_allergens:
			result.pop(allergen)
		for allergen in result:
			result[allergen].difference_update(confirmed_items)
	result_str = ""
	for allergen in sorted(canonical.keys()):
		result_str += canonical[allergen]
		result_str += ","
	result_str = result_str[:len(result_str)-1]
	print(result_str)

solve_p2('21.txt')
