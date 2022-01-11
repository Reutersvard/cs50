#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //Get user name and greet
    string name = get_string("What is your name?\n");
    printf("hello, %s\n", name);
}