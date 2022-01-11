#include <stdio.h>
#include <cs50.h>
#include <math.h>

int get_change(void);

//Prints number of coins needed to give the change. Each while loop subtracts the coin value and adds one to the coin counter.
int main(void)
{
    int change = get_change();
    int coins = 0;
    while (change >= 25)
    {
        change = change - 25;
        coins++;
    }
    while (change >= 10)
    {
        change = change - 10;
        coins++;
    }
    while (change >= 5)
    {
        change = change - 5;
        coins++;
    }
    while (change >= 1)
    {
        change = change - 1;
        coins++;
    }
    //This prints the total number of coins in the end.
    printf("%i\n", coins);
}

//Prompts user for a positive number of dollars and converts it into cents.
int get_change(void)
{
    float dollars;
    do
    {
        dollars = get_float("How much change is it owed?: ");
    }
    while (dollars <= 0);
    int change = round(dollars * 100);
    return change;
}

// Another solution would be to use a for loop and modulo operators.
