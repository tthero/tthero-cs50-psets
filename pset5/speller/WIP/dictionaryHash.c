// Implements a dictionary's functionality
// Many ways to store the dictionary words: Hashtable, array, trie
// Below is trie method

#include "dictionary.h"
#include "MurmurHash3.h"

// ====== TRIE ======
typedef struct trie_node
{
    bool is_word;
    struct trie_node *next[ALPHASTROPHE];
}
node;

// Used throughout this file only (global only to this file)
// Static keyword is used to ensure this
static node *root;
static unsigned int counter = 0;

// Construct a new node (giving birth of children)
node *createNode()
{
    node *temp = NULL;

    // May be the real problem of all?
    temp = malloc(sizeof(node));

    if (temp)
    {
        temp->is_word = false;

        // Memset is writing the memory with how many bytes
        memset(temp->next, 0, sizeof(temp->next));
    }
    return temp;
}

// Data entry
bool insertWord(char *word)
{
    node *trav = root;

    // Char by char, go to the node with the word as index, if NULL, construct new node
    for (int i = 0; word[i] != '\0'; i++)
    {
        // Alphabets and apostrophe
        int index = isalpha(word[i]) ? word[i] - 'a' : ALPHASTROPHE - 1;

        // If the children are NULL
        if (!trav->next[index])
        {
            trav->next[index] = createNode();

            // Not enough space
            if (!trav->next[index])
            {
                return false;
            }
            trav->next[index]->is_word = false;
        }
        trav = trav->next[index];
    }

    trav->is_word = true;
    counter++;
    return true;
}

// Prefix word search concept
bool searchWord(const char *word)
{
    node *trav = root;

    if (root)
    {
        // Char by char, go to the node with the word as index, if NULL, construct new node
        for (int i = 0; word[i] != '\0'; i++)
        {
            int index = isalpha(word[i]) ? tolower(word[i]) - 'a' : ALPHASTROPHE - 1;

            // If the children are NULL
            if (!trav->next[index])
            {
                return false;
            }
            trav = trav->next[index];
        }

        if (trav->is_word)
        {
            return true;
        }
    }
    return false;
}

// Free the memory
void freeTrie(node *trav)
{
    // Use the concept of recursion to go deeper the children of node in trie
    if (trav)
    {
        for (int i = 0; i < ALPHASTROPHE; i++)
        {
            freeTrie(trav->next[i]);
        }
        free(trav);
    }
}
// ==================

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    return searchWord(word);
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Fopen the dictionary first
    FILE *file_dict = fopen(dictionary, "r");
    if (file_dict == NULL)
    {
        return false;
    }

    // If dictionary exists, read the word through fscanf?
    // Create root of trie
    root = createNode();

    char word[LENGTH + 1];

    while (fscanf(file_dict, "%s", word) != EOF)
    {
        if (!insertWord(word))
        {
            unload();
            fclose(file_dict);
            return false;
        }
    }

    fclose(file_dict);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return counter;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    if (root)
    {
        freeTrie(root);
        return true;
    }
    return false;
}