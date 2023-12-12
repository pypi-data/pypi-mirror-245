import re

def split_english_japanese(input_str):
    # Regular expression to match English sentences
    english_pattern = re.compile(r'[a-zA-Z.,!? ]+')

    # Regular expression to match Japanese sentences
    japanese_pattern = re.compile(r'[\u3000-\u303F\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF、。]+')

    # Find all English and Japanese sentences in the input string
    english_sentences = english_pattern.findall(input_str)
    japanese_sentences = japanese_pattern.findall(input_str)

    return english_sentences, japanese_sentences

input_str1 = "Insufficient amount is based on allocation trial. 担保不足時の額は充当前の額をベースに表示。"
input_str2 = "担保不足時の額は充当前の額をベースに表示。 Insufficient amount is based on allocation trial."

# Split input_str1
english_sentences_1, japanese_sentences_1 = split_english_japanese(input_str1)
print("English Sentences 1:", english_sentences_1)
print("Japanese Sentences 1:", japanese_sentences_1)

# Split input_str2
english_sentences_2, japanese_sentences_2 = split_english_japanese(input_str2)
print("\nEnglish Sentences 2:", english_sentences_2)
print("Japanese Sentences 2:", japanese_sentences_2)
