# Abd Alah Fashesh

import pygame

class Scoreboard:
    def __init__(self):
        self.score = 0           # current game score
        self.all_scores = []     # history of past final scores

    def reset(self):
        self.score = 0           # reset score for a new game

    def increase_score(self):
        self.score += 1          # called when snake eats; bump score

    def record_final_score(self):
        self.all_scores.append(self.score)  # save final score to history

    def get_first_of_sorted(self, arr):
        # bubble sort on a copy to avoid mutating original list
        if not arr:
            return 0
        lst = arr.copy()
        n = len(lst)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if lst[j] > lst[j + 1]:
                    lst[j], lst[j + 1] = lst[j + 1], lst[j]
                    swapped = True
            if not swapped:
                break
        return lst[-1]  # highest value ends up at the end
