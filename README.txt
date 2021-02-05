README  John Bartlett  Rubiks Cube  2/4/2021
Program solves Rubiks Cube from any starting location (I think!)
Tested with about 5 different initial configurations, more to be done.

Assumptions:
An 'Oriented' cube has white on the top, green facing front (you), orange on the left, red on the right, yellow on
 the bottom and blue in the back.
The graphics of the cube show five 9x9 squares in a cross.  The 9x9 in the middle is the top (white center) as if you
 tipped the cube towards you.  The left and right 9x9s show the left and right sides respectively, and are oriented
 as if you turned the cube 1/4 turn either left or right so that face faces the user.  The top 9x9 is the back and is
 oriented as if you had turned the cube left or right twice so you are looking at the back, with the white side still
 on top.  And the last 9x9 (down right of graphic) is the bottom, oriented as if you had turned the cube (starting
 with green in front) up so you see the bottom.  So the top of the bottom view is the green side and the bottom of
 the bottom is the blue (back) side.

The file input_txt.py describes the cube initial state.  If you delete or comment-out the information in the input_txt
 file, the program will draw a picture of each side starting with orange, and ask you to input the color for each
 square (facet) of the face.  Input starts in the top left corner and goes across, then the middle row, etc.  The
 middle cube is already painted, so that facet is not requested.  The coordinates provided with each request
 (e.g. (1, 2)) are the 2D location of the facet in question, with the X-axis at the bottom and the Y-axis at the left.
 Thus (1,2) refers to the middle facet in the top row.  Axis coordinates start with 0 and go to 2.

Input for the final side of the cube will paint the facets where the answer is known and not where there is still an
 option, so often the blue face will have them all filled in or sometimes 6 out of 9 filled in.  The input sequence
 is still the same but it only requests input for the missing facets.  The coordinates will guide you to the facet
 in question.

Once a new cube solution is put into the program, it writes text into the input_txt.py file so that the same puzzle
 and solution can be executed over again without providing input.  This is useful if you are trying to follow along
 with a cube, or if you are debugging the program.

The program shows a graphic of the cube being solved at each major step.  It also writes a series of moves to the
 console if you want to make those moves on an actual cube to solve it.  The moves are of the form R (Right side
 rotate forward), R' (right side rotate backwards) etc.  The program uses the nomenclature found at the following
 website, which also has a simulator so you can see how each command translates into a cube move.  They are not
 initially intuitive but you get used to them, and I think they are something of a standard.

 https://ruwix.com/the-rubiks-cube/notation/

If you find a starting configuration that fails to solve, please send it to me so I can further debug the program
 (johnbartlett19@gmail.com).  Thanks!
