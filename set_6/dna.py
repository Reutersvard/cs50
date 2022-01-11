import sys
import csv


def main():

    people = {}  # Where {name: list of STR counts}

    # Check for correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: dna.py data.csv sequence.txt")
        sys.exit(1)

    # Open csv file and read contents into the STR_list list and people dictionary
    with open(sys.argv[1], "r") as csvfile:
        reader = csv.reader(csvfile)
        STR_list = next(reader)
        STR_list.pop(0)
        for row in reader:
            people[row[0]] = [int(x) for x in row[1:]]

    # Read the DNA sequence from the file into a string
    with open(sys.argv[2], "r") as textfile:
        sequence = textfile.read()

    STR_counts = STR_counter(STR_list, sequence)
    printer(STR_counts, people)
    sys.exit(0)


def STR_counter(STR_list, sequence):

    # A list with all the counts (initially 0) for repeats in order specified by STR_list
    STR_counts = [0 for i in range(len(STR_list))]

    for STR in range(len(STR_list)):  # Iterate through STRs
        STR_length = len(STR_list[STR])
        max_counter = 0
        counter = 0
        i = 0
        while i < len(sequence):
            if STR_list[STR] in sequence[i:i + STR_length]:  # Look for the STR in a moving slice of the sequence
                counter += 1
                i += STR_length
                if counter > max_counter:  # If a new max is reached, pop the previous value and insert the new one
                    max_counter = counter
                    STR_counts.pop(STR)
                    STR_counts.insert(STR, max_counter)
            else:  # When the STR is not found in the moving slice, reset counter and move 1 instead of a whole slice
                counter = 0
                i += 1

    return STR_counts


def printer(STR_counts, people):

    name = "No match"
    for person in people:
        if people[person] == STR_counts:    # Compare the counts for each STR to the ones in the people dict
            name = person

     # Print match name, or no match
    print(name)


main()