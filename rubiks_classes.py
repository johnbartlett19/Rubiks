#/bin/python
from utilities import *
from constants import *


class Game(object):
    """
    Represents the entire Rubiks Cube.  Init defines the three types of sub-cubes (corners, sides, centers).
    """
    def __init__(self):
        self.top_color = False
        self.left_color = False
        self.cubes = []
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    #cube_type = False
                    location = (x, y, z)
                    if location == (1, 1, 1):
                        #cube_type = 'Center'
                        cube = CenterCube(self, 1, 1, 1)
                    elif (x + y + z) % 2 > 0:
                        #cube_type = 'Edge'
                        cube = SideCube(self, x, y, z)
                    elif 1 not in location:
                        #cube_type = 'Corner'
                        cube = CornerCube(self, x, y, z)
                    else:
                        #cube_type = "MidFace"
                        cube = MidCube(self, x, y, z)
                    self.cubes.append(cube)
        self.init_solved()

    def init_solved(self, top_color='white', left_color='orange'):
        """
        Set up this Rubiks Cube game by assigning the locations to each cube and the colors to each cube facet,
         for a fully solved game (all colors the same on each face of the cube)
        Expects as input a game of class Game.  No return, just modifies the game.
        :param top_color:  color to be on the top of the cube e.g. 'white'
        :param left_color:  color to be on the left edge of the cube e.g. 'orange'
        :return: none
        """
        # print('Initiating cubed solved with top color: ' + top_color + ', left color: ' + left_color)
        self.top_color = top_color
        self.left_color = left_color
        seq1 = (['orange', 'white', 'red', 'yellow'], ['green', 'blue'])
        seq2 = (['green', 'white', 'blue', 'yellow'], ['red', 'orange'])
        seq3 = (['orange', 'green', 'red', 'blue'], ['yellow', 'white'])
        colors = [x for x in range(6)]
        colors[1] = top_color
        colors[3] = opposite_color[top_color]
        colors[0] = left_color
        colors[2] = opposite_color[left_color]
        # find two adjacent in first four
        # order of last 2 if forward, forward, if back, back
        if top_color in seq1[0] and left_color in seq1[0]:
            seq = seq1
        elif top_color in seq2[0] and left_color in seq2[0]:
            seq = seq2
        elif top_color in seq3[0] and left_color in seq3[0]:
            seq = seq3
        else:
            raise ValueError('Initiate: Impossible sequence')
        for x in range(4):
            if seq[0][x] == top_color:
                top1 = x
            elif seq[0][x] == left_color:
                left1 = x
        if (top1 - left1) % 4 == 1:
            colors[4] = seq[1][0]
            colors[5] = seq[1][1]
        elif (left1 - top1) % 4 == 1:
            colors[4] = seq[1][1]
            colors[5] = seq[1][0]
        else:
            raise ValueError()
        print('Assumes color sequence L,U,R,D,F,B is', end=' ')
        for color in colors:
            print(color, end=', ')
        print()
        for cube in self.cubes:
            cube.loc = cube.home_loc
            if cube.loc[0] == 0:  # X-axis
                cube.orient[0] = colors[0]
            elif cube.loc[0] == 2:
                cube.orient[2] = colors[2]
            if cube.loc[1] == 0:  # Y-axis
                cube.orient[4] = colors[4]
            elif cube.loc[1] == 2:
                cube.orient[5] = colors[5]
            if cube.loc[2] == 0:  # Z-axis
                cube.orient[3] = colors[3]
            elif cube.loc[2] == 2:
                cube.orient[1] = colors[1]

    def cube_at_location(self, location):
        """
        find cube currently at location & return cube
        :param location: as list [x, y, z]
        :return: cube or False if not found or badly specified
        """
        for cube in self.cubes:
            if location == cube.loc:
                return cube
        return False

    def solved_white_cross(self):
        """
        Determine if white cross has been solved.
        :return: "WhiteCross" or False
        """
        # find white center & four white cubes (look at home_loc
        five_white_cubes = []
        for cube in self.cubes:
            if cube.home_loc[2] == 2 and 'Side' in str(cube):
                if cube.loc != cube.home_loc:
                    return False
                if cube.facet('white') != 1:
                    return False
        return True

    def solved_top_corners(self):
        """
        Determine if top white corners have been solved.
        :return: "WhiteCross" or False
        """
        if not self.solved_white_cross():
            raise ValueError('Must solve top white cross first')
        # find white center & four white cubes (look at home_loc
        for cube in self.cubes:
            if cube.home_loc[2] == 2 and 'Corner' in str(cube):
                if cube.loc != cube.home_loc:
                    return False
                if cube.facet('white') != 1:
                    return False
        return True

    def solved_side_edges(self):
        if not self.solved_top_corners():
            raise ValueError('Must solve top white cross and top white corners first')
        for cube in self.cubes:
            if isinstance(cube, SideCube) and cube.loc[2] == 1:
                if cube.loc != cube.home_loc:
                    return False
                facet_set = cube.facet_set()
                mid1 = self.cube_at_location((1, cube.loc[1], cube.loc[2]))
                mid2 = self.cube_at_location((cube.loc[0], 1, cube.loc[2]))
                facet_set_mid1 = mid1.facet_set()
                facet_set_mid2 = mid2.facet_set()
                if not facet_set_mid1[0] in facet_set or not facet_set_mid2[0] in facet_set:
                    return False
        return True

    def solved_bottom_cross(self):
        if not self.solved_side_edges():
            raise ValueError('Must solve top white cross, top white corners and side edges first')
        for cube in self.cubes:
            if isinstance(cube, SideCube) and cube.loc[2] == 0:
                facet_set = cube.facet_set()
                if ('yellow', 3) not in facet_set:
                    return False
        return True

    def solved_align_bottom_sides(self):
        bottom_sides = find_cubes(self.cubes, cube_type=SideCube, location=(9,9,0))
        mid_sides = find_cubes(self.cubes, cube_type=MidCube, location=(9,9,1))
        for cube in bottom_sides:
            for facet in cube.facet_set():
                if facet[0] != 'yellow':
                    for mid_cube in mid_sides:
                        if mid_cube.loc[0] == cube.loc[0] and mid_cube.loc[1] == cube.loc[1]:
                            if facet[0] not in mid_cube.orient:
                                return False
        return True

    def find_by_home(self, home_loc):
        for cube in self.cubes:
            if cube.home_loc == home_loc:
                return cube

    def rotate(self, axis, position, direction):
        """
        function to rotate a side or the center of the game cube.
        :param axis: which axis of the cube is to be rotatled around (X, Y, Z)
        :param position: [array] list of positions along axis (e.g. 0, 1 or 2) to be rotated.  multiple entries
          means multiple slices to be rotated.  2 means rotate the whole cube
        :param direction: rotate clockwise (CL) or counter-clockwise (CC)
        :return: True if final position has colors on outside faces, otherwise False
        """
        # fix for consistency or ease of calling?
        if not isinstance(position, list):
            position = [position]
        # Orient CL and CC to axis and assign 0,1,2
        cubes_to_rotate = []
        # Identify cubes in side to be rotated
        for cube in self.cubes:
            if cube.loc[axis] in position:
                cubes_to_rotate.append(cube)

        # Rotate cubes within the side
        for cube in cubes_to_rotate:
            cube.rotate(axis, direction)

        # Change their positions in the game
        for cube in cubes_to_rotate:
            if axis != 0:
                x = cube.loc[0]
            else:
                x = cube.loc[1]

            if axis == 2:
                y = cube.loc[1]
            else:
                y = cube.loc[2]

            if axis == X or axis == Z:
                if direction == 'CL':
                    new_y = x
                    new_x = (2 * y - 1) % 3
                elif direction == 'CC':
                    new_x = y
                    new_y = (2 * x - 1) % 3
                else:
                    raise ValueError('direction is not either CL or CC')
            else:
                if direction == 'CC':
                    new_y = x
                    new_x = (2 * y - 1) % 3
                elif direction == 'CL':
                    new_x = y
                    new_y = (2 * x - 1) % 3
                else:
                    raise ValueError('direction is not either CL or CC')

            if axis == 0:
                cube.loc = (cube.loc[0], new_x, new_y)

            if axis == 1:
                cube.loc = (new_x, cube.loc[1], new_y)

            if axis == 2:
                cube.loc = (new_x, new_y, cube.loc[2])

        print_rotation(axis, position, direction)

    def orient(self, top_color=False, left_color=False):
        """
        Re-orient game (if needed) to color top_color on top and color left_color on left
        :param top_color: color to be at the top of game after re-orientation
        :param left_color: color to be on left face after re-orientation
        :return: none
        """
        if not top_color:
            top_color = self.top_color
        if not left_color:
            left_color = self.left_color
        # todo need a check to ensure two colors requested can be on adjacent faces
        if top_color == 'white' and left_color == 'yellow' or \
                top_color == 'red' and left_color == 'orange' or \
                top_color == 'blue' and left_color == 'green':
            raise ValueError('Two colors specified cannot be on adjcent sides')
        # find center-of-face cubes
        top_color_cube = find_cubes(self.cubes, cube_type=MidCube, color_set=[top_color], cnt=1)[0]
        left_color_cube = find_cubes(self.cubes, cube_type=MidCube, color_set=[left_color], cnt=1)[0]

        # rotate cube so top color is on top position 1,1,2
        # axis is the one that doesn't change
        (qty, axis, direction) = find_rotation(top_color_cube, [1, 1, 2])
        for x in range(qty):
            self.rotate(axis, [0, 1, 2], direction)
        (qty, axis, direction) = find_rotation(left_color_cube, [0, 1, 1], use_axis=Z)
        for x in range(qty):
            self.rotate(axis, [0, 1, 2], direction)


    def draw_game_side(self, window, face, win_locs):
        """
        Draw
        :param window:  The graphics window to be used for display
        :param face:  The face of the game to be displayed (L, U, R, D, F, B)
        :param win_locs: list of tuples of tuples specifying lower left and upper right corners of square
         for each of 9 squeares of the side of the cube e.g. [((1,1),(4,4)), ((4,1), (8,4)), ... ]
        :return:
        """
        (axis, position) = axis_from_face[face]
        cubes_to_display = []
        for cube in self.cubes:
            if cube.loc[axis] == position:
                cubes_to_display.append(cube)
        facet = face
        for cube in cubes_to_display:
            if axis == X:
                window_loc = [cube.loc[1], cube.loc[2]]
            elif axis == Y:
                window_loc = [cube.loc[0], cube.loc[2]]
            else:
                window_loc = [cube.loc[0], cube.loc[1]]

            if facet == 0 or facet == 5:
                window_loc[0] = ((window_loc[0] * 2 + 2) % 3)
            elif facet == 3:
                window_loc[1] = ((window_loc[1] * 2 + 2) % 3)

            # Choose a window for this cube
            win_index = 3 * window_loc[1] + window_loc[0]
            sq_indx = win_locs[win_index]

            square = Rectangle(Point(sq_indx[0][0], sq_indx[0][1]), Point(sq_indx[1][0], sq_indx[1][1]))
            square.setFill(cube.orient[facet])
            square.draw(window)

    def mid_cube_by_color(self, color):
        """
        find mid-cube of color 'color' and return that cube
        :param color: e.g. 'white'
        :return: cube
        """
        for cube in self.cubes:
            if isinstance(cube, MidCube) and color in cube.orient:
                return cube
        else:
            raise ValueError('Could not find cube of color: ' + color)

    def bottom_corners_correct_locations(self):
        bottom_corners = find_cubes(self.cubes, location=(9,9,0), cube_type=CornerCube)
        for cube in bottom_corners:
            if cube.loc != cube.home_loc:
                return False
        return True

    def bottom_corners_correct_facets(self):
        bottom_corners = find_cubes(self.cubes, location=(9,9,0), cube_type=CornerCube)
        mid_cubes = find_cubes(self.cubes, cube_type=MidCube)
        face_colors = [False for x in range(6)]
        for cube in mid_cubes:
            for x in range(6):
                if cube.orient[x]:
                    face_colors[x] = cube.orient[x]
        for cube in bottom_corners:
            for x in range(6):
                if cube.orient[x] and cube.orient[x] != face_colors[x]:
                    return False
        return True


class Cube(object):
    """
    Represents one of the 27 cubes of the Game.  Init includes the name of the game to which it belongs
    Orientation sequence is Left, Top, Right, Bottom, Front, Back (L,T,R,B,F,K)
    In Orientation False = no color (inside face), True = Needs color assignment, Color ('red', 'green', etc.) is
     assigned color.
    """

    def __init__(self, game, x, y, z):
        self.loc = None
        self.name = 'Cube_' + str(x) + '_' + str(y) + '_' + str(z)
        self.game = game
        self.orient = [False, False, False, False, False, False]
        self.assigned = False
        self.home_loc = (x, y, z)

    def __repr__(self):
        return self.name

    def rotate(self, axis, direction):
        """
        function to rotate cube during a face rotation.
        :param axis: Rotation axis X, Y or Z
        :param direction: rotate clockwise (CL) or counter-clockwise (CC) around axis
        :return: True
        """
        if axis == X:
            if direction == 'CC':
                self.orient = (self.orient[0], self.orient[4], self.orient[2], self.orient[5],
                               self.orient[3], self.orient[1])
            elif direction == 'CL':
                self.orient = (self.orient[0], self.orient[5], self.orient[2], self.orient[4],
                               self.orient[1], self.orient[3])
            else:
                ValueError('direction value of ' + direction + 'not allowed')
        elif axis == Y:
            if direction == 'CC':
                self.orient = (self.orient[1], self.orient[2], self.orient[3], self.orient[0],
                               self.orient[4], self.orient[5])
                asdf = 1
            elif direction == 'CL':
                self.orient = (self.orient[3], self.orient[0], self.orient[1], self.orient[2],
                               self.orient[4], self.orient[5])
            else:
                ValueError('direction value of ' + direction + 'not allowed')
        elif axis == Z:
            if direction == 'CC':
                self.orient = (self.orient[4], self.orient[1], self.orient[5], self.orient[3],
                               self.orient[2], self.orient[0])
            elif direction == 'CL':
                self.orient = (self.orient[5], self.orient[1], self.orient[4], self.orient[3],
                               self.orient[0], self.orient[2])
            else:
                ValueError('direction value of ' + direction + 'not allowed')
        else:
            ValueError('axis value of ' + axis + 'not allowed')

    def facet(self, color):
        """
        Find the facet of this cube with the requested color.  Return facet as integer in range(6) or
         False if not found
        :param color: requested facet color
        :return: facet number as integer 0-5 or False
        """
        facet = False
        for x in range(6):
            if self.orient[x] == color:
                facet = x
        return facet

    def facet_set(self):
        """
        Return an array of tuples indicating current position of each non-False facet
         e.g. [('green', 3),('white',2)]
        :return: array of tuples as above
        """
        facet_set = []
        for x in range(6):
            if self.orient[x]:
                facet_set.append((self.orient[x], x))
        return facet_set

    def set_facet(self, color_set):
        """
        input a set of tubples [(color, facet), (color, facet) ..] and restructure the orient string to match
        :param color_set:
        :return: nada
        """
        for pair in color_set:
            if pair[0] not in self.orient:
                raise ValueError('Did not receive colors consistent with this cube')
        self.orient = [False, False, False, False, False, False]
        for pair in color_set:
            self.orient[pair[1]] = pair[0]
        asdf = 1

class CenterCube(Cube):
    """
    Represents the center cube which has no external faces and always remains at position 1,1,1
    """
    def __init__(self, game, x, y, z):
        super().__init__(game, x, y, z)
        self.name = 'Center_' + str(x) + '_' + str(y) + '_' + str(z)

    def find_facets(self, loc=False):
        return None


class CornerCube(Cube):
    '''
    Of type Cube, represents a corner cube (8 in Game), each has three colored sides
    '''
    def __init__(self, game, x, y, z):
        super().__init__(game, x, y, z)
        self.name = 'Corner_' + str(x) + '_' + str(y) + '_' + str(z)

    def find_facets(self, loc=False):
        if not loc:
            loc = self.loc
        facets = find_facets(loc)
        if len(facets) != 3:
            raise ValueError('Facet count does not match location')
        return facets


class SideCube(Cube):
    '''
    Of type Cube, represents a side (on edge) cube (12 in game), each has 2 colored sides
    '''
    def __init__(self, game, x, y, z):
        super().__init__(game, x, y, z)
        self.name = 'Side_' + str(x) + '_' + str(y) + '_' + str(z)

    def find_facets(self, loc=False):
        if not loc:
            loc = self.loc
        facets = find_facets(loc)
        if len(facets) != 2:
            raise ValueError('Facet count does not match location')
        return facets

        
class MidCube(Cube):
    '''
    Of type Cube, represents a middle cube on each side (6 in game), each has 1 colored side
    '''
    def __init__(self, game, x, y, z):
        super().__init__(game, x, y, z)
        self.name = 'Mid_' + str(x) + '_' + str(y) + '_' + str(z)

    def find_facets(self, loc=False):
        if not loc:
            loc = self.loc
        facets = find_facets(loc)
        if len(facets) != 1:
            raise ValueError('Facet count does not match location')
        return facets


class PossibleCube(object):
    """
    List of possible cubes for a specific location in an unsolved game, and colors identified
     for that cube
    """
    def __init__(self, location):
        self.location = location
        self.pos_cubes = []
        self.colors = []
        self.type = None

    def __repr__(self):
        return 'PosCube_' + str(self.location)

    def add_color(self, color, facet):
        self.colors.append((color, facet))
        rem_cubes = []
        for pos_cube in self.pos_cubes:
            if color not in pos_cube.orient:
                rem_cubes.append(pos_cube)
        for cube in rem_cubes:
            self.pos_cubes.remove(cube)


    def purge(self):
        """
        Search possible cubes list to see if any have been assigned.  If yes,
         purge them from this list unless there is just one
        :return: True if a change was made, otherwise False
        """
        new_pos_cubes = []
        for cube in self.pos_cubes:
            if cube.assigned and cube.loc == self.location:
                new_pos_cubes = [cube]
                break
            elif not cube.assigned:
                new_pos_cubes.append(cube)
        changed = False
        if len(new_pos_cubes) == 0:
            raise ValueError('Should not have eliminated all possibilities')
        elif len(new_pos_cubes) == 1:
            self.pos_cubes = new_pos_cubes
            if not self.pos_cubes[0].assigned:
                cube = self.pos_cubes[0]
                cube.assigned = True
                # get facets for this position
                facets = cube.find_facets(self.location)

                # check against known colors & facets
                orient = [False for x in range(6)]
                facets_used = []
                for (col, fac) in self.colors:
                    if fac not in facets:
                        raise ValueError('Color Facet does not match possible facet location')
                    orient[fac] = col
                    facets_used.append(fac)
                # find facet not specified in self.colors
                missing_color = False
                missing_facet = False
                for color in cube.orient:
                    if color and color not in orient:
                        missing_color = color
                for facet in facets:
                    if facet not in facets_used:
                        missing_facet = facet
                # finalize new orient list for this cube
                if missing_facet:
                    orient[missing_facet] = missing_color
                cube.orient = orient
                # set cube location to this possible cube location
                cube.loc = self.location
                changed = True
        else:
            self.pos_cubes = new_pos_cubes
        return(changed)


class SetupWindow(object):
    """
    Graphics window for displaying one side of Rubik's cube during setup
    """

    def __init__(self, label='Default'):
        self.win_locs = [[(1, 1), (4, 4)],
                         [(4, 1), (7, 4)],
                         [(7, 1), (10, 4)],
                         [(1, 4), (4, 7)],
                         [(4, 4), (7, 7)],
                         [(7, 4), (10, 7)],
                         [(1, 7), (4, 10)],
                         [(4, 7), (7, 10)],
                         [(7, 7), (10, 10)]
                         ]
        self.label = label
        self.window = GraphWin(self.label, width=300, height=300)
        self.window.setCoords(0, 0, 11, 11)

    def close(self):
        self.window.close()

    def paint_square(self, x, y, color):
        winnum = 3 * y + x
        windx = self.win_locs[winnum]
        square = Rectangle(Point(windx[0][0], windx[0][1]), Point(windx[1][0], windx[1][1]))
        square.setFill(color)
        square.draw(self.window)
