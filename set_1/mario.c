#include<stdio.h>
#include<cs50.h>

int get_height(void);

//Generates a pyramid of height n.
int main(void)
{
    int n = get_height();
    for (int i = 0; i < n; i++)
    {
        //This prints n spaces minus number of rows.
        for (int j = 0; j < n - i - 1; j++)
        {
            printf(" ");
        }
        for (int k = 0; k <= i; k++)
        {
            printf("#");
        }
        //The gap between.
        printf("  ");
        for (int k = 0; k <= i; k++)
        {
            printf("#");
        }
        printf("\n");
    }
}

//Gets an integer between 1 and 8 from the user to be the height of the pyramid.
int get_height(void)
{
    int n;
    do
    {
        n = get_int("Height:");
    }
    while (n < 1 || n > 8);
    return n;
}