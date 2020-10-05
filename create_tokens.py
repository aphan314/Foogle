import sys
import re
from collections import defaultdict

# reads input file
# adds each line to a list
# returns list
# if list is empty, the file is empty
# if unable to open file, file does not exist
# complexity: O(N) + O(1) + O(1) = O(N) <- total time complexity of the function
def read_file(file_name):
    try:
        line_list = []
        # O(N)
        for line in open(file_name):
            # O(1)
            line_list.append(line.rstrip('\n'))
        # O(1)
        if len(line_list) == 0:
            print("incorrect input: empty file")
            exit()
        return line_list
    except IOError:
        print("incorrect input: file does not exist")
        exit()

# tokenizes text
# iterates through each line in the file_list
# finds all tokens that match with the alphanumeric pattern
# adds the tokens to a list
# returns list
# complexity: O(N) + O(1) = O(N) <- total time complexity of the function
def tokenizer(file_list):
    token_list = []
    # O(N)
    for i in file_list:
        # O(1)
        token_list += re.findall('[a-zA-Z0-9]+', i)
    return token_list

# counts the number of occurrences
# iterates through a list of tokens
# adds each token into dictionary as a key
# the value of each key is the number of occurrences
# returns dictionary of tokens and number of occurrences
# complexity: O(N) + O(1) = O(N) <- total complexity of the function
def num_occurrences(t_list):
    token_dict = defaultdict(int)
    # O(N)
    for i in t_list:
        # O(1)
        token_dict[i.lower()] += 1
    return token_dict

# print out token and frequency
# iterates through a sorted list of (token, freq) tuples
# list is sorted by decreasing frequency
# if frequencies are the same, then list is sorted by alphabetical ascending order
# complexity: O(NlogN) <- total time complexity of the function
def frequency(token_count):
    # O(NlogN)
    for token,freq in sorted(token_count.items(), key=(lambda x: (-x[1],x[0]))):
        print(token + '\t' + str(freq))

# main that executes the functions
# checks for valid input
# complexity: O(N) + O(N) + O(N) + O(NlogN) = O(NlogN) <-total time complexity of program
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("incorrect input: more or less arguments given")
        exit()
    main_list = read_file(sys.argv[1])
    main_list = tokenizer(main_list)
    main_dict = num_occurrences(main_list)
    frequency(main_dict)

