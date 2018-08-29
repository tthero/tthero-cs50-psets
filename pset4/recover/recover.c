// Recover various image (JPEG files) from a raw file

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Defining a constant for block size of 512 bytes on FAT file system
#define BLOCK_SIZE 512

int main(int argc, char *argv[])
{
    // If argument count is not 2, return error 1
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    // Read the raw file
    char *infile = argv[1];
    FILE *rawPtr = fopen(infile, "r");

    // If the file does not exist, return error 2
    if (rawPtr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // Allocate for how long the filename should be
    char *out = malloc(strlen("000.jpg"));

    // For the buffer, the data type has to be 8 bit = 1 byte, thus char data type is used
    // However, unsigned char is used instead of char because of signedness, it holds a
    // range of -128 to 127, and thus 0xff is not 256 but most likely -128
    // Ref: https://stackoverflow.com/a/34418193/9494932
    unsigned char *buffer = malloc(BLOCK_SIZE);

    // Declares the file pointer
    FILE *outputFile = NULL;

    // Used for counter in filename
    int counter = 0;

    // Reading 512 bytes into buffer and check if it reads 512 bytes or not
    while (fread(buffer, 1, BLOCK_SIZE, rawPtr) == BLOCK_SIZE)
    {
        // Recognising JPEG header
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff /*
        */ && (buffer[3] & 0xf0) == 0xe0)
        {
            // Closes existing JPEG file
            if (outputFile != NULL)
            {
                fclose(outputFile);
            }

            // Opens new JPEG file start from 000.jpg
            sprintf(out, "%03d.jpg", counter++);
            outputFile = fopen(out, "w");
        }

        // Write all the data from the buffer into the output file
        if (outputFile != NULL)
        {
            fwrite(buffer, 1, BLOCK_SIZE, outputFile);
        }
    }

    // Afraid that there will be segmentation fault
    if (outputFile != NULL)
    {
        fclose(outputFile);
    }
    fclose(rawPtr);

    // After malloc, free them
    free(out);
    free(buffer);

    // Success
    return 0;
}