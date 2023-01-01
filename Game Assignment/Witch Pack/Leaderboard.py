import pygame
import datetime 
import os
import json

class Leaderboard(pygame.font.Font):
    FILE_NAME = "highscore.json"
    score = None
    font = None
    new_score = None
    new_name = None
    scores = None

    def __init__(self, new_name, new_score):
        self.score = 0
        self.font = pygame.font.SysFont("monospace", 15)
        self.new_score = int(new_score) 
        self.new_name = new_name 

        if not os.path.isfile(self.FILE_NAME):
            self.on_empty_file()

    def on_empty_file(self):
        empty_score_file = open(self.FILE_NAME,"w")
        empty_score_file.write("[]")
        empty_score_file.close()

    def save_score(self):
        if not self.scores == None:
            new_json_score = {
                    "score":self.new_score,
                    "name":self.new_name
                    }

            self.scores.append(new_json_score)

            self.scores = sorted(self.scores, key = lambda k: k["score"], reverse = True)

            highscore_file = open(self.FILE_NAME, "r+")
            highscore_file.write(json.dumps(self.scores))
        else:
            self.load_previous_scores()
            self.save_score()

    def load_previous_scores(self):
        with open(self.FILE_NAME) as highscore_file:
           self.scores = json.load(highscore_file)
           self.scores = self.scores