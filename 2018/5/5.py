import string
f = open("in.txt", "r")
polymer = f.readline()
ignored_char = None
#polymer = "dabAcCaCBAcCcaDA"


def reacts(c1, c2):
    return ((c1.isupper() and c2.islower()) or (c1.islower() and c2.isupper())) and (c1.lower() == c2.lower())


def merge(str1, str2):
    #print("merging", str1, str2)
    while str1 and str2:
        if reacts(str1[-1], str2[0]):
            #print("reaction")
            str1 = str1[:-1]
            str2 = str2[1:]
        else:
            #print("done: " ,str1 + str2)
            return str1 + str2
    #print("done: ", str1 + str2)
    return str1+str2


def resolve(str):
    #print("resolving ", str)
    l = len(str)
    if l > 1:
        #print("split")
        half = int(l / 2)
        left = resolve(str[:half])
        right = resolve(str[half:])
        return merge(left, right)
    elif str.lower() == ignored_char:
        return ""
    else:
        return str



result = resolve(polymer)
print(len(result))

min = float("inf")
letter = None
for c in string.ascii_lowercase:
    ignored_char = c
    result = resolve(polymer)
    if len(result) < min:
        min = len(result)
        letter = c

print("best letter: %s, min length: %d" % (letter, min))





# 01234567 l=8
# l > 1
# half = 8-1 = 7   7/2 = 3.5 = 3

