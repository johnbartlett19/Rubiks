#/bin/python

# # location of middle cubes
# red = [0,1,1]
# white = [1,1,2]
# orange = [2,1,1]
# yellow = [1,1,0]
# blue = [1,0,1]
# green = [1,2,1]

L, U, R, D, F, B = range(6)
std_color = ['orange', 'white', 'red', 'yellow', 'green', 'blue']

X, Y, Z = range(3)
axis_name = ['X', 'Y', 'Z']

# 'red', 'white', 'orange', 'yellow', 'blue', 'green'
# 'orange', 'white', 'red', 'yellow', 'green', 'blue'
# 'orange', 'green', 'red', 'blue', 'yellow', 'white'

# find axis and position from face
axis_from_face = {
    L:(X, 0),
    U:(Z, 2),
    R:(X,2),
    D:(Z,0),
    F:(Y,0),
    B:(Y,2)
}

facet_rotation = {
    (1,4):(1, X, 'CL'),
    (4,3):(1, X, 'CL'),
    (3,5):(1, X, 'CL'),
    (5,1):(1, X, 'CL'),
    (0,1):(1, Y, 'CL'),
    (1,2):(1, Y, 'CL'),
    (2,3):(1, Y, 'CL'),
    (3,0):(1, Y, 'CL'),
    (0,5):(1, Z, 'CC'),
    (5,2):(1, Z, 'CC'),
    (2,4):(1, Z, 'CC'),
    (4,0):(1, Z, 'CC'),
    
    (4,1):(1, X, 'CC'),
    (3,4):(1, X, 'CC'),
    (5,3):(1, X, 'CC'),
    (1,5):(1, X, 'CC'),
    (1,0):(1, Y, 'CC'),
    (2,1):(1, Y, 'CC'),
    (3,2):(1, Y, 'CC'),
    (0,3):(1, Y, 'CC'),
    (5,0):(1, Z, 'CL'),
    (2,5):(1, Z, 'CL'),
    (4,2):(1, Z, 'CL'),
    (0,4):(1, Z, 'CL'),
    
    (0,0):(0, X, '*'),
    (1,1):(0, Z, '*'),
    (2,2):(0, X, '*'),
    (3,3):(0, Z, '*'),
    (4,4):(0, Y, '*'),
    (5,5):(0, Y, '*'),

    (0,2):(2,[Y, Z], 'CL'),
    (2,0):(2,[Y, Z], 'CL'),
    (1,3):(2,[X, Y], 'CL'),
    (3,1):(2,[X, Y], 'CL'),
    (4,5):(2,[X, Z], 'CL'),
    (5,4):(2,[X, Z], 'CL')
}

opposite_color = {
    'white':'yellow',
    'yellow':'white',
    'red':'orange',
    'orange':'red',
    'blue':'green',
    'green':'blue'
}

opp_facet = {
    0:2,
    1:3,
    2:0,
    3:1,
    4:5,
    5:4
}


# orange_face = ['yellow', 'orange', 'white', 'green', 'orange', 'orange', 'green', 'green', 'orange']
# white_face = ['yellow', 'red', 'yellow','yellow', 'white', 'green', 'white', 'blue', 'red']
# red_face = ['red', 'red', 'blue', 'orange', 'red', 'blue', 'orange', 'white', 'blue']
# yellow_face = ['red', 'white', 'orange', 'blue', 'yellow', 'blue', 'green', 'green', 'yellow']
# green_face = ['red', 'red', 'green', 'white', 'green', 'yellow', 'blue', 'yellow', 'green']
# blue_face = []
# face_input = [orange_face, white_face, red_face, yellow_face, green_face, blue_face]
