import argparse
import copy
import random
from typing import List, Union, Tuple
from PIL import Image, ImageDraw

PATH_COLOR = (255, 255, 255)
WALL_COLOR = (0, 0, 0)

def shortest_distance(start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> int:
    """
    Calculate the shortest distance between two positions.
    Args: start_pos (Tuple[int, int]). end_pos (Tuple[int, int]): The ending position as a (row, column) tuple.
    Returns: int
    """
    return (abs(start_pos[0] - end_pos[0]) + abs(start_pos[1] - end_pos[1])) // 2

def find_element_in_matrix(matrix: List[List[int]], target: int) -> Union[List[int], None]:
    """
    Find the target value in a 2D matrix.
    Args: matrix (List[List[int]]): The 2D matrix to search. target (int)
    Returns: Union[List[int], None]
    """
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == target:
                return [i, j]
    return None

class Maze:
    """
       A class for generating, solving, and manipulating mazes.
       Args:
           rows (int): The number of rows in the maze.
           cols (int): The number of columns in the maze.
       Attributes: rows_fixed (int)
           cols_fixed (int)
           index (int)
           maze (List[List[int]])
           path (List[List[int]])
           generation_states (List[List[List[int]]])
           solving_states (List[List[List[int]]])
       """

    def __init__(self, rows: int = 1, cols: int = 1) -> None:
        """
        Initialize the Maze object.
        Args: rows (int)
        cols (int)
        Returns: None
        """
        self.rows_fixed = rows * 2 + 1
        self.cols_fixed = cols * 2 + 1
        self.index = 2
        self.maze = None
        self.path = None
        self.generation_states = []
        self.solving_states = []

    def generate_maze(self) -> None:
        """
        Generate a maze and save generation states in generation_states variable.
        Returns: None
        """
        # empty maze
        self.maze = [[0] * self.cols_fixed for _ in range(self.rows_fixed)]

        self.generation_states.append(copy.deepcopy(self.maze))

        # borders
        self.maze = [
            [1 if i in (0, self.rows_fixed - 1) or j in (0, self.cols_fixed - 1) else 0 for j in range(self.cols_fixed)]
            for i in range(self.rows_fixed)]
        self.generation_states.append(copy.deepcopy(self.maze))

        # make support walls
        for i in range(2, self.rows_fixed, 2):
            for j in range(0, self.cols_fixed, 2):
                self.maze[i][j] = 1

        self.generation_states.append(copy.deepcopy(self.maze))

        # first row indecies
        for j in range(1, self.cols_fixed, 2):
            self.maze[1][j] = self.index
            self.index += 1

        for i in range(1, self.rows_fixed, 2):
            # right walls
            for j in range(1, self.cols_fixed - 2, 2):
                if random.choice([True, False]):
                    self.maze[i][j + 1] = 1

                else:
                    if self.maze[i][j] == self.maze[i][j + 2]:
                        self.maze[i][j + 1] = 1

                    else:
                        temp = copy.copy(self.maze[i][j + 2])

                        for k in range(1, self.cols_fixed, 2):
                            if self.maze[i][k] == temp:
                                self.maze[i][k] = self.maze[i][j]

            # bottom walls
            for j1 in range(1, self.cols_fixed, 2):
                if i != self.rows_fixed - 2:
                    self.maze[i + 2][j1] = self.maze[i][j1]

                    if random.choice([True, False]):
                        # place wall under the cell if exist an exit with the same index
                        count = 0
                        temp = copy.copy(self.maze[i][j1])

                        for z in range(1, self.cols_fixed, 2):
                            if self.maze[i][z] == temp and self.maze[i + 1][z] == 0:
                                count += 1

                        if count > 1:
                            self.maze[i + 1][j1] = 1
                            self.maze[i + 2][j1] = self.index
                            self.index += 1

            # update states
            self.generation_states.append(copy.deepcopy(self.maze))

        # last line
        for i in range(1, self.cols_fixed - 2, 2):
            if self.maze[self.rows_fixed - 2][i] != self.maze[self.rows_fixed - 2][i + 2]:
                self.maze[self.rows_fixed - 2][i + 1] = 0
                temp = copy.copy(self.maze[self.rows_fixed - 2][i + 2])

                for z in range(1, self.cols_fixed, 2):
                    if self.maze[self.rows_fixed - 2][z] == temp:
                        self.maze[self.rows_fixed - 2][z] = self.maze[self.rows_fixed - 2][i]

        self.generation_states.append(copy.deepcopy(self.maze))

        # delete trash
        for i in range(1, self.rows_fixed, 2):
            for j in range(1, self.cols_fixed, 2):
                self.maze[i][j] = 0
        self.index = 2

    def print_maze(self) -> None:
        """
        Print the maze in console.
        Returns: None
        """
        for i in range(self.cols_fixed // 2):
            print('___', end='')
        print()
        for i in range(1, self.rows_fixed, 2):
            print('|', end='')
            for j in range(1, self.cols_fixed, 2):
                if self.maze[i][j + 1] == 1 and self.maze[i + 1][j]:
                    print('__|', end='')
                elif self.maze[i][j + 1] == 1:
                    print('  |', end='')
                elif self.maze[i + 1][j] == 1:
                    print('___', end='')
                elif i == self.rows_fixed - 2 and self.maze[i][j + 1] == 0:
                    print('___', end='')
                else:
                    print('   ', end='')
            print()

    def print_solved_maze(self) -> None:
        """
        Print the solved maze layout in console.
        Returns: None
        """
        for i in range(self.cols_fixed // 2):
            print('___', end='')
        print()
        for i in range(1, self.rows_fixed, 2):
            print('|', end='')
            for j in range(1, self.cols_fixed, 2):
                if self.maze[i][j + 1] == 1 and self.maze[i + 1][j] and [i, j] in self.path:
                    print('_=|', end='')
                elif self.maze[i][j + 1] == 1 and [i, j] in self.path:
                    print(' =|', end='')
                elif self.maze[i + 1][j] == 1 and [i, j] in self.path:
                    print('_=_', end='')
                elif i == self.rows_fixed - 2 and self.maze[i][j + 1] == 0 and [i, j] in self.path:
                    print('_=_', end='')
                elif self.maze[i][j + 1] == 1 and self.maze[i + 1][j]:
                    print('__|', end='')
                elif self.maze[i][j + 1] == 1:
                    print('  |', end='')
                elif self.maze[i + 1][j] == 1:
                    print('___', end='')
                elif i == self.rows_fixed - 2 and self.maze[i][j + 1] == 0:
                    print('___', end='')
                elif [i, j] in self.path:
                    print(' = ', end='')
                else:
                    print('   ', end='')
            print()

    def solve_maze(self, start: Tuple[int, int], end: Tuple[int, int]) -> None:
        """
        Solve the maze from a given start position to an end position.
        Args: start (Tuple[int, int])
            end (Tuple[int, int])
        Returns: None
        """
        if (all(x % 2 == 0 for x in start) and all(x % 2 == 0 for x in end)):
            return

        if start == end:
            return

        max_value = max(self.rows_fixed, self.cols_fixed)
        if not (1 <= start[0] <= max_value and 1 <= start[1] <= max_value and 1 <= end[
            0] <= max_value and 1 <= end[1] <= max_value):
            return

        def a_way_out(maze: List[List[List[int]]], start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> None:
            """
            Recursive function to find a way out in the maze using backtracking.
            Args: maze (List[List[List[int]])
                start_pos (Tuple[int, int])
                end_pos (Tuple[int, int])
            Returns: None
            """
            maze[start_pos[0]][start_pos[1]][1] = 1
            self.solving_states.append(maze[start_pos[0]][start_pos[1]][2])
            ways = []

            def try_move(direction, distance) -> None:
                """
                Attempt to move in a specific direction from the current position and update the maze state.
                Args: maze (List[List[List[int]])
                    direction (Tuple[int, int])
                    distance (int)
                Returns: None
                """
                new_pos_wall = (start_pos[0] + direction[0], start_pos[1] + direction[1])
                new_pos = (start_pos[0] + direction[0] * distance, start_pos[1] + direction[1] * distance)
                if maze[new_pos_wall[0]][new_pos_wall[1]] != 1 and maze[new_pos[0]][new_pos[1]][1] != 1:
                    maze[new_pos[0]][new_pos[1]] = [shortest_distance(new_pos, end_pos), 0,
                                                    maze[start_pos[0]][start_pos[1]][2] + [
                                                        [new_pos[0], new_pos[1]]]]
                    ways.append(maze[new_pos[0]][new_pos[1]])

            try_move((0, 1), 2)
            try_move((-1, 0), 2)
            try_move((1, 0), 2)
            try_move((0, -1), 2)
            shortest_ways = list(filter(lambda x: not x[1], ways))
            shortest_ways.sort(key=lambda x: x[0])
            if any(sublist[:2] == [0, 0] for sublist in shortest_ways):
                return

            if shortest_ways:
                new_start = find_element_in_matrix(maze, shortest_ways[0])
                a_way_out(maze, new_start, end_pos)

            else:
                new_start = [1, 1]
                for i in range(1, self.rows_fixed, 2):
                    for j in range(1, self.cols_fixed, 2):
                        if maze[i][j][0] != 0 and maze[i][j][1] != 1:
                            if maze[i][j][0] < maze[new_start[0]][new_start[1]][0]:
                                new_start = [i, j]
                a_way_out(maze, new_start, end_pos)

        solving_maze = copy.deepcopy(self.maze)
        for i in range(1, self.rows_fixed, 2):
            for j in range(1, self.cols_fixed, 2):
                solving_maze[i][j] = [0, 0, 0]

        solving_maze[start[0]][start[1]] = [shortest_distance(start, end), 0, [list(start)]]
        self.solving_states.append(solving_maze[start[0]][start[1]][2])
        a_way_out(solving_maze, start, end)
        self.solving_states.append(solving_maze[end[0]][end[1]][2])
        self.solving_states.append(solving_maze[end[0]][end[1]][2])
        self.solving_states.append(solving_maze[end[0]][end[1]][2])
        self.path = solving_maze[end[0]][end[1]][2]

    def import_maze_from_file(self, filename: str) -> None:
        """
        Import a maze from a text file.
        Args: filename (str)
        Returns: None
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                maze_data = [list(map(int, line.strip())) for line in file.readlines()]
                self.maze = maze_data
                self.rows_fixed = len(maze_data)
                self.cols_fixed = len(maze_data[0])

        except FileNotFoundError:
            print(f"File {filename} not found.")

    def import_maze_from_image(self, filename) -> None:
        """
        Import a maze from an image file.
        Args: filename (str)
        Returns: None
        """
        wall_color = WALL_COLOR
        path_color = PATH_COLOR

        try:
            image = Image.open(filename)
            width, height = image.size
            maze_data = []

            for y in range(0, height, 21):
                row = []

                for x in range(0, width, 21):
                    pixel = image.getpixel((x, y))

                    if pixel == wall_color:
                        row.append(1)

                    elif pixel == path_color:
                        row.append(0)

                    else:
                        raise ValueError("Unknown pixel color in the image")

                maze_data.append(row)

            self.maze = maze_data
            self.rows_fixed = len(maze_data)
            self.cols_fixed = len(maze_data[0])

        except FileNotFoundError:
            print(f"File {filename} not found.")

    def export_maze_to_file(self, filename: str) -> None:
        """
        Export the maze to a text file.
        Args: filename (str)
        Returns: None
        """
        with open(filename, 'w', encoding='utf-8') as file:
            for row in self.maze:
                file.write(''.join(map(str, row)) + '\n')

    def create_maze_png(self, maze: List[List[int]]) -> Image.Image:
        """
        Create an image of a labyrinth with a solution path if there is one
        Args: maze (List[List[int]])
        Returns: Image.Image
        """

        cell_size = 20  # Adjust cell size as needed, you should change the for algorithm in import also
        wall_color = WALL_COLOR
        path_color = PATH_COLOR

        width = self.cols_fixed * cell_size
        height = self.rows_fixed * cell_size
        img = Image.new('RGB', (width, height), path_color)
        draw = ImageDraw.Draw(img)

        for i in range(self.rows_fixed):
            for j in range(self.cols_fixed):
                if maze[i][j] == 1:
                    draw.rectangle([(j * cell_size, i * cell_size), ((j + 1) * cell_size, (i + 1) * cell_size)], fill=wall_color)
        return img

if __name__ == "__main__":
    """Main function"""

    parser = argparse.ArgumentParser(description="Maze Generator and Solver CLI")
    parser.add_argument("--size", type=str, help="Maze size in the format 'rows,cols'")
    parser.add_argument("--solve_indecies", type=str, help="Indices for solving in the format 'start_row,start_col,end_row,end_col'")
    parser.add_argument("--import_file", type=str, help="Path to the import file")
    parser.add_argument("--filename", type=str, help="Name of the output files")
    parser.add_argument("--console_output", action="store_true", help="Output the maze in console")
    parser.add_argument("--text_output", action="store_true", help="Output the maze in textfile")
    parser.add_argument("--image_output", action="store_true", help="Output the maze in image")

    args = parser.parse_args()
    maze = None

    # check size for generation
    if args.size:
        size_args = str(args.size)
        size = size_args.split(",")
        if len(size) != 2:
            raise ValueError("Error: Provide dimensions in the format 'rows,cols'.")

        rows, cols = map(int, size)
        maze = Maze(rows, cols)
        maze.generate_maze()

    # import maze from file
    if args.import_file:
        maze = Maze()

        if args.import_file.endswith(".png"):
            maze.import_maze_from_image(args.import_file)

        elif args.import_file.endswith(".txt"):
            maze.import_maze_from_file(args.import_file)

        else:
            raise ValueError("Error: Unsupported import file format. Use .png for images or .txt for text.")

    # if the maze is not created, subsequent functions are useless
    if maze is None:
        raise ValueError("Error: Provide maze size or import a maze for solving.")

    # check indecies for solving
    solve_args = str(args.solve_indecies)
    solve_indecies = solve_args.split(",")

    if len(solve_indecies) != 4:
        print("Provide solving coordinates in the format" +
                          "'start_row,start_col,end_row,end_col' to see solution")
        if args.console_output:
            maze.print_maze()
            
        if args.filename:
            if args.text_output:
                maze.export_maze_to_file(args.filename + ".txt")

            if args.image_output:
                maze.create_maze_png(maze.maze).save(args.filename + ".png", "PNG")
        
    else:
        start = list(map(int, solve_indecies[:2]))
        end = list(map(int, solve_indecies[2:]))
        maze.solve_maze(start, end)

        if args.console_output:
            maze.print_maze()

            if maze.path:
                maze.print_solved_maze()

        if args.filename:
            if args.text_output:
                maze.export_maze_to_file(args.filename + ".txt")

            if args.image_output:
                maze.create_maze_png(maze.maze).save(args.filename + ".png", "PNG")
