class ScoreSystem():
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.load_high_score()

    def add_score(self, points):
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

    def reset(self):
        self.score = 0
    
    def save_high_score(self):
        try:
            with open('highscore.dat', 'w') as file: # open file for writing
                file.write(str(self.high_score))
        except:
            print("Error saving high score")
    
    def load_high_score(self):
        try:
            with open('highscore.dat', 'r') as file: # open file for reading
                self.high_score = int(file.read())
        except:
            self.high_score = 0
            print("No high score file found, starting fresh")