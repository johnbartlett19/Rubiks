from rubiks_classes import *
from constants import *
from utilities import *
from input_txt import *

def init_game_smart(game):
    """
    Set up a Rubiks Cube game by assigning the locations to each cube and the colors to each cube facet.
    This routine keeps track of which cubes have been assigned and colors any sides where the answer is
     already known.  Also produces graphic which updates as the data is entered for verification.
    Expects as input a game of class Game.  No return, just modifies the game.
    :param game:
    :return: none
    """
    print('Initiating a Cube.  Enter colors of each cube on each face, ')
    print('  starting in the upper left, working across, then down to the middle row,')
    print('  and across, then bottom left to bottom right')

    # Create assignment library.  Format will be index is a location e.g. ([x, y, z])
    #  contents will be list of possible cubes e.g. [cube1, cube2, ..]
    # when possible list has length one, cube is fully assigned
    assign_lib = {}
    for cube in game.cubes:
        if cube.home_loc != (1, 1, 1):
            pos_cube = PossibleCube(cube.home_loc)
            pos_cube.type = type(cube)
            assign_lib[cube.loc] = pos_cube
    for loc in assign_lib:
        pos_cube = assign_lib[loc]
        for cube in game.cubes:
            if isinstance(cube, MidCube):
                if cube.loc == pos_cube.location:
                    cube.assigned = True
                    pos_cube.pos_cubes = [cube]
                    break
            elif isinstance(cube, pos_cube.type):
                pos_cube.pos_cubes.append(cube)

    for face in range(6):
        window = SetupWindow('Face ' + str(face))
        painted = [False, False, False, False, False, False, False, False, False]
        print('Initiate face with center color ' + std_color[face])
        # paint squares where we already know the answer:
        colors = [False, False, False, False, False, False, False, False, False]
        changed = True
        while changed:
            changed = False
            for y in [2, 1, 0]:
                for x in range(3):
                    if not painted[3*y+x]:
                        loc = loc_2d_to_3d(face, x, y)
                        changed = assign_lib[loc].purge() or changed
                        if len(assign_lib[loc].pos_cubes) == 1:
                            cube = assign_lib[loc].pos_cubes[0]
                            facet_color = cube.orient[face]
                            window.paint_square(x, y, facet_color)
                            painted[3 * y + x] = True
                    elif False not in painted:
                        changed = False
                        break
        painted_correctly = False
        if 'face_input' in globals():
            for y in range(3):
                for x in range(3):
                    if painted[3 * y + x]:
                        continue
                    else:
                        color = face_input[face][y * 3 + x]
                        window.paint_square(x, y, color)
                        colors[3 * y + x] = color
        else:
            while not painted_correctly:
                colors[4] = std_color[face]
                for y in [2, 1, 0]:
                    for x in range(3):
                        if painted[3 * y + x]:
                            continue
                        # elif face_input in locals():
                        #     color = face_input[face][y*3+x]
                        #     window.paint_square(x, y, color)
                        #     colors[3 * y + x] = color
                        else:
                            okay = False
                            while not okay:
                                color = input('Location ' + str(x) + ', ' + str(y) + ': ')
                                if not is_color(color):
                                    print('Not a valid color, please type again: ')
                                else:
                                    okay = True
                            # paint square
                            window.paint_square(x, y, color)
                            colors[3*y+x] = color
                        # find or assign a cube for this square
                        # find 3D location of this cube
                        # cube_loc = loc_2d_to_3d(face, x, y)
                ans = input('Is face painted correctly? ').lower()
                # todo improve behavior when you get painting wrong and need to redo.  e.g.
                #  unpaint the cube?  allow choice of which cube to update?
                if ans in ['y', 'yes', 'yep', 'yup']:
                    painted_correctly = True
        window.close()
        for x in range(3):
            for y in range(3):
                cube_loc = loc_2d_to_3d(face, x, y)
                assign_lib[cube_loc].add_color(colors[3*y+x], face)
        for pos_cube_loc in assign_lib:
            assign_lib[pos_cube_loc].purge()

    file = open('input_txt.py', 'w+')
    for face in range(6):
        file.write('face_' + str(face) + ' = [')
        for y in range(3):
            for x in range(3):
                loc = loc_2d_to_3d(face, x, y)
                cube = game.cube_at_location(loc)
                facets = cube.find_facets()
                for facet in facets:
                    if facet == face:
                        color = cube.orient[facet]
                        if x == 2 and y == 2:
                            file.write("'" + color + "'")
                        else:
                            file.write("'" + color + "', ")
        file.write(']\n')
    file.write('face_input = [face_0, face_1, face_2, face_3, face_4, face_5]')
    file.close()


def draw_game_full(game, title='Full Cube', debug=False):
    """
    # draw graphic showing front, top and right side colors
    :param game: game
    :param faces: [list] of faces e.g. [F, U, R] three max
    :return: nada
    """
    faces = range(6)
    # Define windows within the bigger window to be used for three sides of cube
    front_win = [[(11, 1), (14, 4)],
                 [(14, 1), (17, 4)],
                 [(17, 1), (20, 4)],
                 [(11, 4), (14, 7)],
                 [(14, 4), (17, 7)],
                 [(17, 4), (20, 7)],
                 [(11, 7), (14, 10)],
                 [(14, 7), (17, 10)],
                 [(17, 7), (20, 10)]
                 ]
    top_win = []
    for x in range(9):
        window = [(front_win[x][0][0], front_win[x][0][1] + 10), (front_win[x][1][0], front_win[x][1][1] + 10)]
        top_win.append(window)
    right_win = []
    for x in range(9):
        window = [(front_win[x][0][0] + 10, front_win[x][0][1] + 10),
                  (front_win[x][1][0] + 10, front_win[x][1][1] + 10)]
        right_win.append(window)
    left_win = []
    for x in range(9):
        window = [(top_win[x][0][0] - 10, top_win[x][0][1]), (top_win[x][1][0] - 10, top_win[x][1][1])]
        left_win.append(window)
    down_win = []
    for x in range(9):
        window = [(front_win[x][0][0] + 10, front_win[x][0][1]), (front_win[x][1][0] + 10, front_win[x][1][1])]
        down_win.append(window)
    back_win = []
    for x in range(9):
        window = [(top_win[x][0][0], top_win[x][0][1] + 10), (top_win[x][1][0], top_win[x][1][1] + 10)]
        back_win.append(window)

    win = GraphWin(title=title, width=600, height=600)
    win.setCoords(0, 0, 31, 31)
    win_locs = [left_win, top_win, right_win, down_win, front_win, back_win]

    for x in range(len(faces)):
        # face is number equivalent of face to be shown, 0 for left, 4 for front ..
        game.draw_game_side(win, faces[x], win_locs[x])
    win.getMouse()  # pause before closing
    if not debug:
        win.close()


def draw_game_three(game, faces):
    """
    # draw graphic showing front, top and right side colors
    :param game: game
    :param faces: [list] of faces e.g. [F, U, R] three max
    :return: nada
    """
    if len(faces) != 3:
        raise ValueError('Wrong number of faces in draw call')
    # Define windows within the bigger window to be used for three sides of cube
    front_win = [[(1, 1), (4, 4)],
                 [(4, 1), (7, 4)],
                 [(7, 1), (10, 4)],
                 [(1, 4), (4, 7)],
                 [(4, 4), (7, 7)],
                 [(7, 4), (10, 7)],
                 [(1, 7), (4, 10)],
                 [(4, 7), (7, 10)],
                 [(7, 7), (10, 10)]
                 ]
    top_win = []
    for x in range(9):
        window = [(front_win[x][0][0], front_win[x][0][1] + 10), (front_win[x][1][0], front_win[x][1][1] + 10)]
        top_win.append(window)
    right_win = []
    for x in range(9):
        window = [(front_win[x][0][0] + 10, front_win[x][0][1] + 10),
                  (front_win[x][1][0] + 10, front_win[x][1][1] + 10)]
        right_win.append(window)
    title = 'Front, Top & Right Sides'
    win = GraphWin(title=title, width=500, height=500)
    win.setCoords(0, 0, 21, 21)
    win_locs = [front_win, top_win, right_win]

    for x in range(3):
        # face is number equivalent of face to be shown, 0 for left, 4 for front ..
        game.draw_game_side(win, faces[x], win_locs[x])
    win.getMouse()  # pause before closing
    win.close()
    # find the cubes of the face to be printed


def draw_game(game):
    # for axis in [X, Y, Z]:
    #     for position in [0,2]:
    #         draw_game_side(game, axis, position)
    win_locs = [[(1, 1), (4, 4)],
                [(4, 1), (7, 4)],
                [(7, 1), (10, 4)],
                [(1, 4), (4, 7)],
                [(4, 4), (7, 7)],
                [(7, 4), (10, 7)],
                [(1, 7), (4, 10)],
                [(4, 7), (7, 10)],
                [(7, 7), (10, 10)]
                ]
    to_draw = [
        (L, 'Left'),
        (U, 'Top'),
        (R, 'Right'),
        (D, 'Bottom'),
        (F, 'Front'),
        (B, 'Back')
    ]

    for face in to_draw:
        window = GraphWin(face[1], width=200, height=200)
        window.setCoords(0, 0, 11, 11)
        game.draw_game_side(window, face[0], win_locs)
        window.getMouse()  # pause before closing
    window.close()


def solve_white_cross(game):
    # find a white mid not in correct place
    game.orient()
    # cube_set = find_cubes(game.cubes, cube_type='SideCube', color_set=['white'], cnt=4)
    one_top_spin = False
    while not game.solved_white_cross():
        cubes_on_top_white_up = find_cubes(game.cubes, cube_type=SideCube, location=[9,9,2], faces=[('white',[1])])
        cubes_on_top_white_side = find_cubes(game.cubes, cube_type=SideCube, location=[9, 9, 2], faces=[('white', [0,2,4,5])])
        cubes_on_bottom_white_down = find_cubes(game.cubes, cube_type=SideCube, location=[9,9,0], faces=[('white',[3])])
        cubes_on_bottom_white_side = find_cubes(game.cubes, cube_type=SideCube, location=[9,9,0], faces=[('white', [0,2,4,5])])
        cubes_on_vert_edge = find_cubes(game.cubes, cube_type=SideCube, faces=[('white', [0,2,4,5])])

        if len(cubes_on_top_white_up) > 0 and not one_top_spin:
            print('Top Spin Once')
            cube = cubes_on_top_white_up[0]
            (qty, axis, direction) = find_rotation(cube, cube.home_loc, Z)
            position = cube.loc[axis]
            for x in range(qty):
                game.rotate(axis, position, direction)
            # one_top_spin = True
        elif len(cubes_on_bottom_white_down) > 0:
            # if in bottom row and white is facing down
            cube = cubes_on_bottom_white_down[0]
            print('Cube on Bottom White Down: ' + str(cube) + ': ' + str(cube.loc))
            (qty, axis, direction) = find_rotation(cube, cube.home_loc, Z)
            position = 0
            # rotate bottom (D) until on correct side
            for x in range(qty):
                game.rotate(axis, position, direction)
            # what is face of second color?
            for x in range(6):
                if cube.orient[x] != 'white' and cube.orient[x]:
                    second_color_facet = x
            (axis, qty) = axis_from_face[second_color_facet]
            (qty, axis2, direction) = facet_rotation[(D, U)]
            position = cube.loc[axis]
            for x in range(qty):
                game.rotate(axis, position, direction)

            if cube.loc[0] == 1:
                axis = Y
            elif cube.loc[1] == 1:
                axis = X
            else:
                raise ValueError('Cube not in expected location')
            (qty, axis, direction) = find_rotation(cube, cube.home_loc, axis)
            position = 0
            for x in range(qty):
                game.rotate(axis, position, direction)

        elif len(cubes_on_top_white_side) > 0:
            cube = cubes_on_top_white_side[0]
            print('Cube on top white side: ' + str(cube) + ": " + str(cube.loc))
            # Push cube to bottom so white is on the bottom
            white_facet = cube.facet('white')
            dest_facet = 3 # bottom
            (qty, axis, direction) = facet_rotation[(white_facet, dest_facet)]
            if qty > 1:
                raise ValueError()
            position = 1
            game.rotate(axis, [position], direction)  # rotate side_cube to bottom
            game.rotate(2, 0, 'CL')
            game.rotate(axis, [position], opp_dir(direction))
            asdf = 1

        elif len(cubes_on_bottom_white_side) > 0:
            cube = cubes_on_bottom_white_side[0]
            print('Cube on bottom white side: ' + str(cube) + ": " + str(cube.loc))
            # Move face be under destination location, still with face out
            white_facet = cube.facet('white')
            other_color = cube.orient[3]
            # find facet of other_color middle cube, so we know dest
            for mid_cube in game.cubes:
                if isinstance(mid_cube, MidCube) and other_color in mid_cube.orient:
                    dest_facet = mid_cube.facet(other_color)
                    break
            (qty, axis, direction) = facet_rotation[(white_facet, dest_facet)]
            position = cube.loc[axis]
            for x in range(qty):
                game.rotate(axis, [position], direction)  # rotate side_cube to bottom
            # now rotate middle down, rotate bottom once, rotate middle back up
            # destination facet to bottom (3)
            (qty, axis, direction) = facet_rotation[(dest_facet, 3)]
            if qty > 1:
                raise ValueError()
            position = 1
            game.rotate(axis, position, direction)
            game.rotate(2, 0, 'CL')
            game.rotate(axis, position, opp_dir(direction))
        elif len(cubes_on_vert_edge) > 0:
            cube = cubes_on_vert_edge[0]
            print('Cube on vertical edge, move to bottom: ' + str(cube) + ": " + str(cube.loc))
            # rotate to bottom.  find correct axis and destination loc
            # find white face direction
            dest_loc=[9,9,0]
            white_facet = cube.facet('white')
            dest_facet = 3
            (qty, axis, direction) = facet_rotation[(white_facet, dest_facet)]
            if qty > 1:
                raise ValueError()
            position = cube.loc[axis]
            game.rotate(axis, position, direction)
            game.rotate(2, 0, 'CL')
            game.rotate(axis, position, opp_dir(direction))
        else:
            raise ValueError("Can't find move to make in solving white cross")

        one_top_spin = True
    if game.solved_white_cross():
        return()
    asdf = 1


def solve_top_white_corners(game):
    while not game.solved_top_corners():
        cubes_on_top_white_up = find_cubes(game.cubes, cube_type=CornerCube, location=[9, 9, 2], faces=[('white', [1])])
        cubes_on_top_white_side = find_cubes(game.cubes, cube_type=CornerCube, location=[9, 9, 2], faces=[('white', [0, 2, 4, 5])])
        cubes_on_bottom_white_side = find_cubes(game.cubes, cube_type=CornerCube, location=[9, 9, 0], faces=[('white', [0, 2, 4, 5])])
        cubes_on_bottom_white_down = find_cubes(game.cubes, cube_type=CornerCube, location=[9, 9, 0], faces=[('white', [3])])
        if len(cubes_on_bottom_white_side) > 0:
            cube = cubes_on_bottom_white_side[0]
            print('Cube on bottom white on side, move to home: ' + str(cube) + ": " + str(cube.loc))
            # move so it is under position where it belongs ..
            dest_loc = [cube.home_loc[0], cube.home_loc[1], 0]
            (qty, axis, direction) = find_rotation(cube, dest_loc, Z)
            position = 0
            for x in range(qty):
                game.rotate(axis, position, direction)

            # find rotation to final position (not ready to do it but needs to be saved)
            (final_qty, final_axis, final_direction) = facet_rotation[(cube.facet('white'), 1)]
            final_position = cube.loc[final_axis]
            # find color of bottom facet
            bottom = cube.orient[3]
            # find location of bottom-colored mid-cube
            for mid_cube in game.cubes:
                if isinstance(mid_cube, MidCube):
                    if bottom in mid_cube.orient:
                        comm_side = mid_cube.facet(bottom)
                        break
            if cube.loc[0] == mid_cube.loc[0]:
                dest_loc[1] = (2 * cube.loc[1] - 1) % 3
                dest_loc[0] = mid_cube.loc[0]
            elif cube.loc[1] == mid_cube.loc[1]:
                dest_loc[0] = (2 * cube.loc[0] - 1) % 3
                dest_loc[1] = mid_cube.loc[1]
            dest_loc[2] = cube.loc[2]

            # rotate to interim position
            (qty, axis, direction) = find_rotation(cube, dest_loc, Z)
            if qty > 1:
                raise ValueError()
            game.rotate(axis, position, direction)
            game.rotate(final_axis, final_position, opp_dir(final_direction))
            game.rotate(axis, position, opp_dir(direction))
            game.rotate(final_axis, final_position, final_direction)

        elif len(cubes_on_bottom_white_down) > 0:
            # Need to rotate side that puts one of the side facets on the bottom.  Look for
             # one of the other colors, find its facet, move that to bottom
            cube = cubes_on_bottom_white_down[0]
            print('Cube on bottom white down, rotate to side and move to home: ' + str(cube) + ": " + str(cube.loc))
            # first move under home location (Z location = 0, Z-axis)
            dest_loc = [cube.home_loc[0], cube.home_loc[1], 0]
            (qty, axis, dir) = find_rotation(cube, dest_loc, Z)
            position = 0
            for x in range(qty):
                game.rotate(axis, position, dir)
            facet_set = cube.facet_set()
            non_white_facet_set = []
            for facet in facet_set:
                if facet[0] != 'white':
                    non_white_facet_set.append(facet)
            (qty, axis, dir) = facet_rotation[(non_white_facet_set[0][1], D)]
            position = cube.loc[axis]
            game.rotate (axis, position, dir)
            (qty, axis2, dir2) = facet_rotation[(non_white_facet_set[1][1],cube.facet('white'))]
            if axis2 != Z:
                raise ValueError()
            position2 = cube.loc[axis2]
            game.rotate(axis2, position2, dir2)
            game.rotate(axis, position, opp_dir(dir))
        elif len(cubes_on_top_white_side) > 0:
            # Need to rotate side that puts one of the side facets on the bottom.  Look for
            # one of the other colors, find its facet, move that to bottom
            cube = cubes_on_top_white_side[0]
            print('Cube on top white on side, push to bottom and move to home: ' + str(cube) + ": " + str(cube.loc))
            # rotate down so white ends up on side not bottom
            # find not-white facet currently on side, rotate to bottom
            facet_set = cube.facet_set()
            for set in facet_set:
                if set[0] != 'white' and set[1] in [0, 2, 4, 5]:
                    facet = set[1]

            (qty, axis, dir) = facet_rotation[(facet, 3)]
            position = cube.loc[axis]
            game.rotate(axis, position, dir)
            dest_facet = opp_facet[cube.facet('white')]
            for set in cube.facet_set():
                if set[0] != 'white' and set[1] in [0, 2, 4, 5]:
                    facet = set[1]
            (qty, axis2, dir2) = facet_rotation[(facet, dest_facet)]
            position2 = cube.loc[axis2]
            game.rotate(axis2, position2, dir2)
            game.rotate(axis, position, opp_dir(dir))
            asdf = 1

        elif len(cubes_on_top_white_up) > 0:
            raise ValueError('In correct orientation but not correct position?  Not implemenmted')
    asdf = 1


def solve_side_sidecubes(game):
    game.orient()
    while not game.solved_side_edges():
        # find SideCubes with colors that are not white and not yellow and in bottom row
        side_cubes = find_cubes(game.cubes, cube_type=SideCube)
        side_cubes_on_bottom = []
        # for cube in side_cubes:
        #     print(cube.name + str(cube.loc))
        for cube in side_cubes:
            if 'white' not in cube.orient and 'yellow' not in cube.orient and cube.loc[2] == 0:
                facet_set = cube.facet_set()
                mid1 = game.cube_at_location((1, cube.loc[1], cube.loc[2]))
                mid2 = game.cube_at_location((cube.loc[0], 1, cube.loc[2]))
                facet_set_mid1 = mid1.facet_set()
                facet_set_mid2 = mid2.facet_set()
                if facet_set_mid1[0] != facet_set[0] and facet_set_mid1 != facet_set[1]:
                    side_cubes_on_bottom.append(cube)
                elif facet_set_mid2[0] != facet_set[0] and facet_set_mid1 != facet_set[1]:
                    side_cubes_on_bottom.append(cube)
        # find SideCubes in side locations that are not in the right location or not color aligned
        side_cubes_side_flipped = []
        for cube in side_cubes:
            if 'white' not in cube.orient and 'yellow' not in cube.orient and cube.loc[2] == 1:
                if cube.loc != cube.home_loc:
                    side_cubes_side_flipped.append(cube)
                else:
                    facet_set = cube.facet_set
                    color_1 = facet_set()[0][0]
                    facet_1 = facet_set()[0][1]
                    color_2 = facet_set()[1][0]
                    facet_2 = facet_set()[1][1]
                    mid_1_facet = game.mid_cube_by_color(color_1).facet(color_1)
                    mid_2_facet = game.mid_cube_by_color(color_2).facet(color_2)
                    if facet_1 != mid_1_facet or facet_2 != mid_2_facet:
                        side_cubes_side_flipped.append(cube)

        if len(side_cubes_on_bottom) > 0:
            cube = side_cubes_on_bottom[0]
            print('Side cube on bottom to move onto side: ' + str(cube) + ": " + str(cube.loc))
            # move under correct colored mid-piece
              # what color is on the side?
            facet_set = cube.facet_set()
            for set in facet_set:
                if set[1] != 3:
                    side_color = set[0]
                    side_facet = set[1]
            mid_cube = game.mid_cube_by_color(side_color)
            (qty, axis, dir) = facet_rotation[(side_facet, mid_cube.facet(side_color))]
            axis = Z
            position = 0
            for x in range(qty):
                game.rotate(axis, position, dir)
            # rediscover facet directions
            facet_set = cube.facet_set()
            for set in facet_set:
                if set[1] != 3:
                    side_color = set[0]
                    side_facet = set[1]
                else:
                    bottom_color = set[0]
                    bottom_facet = set[1]
            # find facet for mid-cube matching second side of side cube
            other_mid = game.mid_cube_by_color(bottom_color)
            other_facet = other_mid.facet(bottom_color)
            # first move
            (qty, axis1, dir1) = facet_rotation[(side_facet, opp_facet[other_facet])]
            pos1 = 0
            game.rotate(axis1, pos1, dir1)

            (qty, axis2, dir2) = facet_rotation[(side_facet, bottom_facet)]
            pos2 = other_mid.loc[axis2]
            game.rotate(axis2, pos2, dir2)
            game.rotate(axis1, pos1, opp_dir(dir1))
            game.rotate(axis2, pos2, opp_dir(dir2))
            # second half starts by continuing seocnd to last rotation
            game.rotate(axis1, pos1, opp_dir(dir1))
            (qty, axis3, dir3) = facet_rotation[(other_facet, 3 )]
            pos3 = mid_cube.loc[axis3]
            game.rotate(axis3, pos3, dir3)
            # and back
            game.rotate(axis1, pos1, dir1)
            game.rotate(axis3, pos3, opp_dir(dir3))

            # draw_game_three(game, [F, U, R])
        elif len(side_cubes_side_flipped) > 0:
            cube_to_move = side_cubes_side_flipped[0]
            print('Side cube on side but not final, move to bottom: ' + str(cube_to_move) + ": " + str(cube_to_move.loc))
            facet_set = cube_to_move.facet_set()
            color_1 = facet_set[0][0]
            facet_1 = facet_set[0][1]
            color_2 = facet_set[1][0]
            facet_2 = facet_set[1][1]
            mid_cube = game.mid_cube_by_color(color_1)
            other_mid = game.mid_cube_by_color(color_2)
            mid_1_facet = mid_cube.facet(color_1)
            mid_2_facet = other_mid.facet(color_2)

            # find SideCube on facet_1 side in yellow row
            for cube in game.cubes:
                if cube.loc[2] == 0 and isinstance(cube, SideCube):
                    facet_set_new = cube.facet_set()
                    if facet_set_new[0][1] == facet_1 or facet_set_new[1][1] == facet_1:
                        break

            # which facet is side facet?
            for set in facet_set:
                if set[1] != 3:
                    side_color = set[0]
                    side_facet = set[1]

            # first move
            (qty, axis1, dir1) = facet_rotation[(side_facet, opp_facet[mid_2_facet])]
            pos1 = 0
            game.rotate(axis1, pos1, dir1)

            (qty, axis2, dir2) = facet_rotation[(side_facet, bottom_facet)]
            pos2 = other_mid.loc[axis2]
            game.rotate(axis2, pos2, dir2)
            game.rotate(axis1, pos1, opp_dir(dir1))
            game.rotate(axis2, pos2, opp_dir(dir2))
            # second half starts by continuing seocnd to last rotation
            game.rotate(axis1, pos1, opp_dir(dir1))
            (qty, axis3, dir3) = facet_rotation[(mid_2_facet, 3)]
            pos3 = mid_cube.loc[axis3]
            game.rotate(axis3, pos3, dir3)
            # and back
            game.rotate(axis1, pos1, dir1)
            game.rotate(axis3, pos3, opp_dir(dir3))

def flip_to_bottom_cross(game):
    game.orient()
    while not game.solved_bottom_cross():
        # determine if there are two side cubes adjacent with yellow down (L in corner)
        side_cubes = find_cubes(game.cubes, cube_type=SideCube, location=[9, 9, 0])
        side_cubes_yellow_down = []
        for cube in side_cubes:
            if ('yellow', 3) in cube.facet_set():
                side_cubes_yellow_down.append(cube)
        if len(side_cubes_yellow_down) == 2:
            if side_cubes_yellow_down[0].loc[0] != side_cubes_yellow_down[1].loc[0] and \
                    side_cubes_yellow_down[0].loc[1] != side_cubes_yellow_down[1].loc[1]:
                print('Two yellow adjacent on bottom, rotate to upper left (bottom left)')
                asdf = 1  # two yellow adjacent
                cycle = [(0, 1, 0), (1, 0, 0), (2, 1, 0), (1, 2, 0)]
                dest_1 = (0, 1, 0)
                dest_2 = (1, 0, 0)
                for x in range(len(cycle)):
                    if dest_1 == cycle[x]:
                        dest_1_at = x
                    if dest_2 == cycle[x]:
                        dest_2_at = x
                    if side_cubes_yellow_down[0].loc == cycle[x]:
                        cube1_at = x
                    if side_cubes_yellow_down[1].loc == cycle[x]:
                        cube2_at = x
                dest = (dest_1_at, dest_2_at)
                current = (cube1_at, cube2_at)
                convert = {
                    (0, 3): (1, 'CL'),
                    (3, 0): (1, 'CL'),
                    (0, 1): (0, 'CL'),
                    (1, 0): (0, 'CL'),
                    (1, 2): (1, 'CC'),
                    (2, 1): (1, 'CC'),
                    (2, 3): (2, 'CL'),
                    (3, 2): (2, 'CL')
                }
                axis = Z
                position = 0
                (qty, dir) = convert[current]
                for x in range(qty):
                    game.rotate(axis, position, dir)

                print('Execute yellow pair flip routine')
                command_string = ("B R D R' D' R D R' D' B'")
                list = command_string_to_commands(command_string)
                command_set(game, list)
                asdf = 1
            elif side_cubes_yellow_down[0].loc[0] == side_cubes_yellow_down[1].loc[0] or \
                    side_cubes_yellow_down[0].loc[1] == side_cubes_yellow_down[1].loc[1]:  # if two down across from each other
                print('Pair opposite, execute yellow pair flip routine to make adjacent')
                command_string = ("B R D R' D' R D R' D' B'")
                list = command_string_to_commands(command_string)
                command_set(game, list)
            else:
                raise ValueError('Not implemented')
    asdf = 1

def align_bottom_sides(game):
    """
    Move bottom SideCubes around until each is in its home location
    :param game:
    :return:
    """
    game.orient()
    print('Solving to align bottom side cubes in correct locations')
    spin_count = 0
    while not game.solved_align_bottom_sides():
        spin_count += 1
        bottom_sides = find_cubes(game.cubes, cube_type=SideCube, location=[9, 9, 0])
        mid_cubes = find_cubes(game.cubes, cube_type=MidCube, location=[9, 9, 1])
        # align one and only one bottom_side cube with one mid_cube
        for x in range(4):
            aligned = one_aligned(bottom_sides, mid_cubes)
            if len(aligned) in [0,2,3]:
                # Rotate Z axis one spot and try again
                game.rotate(2, [0], 'CL')
            else:
                break
        if len(aligned) not in [1,4]:
            raise ValueError('Could not find good rotated position')
        elif len(aligned) == 4:
            return
        else:
        # realign game so aligned cube is in front
            the_one = aligned[0]
            for x in range(3):
                (qty, axis, direction) = find_rotation(the_one, (1, 0, 0), use_axis=Z)
                for x in range(qty):
                    game.rotate(axis, [0,1,2], direction)
            # run the algorithm
            cmd_str = "L D L' D L D D L'"
            list = command_string_to_commands(cmd_str)
            command_set(game, list)
            # draw_game_full(game, 'Rotated ' + str(spin_count) + ' times', debug=True)
            if spin_count > 10:
                raise ValueError('Too many tries on bottom sides, case not solved for?')
    game.orient()


def align_bottom_corners(game):
    """
    Move bottom (yellow) CornerCubes around until each is in its home location
    :param game:
    :return:
    """
    while not game.bottom_corners_correct_locations():
        bottom_corners = find_cubes(game.cubes, location=(9,9,0), cube_type=CornerCube)
        # is one cube in correct location?
        correct = []
        for cube in bottom_corners:
            if cube.home_loc == cube.loc:
                correct.append(cube)
        if len(correct) == 1:
            # rotate whole cube so correct cube is in upper left
            # flip bottom up
            # game.rotate(X, [0, 1, 2], 'CL')
            # game.rotate(X, [0, 1, 2], 'CL')
            cube = correct[0]
            (qty, axis, rotation) = find_rotation(cube, (2,0,0), Z)
            for x in range(qty):
                game.rotate(Z, [0, 1, 2], rotation)
            # R U' L' U R' U' L U
            cmd_str = "L D' R' D L' D' R D"
            list = command_string_to_commands(cmd_str)
            command_set(game, list)
            game.orient()
            # draw_game_full(game, 'Debug one correct & move', debug=True)
        elif len(correct) == 0:
            cmd_str = "L D' R' D L' D' R D"
            list = command_string_to_commands(cmd_str)
            command_set(game, list)
            game.orient()
            # draw_game_full(game, 'None, pick any & move', debug=True)
        else:
            raise ValueError('Not implemented')


def flip_bottom_corners(game):
    while not game.bottom_corners_correct_facets():
        bottom_corners = find_cubes(game.cubes, location=(9, 9, 0), cube_type=CornerCube)
        mid_cubes = find_cubes(game.cubes, cube_type=MidCube)
        face_colors = [False for x in range(6)]
        for cube in mid_cubes:
            for x in range(6):
                if cube.orient[x]:
                    face_colors[x] = cube.orient[x]
        cubes_not_oriented = []
        for cube in bottom_corners:
            for x in range(6):
                if cube.orient[x] and cube.orient[x] != face_colors[x] and cube not in cubes_not_oriented:
                    cubes_not_oriented.append(cube)
        # if cube is incorrect orientation, position at (2,0,0)
        # if len(cubes_not_oriented) not in [2,4]:
        #     raise ValueError('Incorrect number of flipped cubes?')
        for cube in cubes_not_oriented:
            # move to (2,0,0)
            (qty, axis, rotation) = find_rotation(cube, (2,0,0), Z)
            for x in range(qty):
                game.rotate(axis, 0, rotation)
            cmd_str = "R U R' U'  R U R' U'"
            list = command_string_to_commands(cmd_str)
            command_set(game, list)
            for x in range(qty):
                game.rotate(axis, 0, opp_dir(rotation))
            asdf = 1
            # game.orient()
        # execute 1/3 of set, check cube for orientation
        # if OK, move to another cube, if not execute again
        asdf = 1
    asdf = 1