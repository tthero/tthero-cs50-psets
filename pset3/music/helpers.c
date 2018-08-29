// Helper functions for music
#include "helpers.h"

// Notes in an octave, MAJOR_C as the starting point
const string NOTE[] = {"C", "C#", "D", "D#", "E", "F",
                       "F#", "G", "G#", "A", "A#", "B"
                      };
#define MAJOR_C -9;

// Default octave
#define DEF_OCTAVE 4

// Eighth
#define EIGHTH 8

// MAJOR_A frequency
const int MAJOR_A_FREQ = 440;

// Macro
#define EXTRACT_INT(str) atoi(strtok(str, "/"))

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    // X = numerator, Y = denominator
    int X = EXTRACT_INT(fraction);
    int Y = EXTRACT_INT(NULL);
    return X * EIGHTH / Y;
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    // Formula: f = (2^(n/12))*440
    // (a) note = XY
    // X = note (A to H)
    // Y = octave (0 to unlimited?)
    // (b) note = XYZ
    // X = note (A to H)
    // Y = sharp or flat (# or b)
    // Z = octave (0 to unlimited?)
    int noteSize = sizeof NOTE / sizeof NOTE[0];
    int noteLength = strlen(note);
    int diffNotes = 0, diffOctave = 0;

    // malloc and calloc are different, calloc can preset memory allocated to zero, while malloc cannot
    string temp = (string)calloc(noteLength, sizeof(char));

    if (noteLength == 2)
    {
        // For XY, Y (note[1]) is octave
        strncpy(temp, note, 1);
        diffOctave = noteSize * (note[1] - '0' - DEF_OCTAVE);
    }
    else if (noteLength == 3)
    {
        // For XYZ, XY (note[0] to [1])
        strncpy(temp, note, 2);
        diffOctave = noteSize * (note[2] - '0' - DEF_OCTAVE);
    }

    for (int i = 0; i < noteSize; i++)
    {
        // Detects for flat
        if (note[1] == 'b')
        {
            temp[1] = '\0';
            if (strcmp(temp, NOTE[i]) == 0)
            {
                diffNotes = i - 1 + MAJOR_C;
                break;
            }
        }
        else if (strcmp(temp, NOTE[i]) == 0)
        {
            diffNotes = i + MAJOR_C;
            break;
        }
    }

    // Free the temp memory for future use
    free(temp);
    return (int)(round(pow(2, (diffOctave + diffNotes) / (double)noteSize) * MAJOR_A_FREQ));
}

// Determines whether a string represents a rest
// Empty string
bool is_rest(string s)
{
    return strcmp(s, "") == 0;
}