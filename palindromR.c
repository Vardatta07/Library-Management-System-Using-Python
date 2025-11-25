#include <stdio.h>
#include <string.h>

int main()
{
    char word1[100], word2[100];
    int len;
    int num, n, revnum = 0;

    // Word palindrome
    printf("Enter a word: ");
    scanf("%s", word1);

    strcpy(word2, word1);
    
    // Reverse the word manually
    len = strlen(word1);
    for (int i = 0; i < len; i++) {
        word2[i] = word1[len - 1 - i];
    }
    word2[len] = '\0';

    printf("Given word: %s\n", word1);
    printf("Reversed word: %s\n", word2);

    if (strcmp(word1, word2) == 0)
        printf("The word is a palindrome.\n");
    else
        printf("The word is NOT a palindrome.\n");

    // Number palindrome
    printf("\nEnter a 5-digit number: ");
    scanf("%d", &num);

    n = num;

    while (n > 0) {
        revnum = revnum * 10 + (n % 10);
        n /= 10;
    }

    printf("Given number: %d\n", num);
    printf("Reversed number: %d\n", revnum);

    if (num == revnum)
        printf("The number is a palindrome.\n");
    else
        printf("The number is NOT a palindrome.\n");

    return 0;
}
