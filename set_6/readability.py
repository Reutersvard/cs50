from cs50 import get_string

# These one liners get the text from the user and initialise the counters
text = get_string("Text: ")
words = 1
sentences = 0
letters = 0

# This loop counts the variables used later in the formula
for char in text:

    if char.isspace():
        words += 1

    if char.isalpha():
        letters += 1

    if char in ['.', '?', '!']:
        sentences += 1

# The average number of letters (L) and sentences (S) per 100 words in the text. This is used to calculate the Coleman-Liau index
S = float(sentences) / words * 100
L = float(letters) / words * 100
index = 0.0588 * L - 0.296 * S - 15.8

# This takes the index and prints the final output
if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {round(index)}")
