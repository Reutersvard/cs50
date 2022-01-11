card_number = input("Number: ")


def main():
    # Check if number is valid, i.e. right length and passes checksum
    if len(card_number) in [13, 15, 16] and checksum() == 0:
        
        if card_number[0:2] in ['34', '37']:
            print("AMEX")
            
        elif card_number[0] == '4':
            print("VISA")
            
        elif card_number[0:2] in ['51', '52', '53', '54', '55']:
            print("MASTERCARD")
            
        else:
            print("INVALID")
        
    else:
        print("INVALID")


# Returns the checksum value
def checksum():
    # Two lists, one with the even numbers (starting from the last one) multplied by 2, one with the odd numbers
    evens = [int(card_number[digit])*2 for digit in range(len(card_number) - 2, -1, -2)]
    odds = [int(card_number[digit]) for digit in range(len(card_number) - 1, -1, -2)]

    # Converts every number in evens into the sum of its digits, e.g. 12 becomes 1 + 2 = 3
    evens = [(number // 10 + number % 10) for number in evens]

    return (sum(odds) + sum(evens)) % 10


main()