from constraint import *
from crossword import *
import pygame
import sys

crossword = Crossword('structure1.txt', 'words1.txt')
problem = Problem()
pygame.init()

# Setting variables
variables = []
for var in crossword.variables:
    if var.length == 1:
        continue
    variables.append(str((var.i, var.j, var.direction, var.length)))

# Setting variables and domain
problem.addVariables(
    variables,
    crossword.words
)

# Setting constraints
constraints_1 = []
overlaps = crossword.overlaps.copy()
for combination in overlaps:
    var_1, var_2 = combination
    if not overlaps[combination] or var_1.length == 1 or var_2.length == 1:
        continue
    constraints_1.append((str((var_1.i, var_1.j, var_1.direction,
                               var_1.length)),
                          str((var_2.i, var_2.j, var_2.direction,
                               var_2.length)),
                          overlaps[var_1, var_2][0],
                          overlaps[var_1, var_2][1]))


# Adding constraints for overlapping
def constraint_overlap(x, y, w, r):
    def constraint_function(a, b):
        try:
            if a[w] == b[r]:
                return True
        except IndexError:
            pass

    problem.addConstraint(constraint_function, (x, y))


for x, y, w, r in constraints_1:
    constraint_overlap(x, y, w, r)


# Adding constraints for length of words
def constraint_length(variable, length):
    def constraint_function(a):
        if len(a) == length:
            return True

    problem.addConstraint(constraint_function, (variable,))


for var in variables:
    var_dup = var.split(',')
    length = int(var_dup[3][:-1])
    constraint_length(var, length)

solution = problem.getSolution()

# Printing the result
result = dict()
for answer in solution:
    value = answer[1:-1]
    value = value.split(',')
    i = int(value[0])
    j = int(value[1])
    direction = value[2]
    length = int(value[3])

    for add in range(length):
        result[(((i + add) if direction == ' \'down\'' else i),
                ((j + add) if direction == ' \'across\'' else
                 j))] = solution[answer][add]

# Displaying the answer using pygame
width = max([val[0] for val in result]) + 2
height = max([val[1] for val in result]) + 2
size = (height * 70, width * 70)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Crossword')

while True:
    screen.fill((0, 0, 0))

    # white and black boxes with text
    for i in range(height):
        for j in range(width):
            rect = pygame.Rect(i * 70, j * 70, 70, 70)
            if (j, i) in result:
                pygame.draw.rect(screen, (255, 255, 255), rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)
                font = pygame.font.Font(pygame.font.get_default_font(), 60)
                text = font.render(result[(j, i)], True, (0, 0, 0))
                text_rect = text.get_rect()
                text_rect.center = rect.center
                screen.blit(text, text_rect)
            else:
                pygame.draw.rect(screen, (0, 0, 0), rect)

    # To end the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    pygame.display.update()
