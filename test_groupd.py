import sys

from spinner import find_best_groups
from spinner import get_file_input

def main():
    students = get_file_input(sys.argv[1])
    number_of_groups = 5

    work_well_together = [
        ('Liam', 'Emma'),
        ('Noah', 'Olivia'),
        ('Oliver', 'Amerlia'),
        ('James', 'Sophia'),

    ]
    do_not_work_well_together = [
        ('Lucas', 'Charlotte'),
        ('Mateo', 'Mia'),
        ('Benjamin', 'Harper'),
        ('Elias', 'Isabella'),

    ]

    test_iterations(students, number_of_groups, work_well_together, do_not_work_well_together)

def test_iterations(students, number_of_groups, work_well_together, do_not_work_well_together):
    score = float('inf')
    iteration = 0

    for i in range(0, 10000, 100):
        group, current_score = find_best_groups(i, students, number_of_groups, work_well_together, do_not_work_well_together)
        if current_score < score:
            score = current_score
            iteration = i

        if score == 0:
            print(iteration, score)
            break

    print(iteration, score)


# def test_punishments():

if __name__ == '__main__':
    main()
