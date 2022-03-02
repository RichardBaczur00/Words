import pandas as pd
import random


def read_dataset():
    data = pd.read_csv('./data/words.csv')
    data['word'] = data.values.sum(axis=1)
    return pd.DataFrame(data['word'])

    
def choose_word(words):
    chosen_index = random.randint(0, len(words))
    return words.loc[chosen_index].values