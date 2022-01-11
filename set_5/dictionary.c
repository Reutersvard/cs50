// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include "dictionary.h"
#include <stdlib.h>
#include <strings.h>
#include <string.h>
#include <ctype.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 4000;

// Hash table with N linked lists or 'buckets', and the word count set to 0 until words are loaded
node *table[N];
int word_count = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int index = hash(word);
    node *cursor = table[index]; // Go to the head of the linked list

    while (cursor != NULL) // Loop the linked list looking for the word
    {
        if (strcasecmp(cursor -> word, word) == 0)
        {

            return true;
        }

        cursor = cursor -> next;
    }

    return false;
}

// Hashes word to a number, called "index" in the load function
unsigned int hash(const char *word)
{
    // The following hash function is taken from https://stackoverflow.com/questions/7700400/whats-a-good-hash-function-for-english-words
    unsigned long hash = 5381;
    int c;
    while ((c = tolower(*word++)))
    {
        hash = ((hash << 5) + hash) + c;
    }

    return hash % N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Open dictionary and check it's not an empty pointer
    FILE *file = fopen(dictionary, "r");
    if (file != NULL)
    {
        // Create an array to store words scanned from the dictionary file until EOF
        char scan_word[LENGTH + 1];
        int index;
        while (fscanf(file, "%s", scan_word) != EOF)
        {
            // Allocate memory for nodes and NULL check
            node *n = malloc(sizeof(node));
            if (n != NULL)
            {
                // Copy scanned word into node
                strcpy(n -> word, scan_word);
                // Hash the word to get the table index and increase global word count
                index = hash(scan_word);
                word_count++;
                // Point the node to the next one
                n -> next = table[index];
            }

            //Reset the first pointer
            table[index] = n;

        }

        fclose(file);
        return true;
    }

    return false;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++) // Iterate thorugh all the buckets
    {
        node *cursor = table[i]; // Go to the head of the linked list
        while (cursor != NULL) // Loop the linked list looking for the word
        {
            node *tmp = cursor;
            cursor = cursor -> next;
            free(tmp);
        }
    }

    return true;
}
