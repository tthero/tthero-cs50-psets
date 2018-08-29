# Questions

## What's `stdint.h`?

`stdint.h` is a header/library which allows users to have typedefs of specified (exact) width integer types and macros definitions involving min and max allowable values for each type defined in other standard headers.

Ref: http://pubs.opengroup.org/onlinepubs/009695399/basedefs/stdint.h.html

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

Because there are various architectures which can have different sizes of int and long, thus with these data types, say `uint8_t`, it will give exactly 8-bit unsigned integer data type.

Ref: http://pubs.opengroup.org/onlinepubs/009695399/basedefs/stdint.h.html

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

`BYTE` = 8 bits = 1 byte <br>
`DWORD` = 32 bits = 4 byte <br>
`LONG` = 32 bits = 4 byte <br>
`WORD` = 16 bits = 2 byte

Ref: http://pubs.opengroup.org/onlinepubs/009695399/basedefs/stdint.h.html

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

*First 2 bytes:*<br>
Hexadecimal: **0x42 0x4D**<br>
ASCII: **BM**

Ref: https://filesignatures.net/index.php?search=BMP&mode=EXT

## What's the difference between `bfSize` and `biSize`?

`bfSize` is the file size of the bitmap. <br>
`biSize` is the size of structure in info header of bitmap, e.g. 40 bytes for 24-bit bitmap, 108 bytes for 32-bit bitmap.

Ref (1): https://msdn.microsoft.com/en-us/library/dd183374.aspx<br>
Ref (2): https://msdn.microsoft.com/en-us/library/dd183376.aspx

## What does it mean if `biHeight` is negative?

If `biHeight` is negative, the bitmap is top-down device-independent bitmap (DIB) and its origin is the upper-left corner, which allows compression for that bitmap. However, positive `biHeight` which indicates bottom-up DIB, cannot allow compression.

Ref: https://msdn.microsoft.com/en-us/library/dd183376.aspx

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

`biBitCount` indicates the number of bits per pixel.

Ref: https://msdn.microsoft.com/en-us/library/dd183376.aspx

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

According to [JaredPar](https://stackoverflow.com/a/5987842/9494932) in StackOverflow, `fopen` fails to write or read and thus returns `NULL` if:

> 1) The file doesn't exist
> 2) The file is opened in a mode that doesn't allow other accesses
> 3) The network is down
> 4) The file exists, but you don't have permissions
> 5) A file exists with the name you gave, but the current directory of the process is not what you expected so the relative pathname fails to find and open the file.

## Why is the third argument to `fread` always `1` in our code?

`fread` third argument is to input the number of members to be used for verification with the output of elements by `fread`. Thus, unless there are various elements in the output to be verified, `fread` will just suffice to take `1` in the third argument. In our code, since mostly we only need the info 1 time, hence the third argument `1` in the `fread`.

Ref: https://www.tutorialspoint.com/c_standard_library/c_function_fread.htm

## What value does line 63 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

In line 63 of `copy.c`,
```c
int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
```
`padding` variable returns `3` after enormous mathematical operations since `sizeof(RGBTRIPLE)` is 3 due to having 3 members of 1 byte inside the struct:
```c
typedef struct
{
    BYTE rgbtBlue;
    BYTE rgbtGreen;
    BYTE rgbtRed;
} __attribute__((__packed__))
RGBTRIPLE;
```

## What does `fseek` do?

According to [CS50 reference](https://reference.cs50.net/stdio/fseek),
```c
#include <stdio.h>
int fseek(FILE* fp, long int offset, int from_where);
```
`fseek` sets the file pointer `fp` to the position with displacement `offset` from the location `from_where`. To put it in analogy to our notepad, the file pointer will be the cursor, trying to shift it by `offset` from the location `from_where`.

Ref (1): https://reference.cs50.net/stdio/fseek <br>
Ref (2): https://www.tutorialspoint.com/c_standard_library/c_function_fseek.htm

## What is `SEEK_CUR`?

```c
#include <stdio.h>
int fseek(FILE* fp, long int offset, int from_where);
```
In `fseek`, there are 3 constants for the argument `from_where`, namely `SEEK_SET`, `SEEK_CUR` and `SEEK_END`. `SEEK_CUR` will be the current position of the file pointer `fp`.

Ref (1): https://reference.cs50.net/stdio/fseek <br>
Ref (2): https://www.tutorialspoint.com/c_standard_library/c_function_fseek.htm
