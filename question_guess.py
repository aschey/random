import random
import math
import operator

trials = 10000
num_answers = 10000
num_correct = 5000
num_choices = 10

answers = [f"answer{i}" for i in range(num_answers)]

correct = [(choice, True) for choice in random.choices(answers, k=num_correct)]
t = [c[0] for c in correct]
incorrect = [(answer, False) for answer in answers if answer not in t]
guesses = dict()

class Guess:
    def __init__(self, answ, num, correct, weight):
        self.ans = answ
        self.num = num
        self.correct = correct
        self.weight = weight

def get_question():
    question = [random.choice(correct)]
    question.extend(random.sample(incorrect, num_choices-1))
    random.shuffle(question)
    return question

num_correct = 0
num_incorrect = 0
correct_guesses = 0
correct_found = 0

correct_total = 0
total = 0

rev = True
use_count = True

for i in range(trials):
    print(f'Round {i}')
    print('==========')
    question = get_question()
    remaining = []
    current_found = []
    for choice in question:
        if choice[0] in guesses:
            guesses[choice[0]].num += 1
            if guesses[choice[0]].correct:
                print(f'Found correct guess {choice[0]}')
                num_correct += 1
                correct_found += 1
                for w_choice in [w_choice for w_choice in question if w_choice[0] != choice[0]]:
                    guesses[w_choice[0]] = Guess(w_choice[0], 1, False, 0)
                remaining = []
                break
            elif guesses[choice[0]].correct == None:
                print(f'Found unknown guess {choice[0]}. Count {guesses[choice[0]].num}. Weight {guesses[choice[0]].weight}')
                remaining.append(choice)
                current_found.append(guesses[choice[0]])
            else:
                print(f'Found incorrect guess {choice[0]}')
        else:
            #print(f'Adding new guess {choice[0]}')
            guesses[choice[0]] = Guess(choice[0], 1, None, None)
            remaining.append(choice)
    if len(remaining) > 0:
        print(f'{len(remaining)} remaining')
        if len(current_found) > 0 and use_count:
            current_names = [c.ans for c in current_found]
            extra = [Guess(r[0], 1, None, 1 / len(remaining)) for r in remaining if r[0] not in current_names]
            current_found.extend(extra)
            for c in current_found:
                c.weight = max(c.weight, 1 / len(remaining))
            current_found.sort(key=lambda c: (c.weight, c.num), reverse=rev)
            for c in current_found:
                print(f'{c.ans}: {c.weight}')
            total_weight = sum(c.weight for c in current_found)
            weighted_avg = current_found[0].weight / total_weight
            print(f'Weighted average: {weighted_avg}. Unweighted {1 / len(remaining)}')
            guess = [r for r in remaining if r[0] == current_found[0].ans][0]
            print(f'Using guess {current_found[0].ans} with percentage {current_found[0].weight}')

            total += weighted_avg
            if guess[1]:
                correct_total += weighted_avg
        else:
            print(f'Guessing randomly from {len(remaining)} choices')
            guess = random.choice(remaining)
        if guess[1]:
            print('Guessed correctly')
            num_correct += 1
            correct_guesses += 1
            guesses[guess[0]] = Guess(guess[0], 1, True, 1)
            for w_choice in [w_choice for w_choice in question if w_choice[0] != guess[0]]:
                guesses[w_choice[0]] = Guess(w_choice[0], 1, False, 0)
        else:
            print('Guessed incorrectly')
            num_incorrect += 1
            others = [other for other in remaining if other[0] != guess[0]]
            print(f'Assigning weights of {1 / len(others)}')
            for other in others:
                weight = guesses[other[0]].weight
                guesses[other[0]].weight = max(1 / len(others), weight if weight is not None else 0)
            if len(others) == 1:
                print('Found answer by process of elimination')
                guesses[others[0][0]].weight = 1
                guesses[others[0][0]].correct = True
            guesses[guess[0]] = Guess(guess[0], 1, False, 0)

    print('\n')
print(f'Correct {num_correct}')
print(f'Incorrect {num_incorrect}')
print(f'Correct guesses {correct_guesses}')
print(f'Correct found {correct_found}')
print(f'Percent correct {num_correct / (num_correct + num_incorrect)}')
print(f'Probability score {correct_total / total}')