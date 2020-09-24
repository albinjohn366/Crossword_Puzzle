class Variable():
    ACROSS = "across"
    DOWN = "down"

    def __init__(self, i, j, direction, length):
        """Create a new variable with starting point, direction, and length."""
        self.i = i
        self.j = j
        self.direction = direction
        self.length = length
        self.cells = []
        for k in range(self.length):
            self.cells.append(
                (self.i + (k if self.direction == Variable.DOWN else 0),
                 self.j + (k if self.direction == Variable.ACROSS else 0))
            )


class Crossword():

    def __init__(self, structure, words):
        # Determining the structure of the crossword
        with open(structure) as file:
            self.contents = file.read().splitlines()

        with open(words) as file:
            self.words = file.read().splitlines()

        self.height = len(self.contents)
        self.width = max(len(item) for item in self.contents)

        self.structure = []
        for i in range(self.height):
            row = [True if self.contents[i][j] == '_' else False if
            len(self.contents[i]) <= j else False for j in range(
                self.width)]
            self.structure.append(row)

        # Checking for word start
        self.variables = set()

        for i in range(self.height):
            vertical_start = [(i, j) for j in range(self.width)
                              if self.structure[i][j] and
                              (i == 0 or not self.structure[i - 1][j])]
            horizontal_start = [(i, j) for j in range(self.width)
                                if self.structure[i][j] and
                                (j == 0 or not self.structure[i][j - 1])]

            for m, j in vertical_start:
                length = 1
                for k in range(m + 1, self.height):
                    if self.structure[k][j]:
                        length += 1
                    else:
                        break
                self.variables.add(Variable(m, j, 'down', length))

            for m, j in horizontal_start:
                length = 1
                for k in range(j + 1, self.width):
                    if self.structure[m][k]:
                        length += 1
                    else:
                        break
                self.variables.add(Variable(m, j, 'across', length))

        # Checking for overlaps
        self.overlaps = dict()
        for variable1 in self.variables:
            for variable2 in self.variables:
                if variable1 == variable2:
                    continue
                intersection = set(variable1.cells).intersection(
                    set(variable2.cells))
                if intersection:
                    poi = intersection.pop()
                    self.overlaps[variable1, variable2] = (
                        variable1.cells.index(poi),
                        variable2.cells.index(poi))
                else:
                    self.overlaps[variable1, variable2] = None

    # To find the overlapping neighbors
    def neighbors(self, variable):
        return set(var for var in self.variables
                   if var != variable and
                   self.overlaps[variable, var])


