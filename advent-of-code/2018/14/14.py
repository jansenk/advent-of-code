from collections import deque
steps = 0
TARGET = 30121
STR_T = "030121"
done_steps = TARGET+ 10
target_deque = deque(maxlen=len(STR_T))
target_deque.extend(int(i) for i in STR_T)

state = [3, 7]
elf1 = 0
elf2 = 1

def move(elf):
    steps = state[elf] + 1
    return (elf + steps) % len(state)

def doStep(e1, e2):
    result = []
    newScore = state[e1] + state[e2]
    if newScore >= 10:
        result.append(int(newScore / 10))
    result.append(newScore % 10)
    return result

# while len(state) < done_steps:
#    state.extend(doStep(elf1, elf2))
 #    move(e1), move(e2)
#     steps += 1
# print(state[TARGET_STEPS:TARGET_STEPS+10])

print target_deque
current_window = deque(maxlen=len(STR_T))
current_window.extend(state)
done = False
while not done:
    newRecipies = doStep(elf1, elf2)
    for newRecipe in newRecipies:
        state.append(newRecipe)
        current_window.append(newRecipe)
        #print(current_window)
        #print(state)
        if current_window == target_deque:
            done = True
            break
    elf1 = move(elf1)
    elf2 = move(elf2)

print("done")
print(len(state) - len(target_deque))






