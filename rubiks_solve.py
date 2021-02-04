from rubiks_classes import *
from routines import *

game = Game()
init_game_smart(game)
draw_game_full(game, 'Ready to Solve')

print()
print('Solve top white cross:')
solve_white_cross(game)
draw_game_full(game, 'Solved top white cross')

print()
print('Solve top white CornerCubes:')
solve_top_white_corners(game)
draw_game_full(game, 'Solved top white corners')

print()
print('Solve side SideCubes:')
solve_side_sidecubes(game)
draw_game_full(game, 'Solved side cubes')

print()
print('Flip bottom side cubes to yellow down:')
flip_to_bottom_cross(game)
draw_game_full(game, 'Turned all bottom sides to yellow down')

print()
print('Solve side SideCubes:')
align_bottom_sides(game)
draw_game_full(game, 'Bottom sides in correct locations')

print()
print('Position bottom corners:')
align_bottom_corners(game)
draw_game_full(game, 'Positioned bottom corners')

print()
print('Flip bottom corners to finish')
flip_bottom_corners(game)
draw_game_full(game)

asdf = 1


