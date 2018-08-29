// Resize a picture by a factor of f (float)
// Pretty much is copied and pasted from copy.c

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // Ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize n infile outfile\n");
        return 1;
    }

    // Remember inputs from command-line arguments
    float f = atoi(argv[1]);
    char *infile = argv[2];
    char *outfile = argv[3];

    // Open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // Open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // Read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // Read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // Ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // ==========
    // Temp variables for input file
    LONG tempWidth = bi.biWidth;

    // Padding for input file
    int paddingIn = (4 - (tempWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // Width and height times n
    bi.biWidth *= n;
    bi.biHeight *= n;

    // Padding for output file
    int paddingOut = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // Output image size
    bi.biSizeImage = ((sizeof(RGBTRIPLE) * bi.biWidth) + paddingOut) * abs(bi.biHeight);

    // Total bitmap size
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // Write the headers, order is very important, file then info because of pointer
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // ==========
    // Counter used for height
    int counter = 0;

    // Iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        // Iterate over pixels in scanline
        for (int j = 0; j < tempWidth; j++)
        {
            // Temporary storage
            RGBTRIPLE triple;

            // Read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

            for (int k = 0; k < n; k++)
            {
                // Write RGB triple to outfile
                fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
            }
        }

        // Add padding
        for (int k = 0; k < paddingOut; k++)
        {
            fputc(0x00, outptr);
        }

        // Push back the file pointer if not yet reaching n times
        if (++counter < n)
        {
            fseek(inptr, -(sizeof(RGBTRIPLE) * tempWidth), SEEK_CUR);
        }
        else
        {
            // Skip over padding, if any
            fseek(inptr, paddingIn, SEEK_CUR);

            // Reset the counter
            counter = 0;
        }
    }

    // Close infile
    fclose(inptr);

    // Close outfile
    fclose(outptr);

    // Success
    return 0;
}
