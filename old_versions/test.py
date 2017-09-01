from timeline_v2 import *

test = Timeline('testname',"whereisit","filename","infoList")

# set length of segment per frame to appear in turtle screen
t_width = 30
screen_x = 500
screen_y = 500

turtle.screensize(screen_x, screen_y)
turtle.up()
turtle.setx(-450)
turtle.down()

turtle.speed('slow')
turtle.width(10)
for i in range(len(test.colours)):
    turtle.color(test.colours[i])
    turtle.forward(t_width)

print(turtle.screensize())
# leaves window open until user decides to close it
turtle.done()
