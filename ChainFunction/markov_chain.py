import random
import pickle


def random_numeral():
    return random.choice(["II", "III", "IV", "V"])


def random_greek():
    return random.choice(["Alpha", "Beta", "Gamma", "Delta", "Epsilon"])


class MarkovChain:
    def __init__(self):
        self.chain = {"_start": [], "_end": []}

    def add_text(self, text):
        from nltk import word_tokenize
        from nltk.corpus import brown

        vocab = set(brown.words())
        sentences = text.lower().split(".")
        for sentence in sentences:
            for word in word_tokenize(sentence):
                if word not in vocab and word.find("-") < 0 and word.find("_") < 0:
                    self.add_word(word)

    def add_word(self, word):
        from nltk.tokenize import SyllableTokenizer

        SSP = SyllableTokenizer()
        syllables = SSP.tokenize(word)

        i = 0
        while i < len(syllables) - 1:
            syllable = syllables[i]
            if i == 0:
                start_words = self.chain.get("_start")
                start_words.append(syllable)
            syllable_after = "_end"
            if i < len(syllables) - 1:
                syllable_after = syllables[i + 1]
            if syllable not in self.chain:
                self.chain[syllable] = []
            self.chain[syllable].append(syllable_after)
            i += 1

    def roll_dice(self, num_dice):
        for _ in range(2, num_dice):
            if random.randint(0, 6) == 1:
                return True
        return False

    def generate_word(self, max_syllables=5):
        new_word = []

        # Select the first bigram
        start_syllable = random.choice(self.chain.get("_start"))
        new_word.append(start_syllable)

        # Keep looping through the syllables until we
        # can't come up with another word or each an "end" marker
        prev_syllable = start_syllable
        new_syllable = ""
        num_forks = 0
        while True:
            new_syllables = self.chain.get(prev_syllable)
            if (
                new_syllables is None
                or self.roll_dice(len(new_word))
                or len(new_word) >= max_syllables
            ):
                break
            if len(new_syllables) > 1:
                num_forks += 1
            new_syllable = random.choice(new_syllables)
            if new_syllable == "_end":
                break
            new_word.append(new_syllable)
            prev_syllable = new_syllable

        return "".join(new_word).capitalize()

    def generate_planet(self, seed=None, force_numeral=False, force_greek=False, **kwargs):
        random.seed(seed)
        planet = self.generate_word(**kwargs)
        if force_greek or (len(planet) <= 12 and random.randint(0, 100) < 10):
            planet = random_greek() + " " + planet
        if force_numeral or random.randint(0, 100) < 8:
            planet += " " + random_numeral()
        return planet

    def save_to_disk(self, filename):
        with open(filename, "wb") as handle:
            pickle.dump(self.chain, handle)

    def load_from_disk(self, filename):
        with open(filename, "rb") as handle:
            self.chain = pickle.loads(handle.read())
