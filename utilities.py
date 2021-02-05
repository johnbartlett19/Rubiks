#/bin/python
from graphics import *
from constants import *

def is_color(color):
    """
    Determine if facet_name is a valid color, return True if good
    :param facet_name: name (text color)
    :return: True if color is on the list, otherwise false
    """
    colors = ['red',
             'white',
             'blue',
             'green',
             'yellow',
             'orange'
             ]
    if color not in colors:
            return False
    return True


def init_game(game):
    """
    Set up a Rubiks Cube game by assigning the locations to each cube and the colors to each cube facet.
    Expects as input a game of class Game.  No return, just modifies the game.
    :param game:
    :return: none
    """
    print('Initiating a Cube.  Enter colors of each cube on each face, ')
    print('  starting in the lower left, working across, then up to the middle row,')
    print('  and across, then top left to top right')

    comp = (('Front','Pos', 'Zero', 'Pos'),
            ('Left', 'Zero', 'Neg', 'Pos'),
            ('Right', 'Zero', 'Pos', 'Pos'),
            ('Top', 'Pos', 'Pos', 'Zero'),
            ('Bottom', 'Pos', 'Neg', 'Zero'),
            ('Back', 'Neg', 'Zero', 'Neg')
            )
    for face in comp:
        print('Initiate ' + face[0] + 'face')
        for x in range(3):
            for y in range(3):
                okay = False
                while not okay:
                    color = input('Location ' + str(x) + ', ' + str(y) + ' : ')
                    if not is_color(color):
                        print('Not a valid color, please type again: ')
                    else:
                        okay = True


def convert(standard):
    if standard == 'U' or standard == "U'":
        axis = Z
        position = [2]
        if "'" in standard:
            direction = 'CL'
        else:
            direction = 'CC'
    elif standard == 'L' or standard == "L'":
        axis = X
        position = [0]
        if "'" in standard:
            direction = 'CC'
        else:
            direction = 'CL'
    elif standard == 'F' or standard == "F'":
        axis = Y
        position = [0]
        if "'" in standard:
            direction = 'CC'
        else:
            direction = 'CL'
    elif standard == 'R' or standard == "R'":
        axis = X
        position = [2]
        if "'" in standard:
            direction = 'CL'
        else:
            direction = 'CC'
    elif standard == 'B' or standard == "B'":
        axis = Y
        position = [2]
        if "'" in standard:
            direction = 'CL'
        else:
            direction = 'CC'
    elif standard == 'D' or standard == "D'":
        axis = Z
        position = [0]
        if "'" in standard:
            direction = 'CC'
        else:
            direction = 'CL'
    elif standard == "M" or standard == "M'":
        axis = X
        position = [1]
        if "'" in standard:
            direction = 'CC'
        else:
            direction = 'CL'
    elif standard == "E" or standard == "E'":
        axis = Z
        position = [1]
        if "'" in standard:
            direction = 'CC'
        else:
            direction = 'CL'
    elif standard == "S" or standard == "S'":
        axis = Y
        position = [1]
        if "'" in standard:
            direction = 'CC'
        else:
            direction = 'CL'
    elif standard == "X" or standard == "X'":
        axis = X
        position = [0,1,2]
        if "'" in standard:
            direction = 'CL'
        else:
            direction = 'CC'
    elif standard == "Y" or standard == "Y'":
        axis = Z  # yeah really
        position = [0,1,2]
        if "'" in standard:
            direction = 'CL'
        else:
            direction = 'CC'
    elif standard == "Z" or standard == "Z'":
        axis = Y  # no idea why
        position = [0,1,2]
        if "'" in standard:
            direction = 'CC'
        else:
            direction = 'CL'
    else:
        raise ValueError('Not standard notation or not implemented')
    return(axis, position, direction)


def command_set(game, commands):
    for command in commands:
        (axis, position, direction) = convert(command)
        game.rotate(axis, position, direction)


def command_string_to_commands(command_string):
    command_list = []
    for i in range(len(command_string)):
        if command_string[i] == ' ' or command_string[i] == "'":
            continue
        elif i+1 == len(command_string):
            command = command_string[i]
        elif command_string[i+1] == "'":
            command = command_string[i] + command_string[i+1]
        else:
            command = command_string[i]
        command_list.append(command)
    return command_list


def find_cubes2(cube_set, cube_type, color_set, cnt=1):
    use_colors = []
    for color in color_set:
        if color:
            use_colors.append(color)
        else:
            asdf = 1
    cube_set_return = []
    for cube in cube_set:
        if cube_type in str(type(cube)):
            color_match = True
            for color in use_colors:
                if color not in cube.orient and color != 'any':
                    color_match = False
            if color_match:
                cube_set_return.append(cube)
            asdf =1
        asdf = 1
    asdf = 1
    if cnt != len(cube_set_return):
        raise ValueError('Cube set not equal to requested count')
    return cube_set_return


def find_cubes(cube_set, cube_type='*', location=[9, 9, 9], color_set=['*'], faces=('*', '*'), cnt=None):
    """
    Find a specific cube or cubes from within cube_set based on input parameters and return
     an array of those cubes
    :param cube_set: input set of cubes as an array [cube, cube, cube ..]
    :param cube_type: looking for specifc cube type e.g. SideCube.  '*' means any
    :param location: array of locations in form [1,0,2] or False meaning no location specified.  using 9 as
     a location implies wild card (any location) e.g. [0,0,9] is any cube in the front face
    :param color_set: looking for cubes with specific face colors e.g. ['white', 'red'] returns three cubes
     that have white on one face and red on another.  '*' implies any color
    :param faces: an array of tuples specifying a color and a direction where L, U, R, D, F, B = range(6)
      e.g. [('white', 1), ('blue', 3), ..]  This is an AND condition, all must be met for cube to return
     is a cube with a white facet facing up
    :param cnt: expected number of cubes returned.  If None, count unknown and any result is OK.  Here as
     a debug parameter
    :return: an array of cubes that meet the criteria specified
    """
    cube_set_return = []
    for cube in cube_set:
        if isinstance(cube, cube_type) or cube_type == ['*']:
            if location == [9, 9, 9] or cube_loc_match(cube, location):
                color_match = True
                for color in color_set:
                    if color not in cube.orient and color != '*':
                        color_match = False
                face_match = False
                for face in faces:
                    if face[0] == '*':
                        face_match = True
                    else:
                        for facet in face[1]:
                            if face[0] == cube.orient[facet]:
                                face_match = True
                if color_match and face_match:
                    cube_set_return.append(cube)
    if cnt != len(cube_set_return) and cnt:
        raise ValueError('Cube set not equal to requested count')
    return cube_set_return


def cube_loc_match(cube, location):
    """
    Determine if cube matches location.  Location is array of values [0,1,2] representing [x, y, z].
     A value of 9 in the location array is a wild card value
    :param cube: cube
    :param location: [x,y,z] with values range(3) except 9 as a wild card
    :return: True if matches otherwise False
    """
    if cube.loc[0] == location[0] or location[0] == 9:
        if cube.loc[1] == location[1] or location[1] == 9:
            if cube.loc[2] == location[2] or location[2] == 9:
                return True
    return False


def find_rotation(cube, dest_loc, use_axis=False):
    """
    Determine cube rotation to take 'cube' to the destination location (e.g. [1,1,2)  This routine
     rotates the entire cube, not just one face
    :param cube: cube of a game.  
    :param dest_loc: three parameter list indicating destination
    :return: (qty, axis, direction)  qty is the number of turns.  axis is the axis of rotation, direction
      is 'CL' or 'CC' based on axis
    """
    #todo have to figure out how to constrain axis so second move doesn't move it away.  Top color should use X or
    # Y axis, side color should use only Z axis.
    # game = cube.game
    if (dest_loc[0] == cube.loc[0] and not use_axis) or use_axis == X:
        axis = X
        dim_dest_loc = [dest_loc[1], dest_loc[2]]
        dim_cube_loc = [cube.loc[1], cube.loc[2]]
    elif (dest_loc[1] == cube.loc[1] and not use_axis) or use_axis == Y:
        axis = Y
        dim_dest_loc = [dest_loc[0], dest_loc[2]]
        dim_cube_loc = [cube.loc[0], cube.loc[2]]
    elif (dest_loc[2] == cube.loc[2] and not use_axis) or use_axis == Z:
        axis = Z
        dim_dest_loc = [dest_loc[0], dest_loc[1]]
        dim_cube_loc = [cube.loc[0], cube.loc[1]]
    qty = 0
    direction = False
    if (dim_dest_loc[0] == dim_cube_loc[1]) and (dim_dest_loc[1] == (2 * dim_cube_loc[0] - 1) % 3):
        qty = 1
        if axis == Y:
            direction = 'CL'
        else:
            direction = 'CC'
    elif (dim_dest_loc[1] == dim_cube_loc[0]) and (dim_dest_loc[0] == (2 * dim_cube_loc[1] - 1) % 3):
        qty = 1
        if axis == Y:
            direction = 'CC'
        else:
            direction = 'CL'
    elif (dim_dest_loc[0] == (2 * dim_cube_loc[0] - 1) % 3) and (dim_dest_loc[1] == (2 * dim_cube_loc[1] - 1) % 3):
        qty = 2
        direction = 'CL'
    return (qty, axis, direction)


def find_rotation_by_face(cur_facet, dest_facet, axis):
    """
    Determine cube rotation to take 'cube' to the destination location (e.g. [1,1,2)  This routine
     rotates the entire cube, not just one face
    :param cur_facet: starting facet range(6)
    :param dest_facet: facet destination location [x, y, z]
    :param axis: axis to use if specified, otherwise False
    :return: (qty, axis, position, direction)  qty is the number of turns.  axis is the axis of rotation, position
     defines the planes to be rotated [0,1,2], direction is 'CL' or 'CC' based on axis
    """
    (qty, axis, direction) = facet_rotation[(cur_facet, dest_facet)]
    return (qty, axis, direction)


def is_solved(game):
    """
    Determine if a game is fully solved by comparing cube locations to home locations
    :param game: game
    :return: True or False
    """
    solved = True
    for cube in game.cubes:
        if cube.home_loc != cube.loc:
            solved = False
    return solved


def find_face(color):
    if color == 'red':
        return red
    elif color == 'white':
        return white
    elif color == 'orange':
        return orange
    elif color == 'yellow':
        return yellow
    elif color == 'blue':
        return blue
    elif color == 'green':
        return green
    else:
        raise ValueError('Requested color is not a cube color')


def print_rotation(axis, position, direction):
    """
    For use in seeing what the program has decided to do.  Print to the console the face or cube turns
     that the program is executing (e.g. R U' F F etc.)
    :param axis: X, Y or Z axis for the turn
    :param position: Location of plane to be turned (array)
    :param direction: CL or CC from axis point of view (e.g. L = X axis, position 0, CC)
    :return: none (print to console)
    """
    if axis == X:
        if position == [0]:
            if direction == 'CL':
                move = 'L'
            else:
                move = "L'"
        elif position == [1]:
            if direction == 'CL':
                move = 'M'
            else:
                move = "M'"
        elif position == [2]:
            if direction == 'CC':
                move = 'R'
            else:
                move = "R'"
        elif position == [0, 1, 2]:
            if direction == 'CC':
                move = 'X'
            else:
                move = "X'"
        else:
            raise ValueError('Print routine does not have action for this case: ' + str(position))
    elif axis == Y:
        if position == [0]:
            if direction == 'CL':
                move = 'F'
            else:
                move = "F'"
        elif position == [1]:
            if direction == 'CL':
                move = 'S'
            else:
                move = "S'"
        elif position == [2]:
            if direction == 'CC':
                move = 'B'
            else:
                move = "B'"
        elif position == [0, 1, 2]:
            if direction == 'CL':
                move = 'Z'
            else:
                move = "Z'"
        else:
            raise ValueError('Print routine does not have action for this case: ' + str(position))
    elif axis == Z:
        if position == [0]:
            if direction == 'CL':
                move = 'D'
            else:
                move = "D'"
        elif position == [1]:
            if direction == 'CL':
                move = 'E'
            else:
                move = "E'"
        elif position == [2]:
            if direction == 'CC':
                move = 'U'
            else:
                move = "U'"
        elif position == [0, 1, 2]:
            if direction == 'CC':
                move = 'Y'
            else:
                move = "Y'"
        else:
            raise ValueError('Print routine does not have action for this case: ' + str(position))
    else:
        raise ValueError('Not a valid input for axis')

    print("Rotation executed: " + move)
    return


def opp_dir(direction):
    if direction == 'CC':
        return 'CL'
    elif direction == 'CL':
        return 'CC'
    raise ValueError("opp_dir called with invalid direction")


def one_aligned(sides, mid_cubes):
    """
    Determine how many of the cubes in sides are aligned with a mid cube.  Return the quantity that are aligned
    :param sides: [cube, cube ..] list of 4 side cubes on the same Z axis position
    :param mid_cubes: [cube, cube ..] list of 4 mid cubes
    :return: list of cubes that are aligned (0 to 4)
    """
    matches = 0
    aligned = []
    for cube in sides:
        for mid_cube in mid_cubes:
            if cube.loc[0] == mid_cube.loc[0] and cube.loc[1] == mid_cube.loc[1]:
                for facet in mid_cube.facet_set():
                    if facet[0] in cube.orient:
                        aligned.append(cube)
    return aligned


neg = lambda x: (2 * x - 1) % 3


def loc_2d_to_3d(face, x, y):
    """
    Find three D location [x, y, z] based on knowing face (L, U, R ..) and x, y on that face
    :param face: which face of cube, where [L, U, R, D, F, B] = [0, 1, 2, 3, 4, 5]
    :return: location (x, y, z)
    """
    if face == 0:
        retx = 0
        rety = neg(x)
        retz = y
    elif face == 1:
        retx = x
        rety = y
        retz = 2
    elif face == 2:
        retx = 2
        rety = x
        retz = y
    elif face == 3:
        retx = x
        rety = neg(y)
        retz = 0
    elif face == 4:
        retx = x
        rety = 0
        retz = y
    elif face == 5:
        retx = neg(x)
        rety = 2
        retz = y
    else:
        raise ValueError('Bad value for face')
    return((retx, rety, retz))


def loc_3d_to_2d(face, x, y, z):
    if face in [1,3,4]:
        retx = x
    elif face == 5:
        retx = neg(x)
    elif face == 0:
        retx = neg(y)
    elif face == 2:
        retx = y
    else:
        raise ValueError('Bad value for face')
    if face in [0, 2, 4, 5]:
        rety = z
    elif face == 1:
        rety = y
    elif face == 3:
        rety = neg(y)
    else:
        raise ValueError('Band value for face')
    return(x, y)


def find_facets(loc):
    facets = []
    if loc[X] == 0:
        facets.append(0)
    elif loc[X] == 2:
        facets.append(2)
    if loc[Y] == 0:
        facets.append(4)
    elif loc[Y] == 2:
        facets.append(5)
    if loc[Z] == 0:
        facets.append(3)
    elif loc[Z] == 2:
        facets.append(1)
    return facets
