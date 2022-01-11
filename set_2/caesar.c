#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

//Function declarations
string get_text(void);

//Main
int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Error: expected exactly one command line argument.\n");
        return 1;
    }
    int key_length = strlen(argv[1]);
    for (int i = 0; i < key_length; i++)
    {
        if (isdigit(argv[1][i]) == false)
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    int key = atoi(argv[1]); // Converts key from string to int.
    string text = get_text();
    printf("ciphertext: ");
    
    // Iterates over the plain text provided by the user and prints every alphabetic char according to key.
    int text_length = strlen(text);
    for (int i = 0; i < text_length; i++)
    {
        if (isalpha(text[i])) 
        {
            if (islower(text[i]))
            {
                // Take the ith char, shift it to 0 from its ASCII position, make it rotate according to the key, shift it back.
                char cipher_char = (((text[i] - 97) + key) % 26) + 97;
                printf("%c", cipher_char);
            }
            if (isupper(text[i]))
            {
                char cipher_char = (((text[i] - 65) + key) % 26) + 65;
                printf("%c", cipher_char);
            }
        }
        else
        {
            printf("%c", text[i]);
        }
    }
    printf("\n");
    return 0;
}

//Prompt user for a string of text.
string get_text(void)
{
    string text = get_string("Plaintext: ");
    return text;
}