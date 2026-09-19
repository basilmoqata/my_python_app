text = input("Enter a sentence or paragraph: ")
num_characters = len(text)
words_list = text.split()
num_words = len(words_list)
num_sentences = text.count('.') + text.count('!') + text.count('?')
if num_sentences == 0 and len(text.strip()) > 0:
    num_sentences = 1
print("\n--- Results ---")
print(f"Number of characters: {num_characters}")
print(f"Number of words: {num_words}")
print(f"Number of sentences: {num_sentences}")