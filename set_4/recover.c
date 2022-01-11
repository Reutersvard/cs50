#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Check usage
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Open valid file to read
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Could not open %s.\n", argv[1]);
        return 1;
    }

    BYTE bytes[512];
    int img_counter = 0;
    char filename[8];
    FILE *img;


    // Start reading the file
    while (true)
    {
        int bytes_read = fread(bytes, sizeof(BYTE), 512, file);
        if (bytes_read == 0)
        {
            break;
        }

        // Check if file is a valid JPEG
        if (bytes[0] == 0xff && bytes[1] == 0xd8 && bytes[2] == 0xff && (bytes[3] & 0xf0) == 0xe0)
        {
            // Close already open JPEGs
            if (img_counter != 0)
            {
                fclose(img);
            }

            // Populate filename string, open new file and write into it
            sprintf(filename, "%03i.jpg", img_counter);
            img = fopen(filename, "w");
            fwrite(bytes, sizeof(BYTE), bytes_read, img);
            img_counter++;
        }

        // Keep writing into existing file
        else
        {
            if (img_counter != 0)
            {
                fwrite(bytes, sizeof(BYTE), bytes_read, img);
            }
        }
    }
    fclose(img);
    fclose(file);
    return 0;
}