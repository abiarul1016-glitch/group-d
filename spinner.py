import random
import sys


def main():

    # Error checking
    if len(sys.argv) != 2:
        sys.exit('Input filename of textfile with list of students names.')

    # Ask for name of each kid in the class, should be able to be inputted from textfile
    students = get_file_input(sys.argv[1])
    print(students)

    # Ask user to input number of students in the class
    # number_of_students = input('How many students are in the class?: ')
    # number_of_students = len(students)

    # Ask input for number of groups needed or range of people in each group
    while True:
        number_of_groups = get_number_of_groups('How many groups are needed?: ')
        if number_of_groups > 0:
            break
        # Program might have to be able to autocalculate these values

    # Ask for pairs of people who like to work to together
    pairs_together = get_number_of_groups('How many pairs want to work together?: ')
    work_well_together = get_constrained_groups(
        'Who works well together? (Input as Name 1, Name 2): ',
        pairs_together
    )

    # Print newline for aesthetics
    print()

    # Ask teacher to input people they know do not work well together
    pairs_not_together = get_number_of_groups('How many pairs DO NOT want to work together?: ')

    do_not_work_well_together = get_constrained_groups(
        'Who does not work well together? (Input as Name 1, Name 2): ',
        pairs_not_together
    )

    print()
    print(find_best_groups(10000, students, number_of_groups, work_well_together, do_not_work_well_together))


# Group creating algorithm, takes in input of how many times the group generating algorithm needs to run
def find_best_groups(iterations, students, number_of_groups, together_pairs, not_together_pairs):
    # Set intial best score to positive infinity, so first output is always lower
    best_score = float('inf')
    # Set best_permutation to None
    best_assignment = None

    # First random group algorithm
    # Might have to purposely rig the sort of the list, to ensure proper distribution and weighting
    for _ in range(iterations):
        random.shuffle(students)

        current_groups = [[] for _ in range(number_of_groups)]

        for i, student in enumerate(students):
            current_groups[i % number_of_groups].append(student)

        # Get score of current group
        current_score = get_score(current_groups, together_pairs, not_together_pairs)

        # Update the groups till the group with the lowest score
        # Check if this is the lowest score
        if current_score < best_score:
            best_score = current_score
            best_assignment = current_groups

        # If it already acheived 0, immediately exit the program and return this group
        if best_score == 0:
            break

    # Output list of groups
    return best_assignment, best_score


# Now using machine learning, and some scoring logic, optimize the groups as much as possible
# Assign a score for each output the random algorithm provides for 1000 iterations
# Punish the outcomes with not_together more harshly than together
def get_score(groups, together_pairs, not_together_pairs):
    score = 0
    for group in groups:
        # Together pairs reward
        for p1, p2 in together_pairs:
            if (p1 in group) ^ (p2 in group):
                score += 10

        # Not together pairs punishment
        for p1, p2 in not_together_pairs:
            if p1 and p2 in group:
                # Heavier punishment for keeping two individuals together,
                # as its better to have two kids who don't work well together apart
                score += 50

    return score


def get_file_input(filename):
    with open(filename) as file:
        file_values = [line.rstrip() for line in file]
    return (file_values)


def get_number_of_groups(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print('Please enter an integer')


def get_constrained_groups(prompt, number_of_pairs):
    groups = []

    for _ in range(number_of_pairs):
        pair = input(prompt).split(', ')
        groups.append(tuple(pair))
    return groups


if __name__ == '__main__':
    main()
