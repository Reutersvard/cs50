#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float Average = (image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0;
            int rgbtAverage = round(Average);

            image[i][j].rgbtRed = rgbtAverage;
            image[i][j].rgbtGreen = rgbtAverage;
            image[i][j].rgbtBlue = rgbtAverage;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            int sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            int sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);

            image[i][j].rgbtRed = sepiaRed;
            if (sepiaRed > 255)
            {
                image[i][j].rgbtRed = 255;
            }

            image[i][j].rgbtGreen = sepiaGreen;
            if (sepiaGreen > 255)
            {
                image[i][j].rgbtGreen = 255;
            }

            image[i][j].rgbtBlue = sepiaBlue;
            if (sepiaBlue > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            int originalRed = image[i][j].rgbtRed;
            int originalGreen = image[i][j].rgbtGreen;
            int originalBlue = image[i][j].rgbtBlue;

            image[i][j].rgbtRed = image[i][width - j - 1].rgbtRed;
            image[i][j].rgbtGreen = image[i][width - j - 1].rgbtGreen;
            image[i][j].rgbtBlue =  image[i][width - j - 1].rgbtBlue;

            image[i][width - j - 1].rgbtRed = originalRed;
            image[i][width - j - 1].rgbtGreen = originalGreen;
            image[i][width - j - 1].rgbtBlue = originalBlue;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE original[height][width];

    // This makes a copy of the original image to work with.
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            original[i][j].rgbtRed = image[i][j].rgbtRed;
            original[i][j].rgbtGreen = image[i][j].rgbtGreen;
            original[i][j].rgbtBlue = image[i][j].rgbtBlue;
        }
    }

    // Here starts the main loop that blurs the pixels.
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sumRed = 0;
            int sumGreen = 0;
            int sumBlue = 0;
            float counter = 0.0;

            //This sums all the pixel's RGB values around the target one.
            for (int k = - 1; k < 2; k++)
            {
                for (int l = - 1; l < 2; l++)
                {
                    if ((i + k) < 0 || (j + l) < 0 || (i + k) > height - 1 || (j + l) > width - 1)
                    {
                        continue;
                    }

                    sumRed += original[i + k][j + l].rgbtRed;
                    sumGreen += original[i + k][j + l].rgbtGreen;
                    sumBlue += original[i + k][j + l].rgbtBlue;
                    counter ++;
                }
            }

            int averageRed = round(sumRed / counter);
            int averageGreen = round(sumGreen / counter);
            int averageBlue = round(sumBlue / counter);

            image[i][j].rgbtRed = averageRed;
            image[i][j].rgbtGreen = averageGreen;
            image[i][j].rgbtBlue = averageBlue;
        }
    }

    return;
}