#include <stdio.h>
#include <cs50.h>
#include <math.h>
#include <ctype.h>
#include <string.h>

string get_text(void);
int word_count(string text);
int sentence_count(string text);
int letter_count(string text);
double get_L(int words, int letters);
double get_S(int words, int sentences);


// Given a text, the function prints its readability grade according to the Coleman-Liau index.
int main(void)
{
    string text = get_text();
    int words = word_count(text), letters = letter_count(text), sentences = sentence_count(text);
    double L =  get_L(words, letters), S = get_S(words, sentences);
    double index = 0.0588 * L - 0.296 * S - 15.8;
    if (index >= 1 && index <= 16)
    {
        printf("Grade %i\n", (int) round(index));
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade 16+\n");
    }
}

// Promts the user for a text.
string get_text(void)
{
    string text = get_string("Text: ");
    return text;
}

// Counts the number of words in a text.
int word_count(string text)
{
    int words = 0, n = strlen(text);
    for (int i = 0; i < n; i++)
    {
        if (isspace(text[i]))
        {
            words++;
        }
    }
    return words += 1;
}

// Counts the number of sentences in a text.
int sentence_count(string text)
{
    int sentences = 0, n = strlen(text);
    for (int i = 0; i < n; i++)
    {
        if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            sentences++;
        }
    }
    return sentences;
}

// Counts the number of letters in a text.
int letter_count(string text)
{
    int letters = 0, n = strlen(text);
    for (int i = 0; i < n; i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
    }
    return letters;
}

// Calculates the average number of letters per 100 words in a text.
double get_L(int words, int letters)
{
    double dwords = (double) words, dletters = (double) letters;
    double L = dletters / dwords * 100;
    return L;
}

// Calculates the average number of sentences per 100 words in a text.
double get_S(int words, int sentences)
{
    double dwords = (double) words, dsentences = (double) sentences;
    double S = dsentences / dwords * 100;
    return S;
}