# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?

**Pneumonoultramicroscopicsilicovolcanoconiosis** means a lung disease due to inhalation of very fine volcanic dust and ash particles. <br>
What is this word... Help me...

Ref: https://en.oxforddictionaries.com/definition/Pneumonoultramicroscopicsilicovolcanoconiosis

## According to its man page, what does `getrusage` do?

From **SYNOPSIS**,
```c
#include <sys/time.h>
#include <sys/resource.h>

int getrusage(int who, struct rusage *usage);
```
`getrusage` serves to return resource usage measures on the `struct rusage *usage` for input of `int who`. The `int who` can take the following constants: `RUSAGE_SELF`, `RUSAGE_CHILDREN` and `RUSAGE_THREAD` to return resource usage measures for what type.

## Per that same man page, how many members are in a variable of type `struct rusage`?

From **DESCRIPTION**,

There are 16 members in the `struct rusage`.
```c
struct rusage{
        struct timeval ru_utime; /* user CPU time used */
        struct timeval ru_stime; /* system CPU time used */
        long   ru_maxrss;        /* maximum resident set size */
        long   ru_ixrss;         /* integral shared memory size */
        long   ru_idrss;         /* integral unshared data size */
        long   ru_isrss;         /* integral unshared stack size */
        long   ru_minflt;        /* page reclaims (soft page faults) */
        long   ru_majflt;        /* page faults (hard page faults) */
        long   ru_nswap;         /* swaps */
        long   ru_inblock;       /* block input operations */
        long   ru_oublock;       /* block output operations */
        long   ru_msgsnd;        /* IPC messages sent */
        long   ru_msgrcv;        /* IPC messages received */
        long   ru_nsignals;      /* signals received */
        long   ru_nvcsw;         /* voluntary context switches */
        long   ru_nivcsw;        /* involuntary context switches */
};
```

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?

Through the declaration and definition of `calculate`, its parameters takes pointers of `struct rusage` (namely `struct rusage *b` and `struct rusage *a`). Passing of `before` and `after` by reference is used because their addresses are required during the `calculate` operation to retrieve the required values precisely. If passing by value is used instead, its parameters will be treated like local variables in the `calculate` function where different addresses are issued or allocated for them. Thus, at lines 189 - 193 of `speller.c`, say `a->ru_utime.tv_sec`, it will either refer to NULL or garbage value.

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.

At first, the `main` will either take 2 or 3 command line arguments where it takes the text to be spell checked as required input, and optionally which dictionary to be used for loading the words through `load` function. <br>

Next, the main part of spell checker is in the `for` loop incorporating the `check` function. By using `fgetc` function, each word of the text file is checked by fetching all the characters of that word. Only the word made up of alphabets and apostrophe will be further processed. If the word contains digits, the whole word is skipped. The checkup of that word is finished when `fgetc` faces the next character other than alphabets, digits and apostrophe, like space, newline, #, $, % and so on. The `word[index]` is where an array of characters from `fgetc` will be appended on it. `index` is useful in keeping track of number of characters in a word and then forming a word, provided that the character is an alphabet or apostrophe.<br>

For example to explain the previous paragraph, there is an excerpt saying `"You n3rd! t#lmao's"`. Through `fgetc`, starting from the char `'Y'`, it is checked to see it fits the criterion of being an alphabet or apostrophe. `'Y'` is alphabet, thus the char is appended and stored in `word[index]`, then `index` is incremented by 1 for next char. The next char, `'o'`, is an alphabet as well, so, it is appended into `word[index]` before `index` is incremented by 1. Same goes for `'u'`. Until `fgetc` encounters a space char, it does not fit the criterion, so `'\0'` is appended into `word[index]` and `index` is reset to 0 to terminate the word, `"You"`. Next, `'n'` fulfills the criterion and appended into `word[index]` using the new `index`. However, `'3'`is a digit and thus subsequent alphabets and apostrophe will be skipped until char `'!'` is encountered. The whole word `"n3rd"` is thus ignored. Then, after the space char, `fgetc` encounters `'t'` and the process above is repeated. `'#'` is another char just like space char, thus ending the word with `'\0'` and finishing the word `"t"`. Finally, the process is repeated once again for the next few characters `'l'`, `'m'`, `'a'`, `'o'`. For apostrophe, it fits the criterion and thus is appended into `word[index]`. The word, `"lmao's"` is then finished after `'s'` and `'\0'` (when `fgetc` reads EOF). In between every word checking, they are passed to `check` function to return if they are misspelled or not according to dictionary from `load` function.

## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?

Based on my understanding, both `fgetc` and `fscanf` can be used to read words of a file. Somehow, using `fscanf` is performing additional work for processing during word checking. It is because after `fscanf`, a string or whole word is read and stored in `word[index]`. And in order to check if that word has digits and other characters or not, one will pass this word into another `for` loop to iterate through each character, e.g. the `index` of `word[index]` until it reaches `strlen` of that word. That is basically as same as using `fgetc` to achieve the same results but with more steps. <br>

Another drawback of using `fscanf` is it may cause buffer overflow. Based on this [answer](https://stackoverflow.com/a/1239970/9494932) from StackOverflow, if there is a word which can have more characters than defined size, say 50 characters in a word vs defined size of 46, odds are some of the stack addresses will be overwritten, causing undefined behaviour. If lucky, nothing bad will happen and the program will execute and exit normally. Else, either some of the variables will yield different results or program may end abruptly.

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?

In `check` and `load`, the parameters are `const char *word` and `const char *dictionary`, which are pointers. If these addresses are unintentionally altered, the access to their contents will be lost or orphaned. Thus, by making use of type qualifier `const`, those parameters will become read-only and do not allow any modification to their contents. Most of the time, `const` is used for pointers during prototyping (declaration of functions). For normal variables, `const` is redundant since copies of these variables are made within the function.

Ref: https://softwareengineering.stackexchange.com/a/204720