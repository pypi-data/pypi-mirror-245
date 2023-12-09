BoxTurtle will automatically import and translate all regular turtle functions. This means that you do not have to import turtle on it's own to perform any regular turtle functions, just use BoxTurtle.

For example, you do not have to do:

    import turtle
    import BoxTurtle
    turtle.bgcolor("white")
    BoxTurtle.goto(0, 30, 0)
    turtle.done()

You can simply do:

    import BoxTurtle
    BoxTurtle.bgcolor("white")
    BoxTurtle.goto(0, 30, 0)
    BoxTurtle.done()

However, even though BoxTurtle will import turtle on its own, you must have turtle installed with your version of Python.

---

*Note: I did not write any original turtle commands, I just redefined them. The only functions that I wrote on my own are the ones documented below, all of which were written using various different functions from the original turtle library. All credit goes to the creators of the original turtle module, and for information on the usage of any turtle functions not shown below, please consult documentation for the original turtle library.*

---

Functions:

---

- goto(x, y, z)

As with the original turtle module, the goto function makes the turtle travel to the point specified. However, now it must account for the z axis as well. This means that goto now takes three arguments (x, y and z) instead of just two (x and y).

    BoxTurtle.goto(x, y, z)

Example:

    BoxTurtle.goto(0, 30, 0)

*(Turtle will travel to 0, 30, 0)*

---

- line(startX, startY, startZ, endX, endY, endZ)

Draws a line from a point defined by startX, startY and startZ to a point definded by endX, endY and endZ.

    BoxTurtle.line(startX, startY, startZ, endX, endY, endZ)

Example:

    BoxTurtle.line(0, -30, 0, 0, 30, 0)

*(Draws a line from 0, -30, 0 to 0, 30, 0)*

---

- cube(x, y, z, size)

Draws a three dimensional cube. The first three arguments, x, y and z, define the point of which the center of the cube will be located. Note that unlike the square function in the original turtle module, this is NOT where the corner of the cube is, but where the center of the cube is, meaning the cube will be centered at that point. Size will determine the length of each edge of the cube. If no parameters are set, they will automatically be set as (0, 0, 0, 10)

    BoxTurtle.cube(x, y, z, size)

Example:

    BoxTurtle.cube(0, 0, 0, 10)

*(Creates a cube centered at 0, 0, 0 with a height, width and length of 10)*

---

- rotate(x, y, z)

Rotate the position of the turtle around any of the three axis. It takes three arguments, x, y, and z. The function will modify the rotation around each axis by the number stated. Note that it rotates AROUND each axis, so increasing x rotation will rotate flip it up, increasing y rotation will flip left, etc. This will also only rotate anything rendered after the function call, so all previous points will remain the same untill clear() is called.

    BoxTurtle.rotate(x, y, z)

Example:

    BoxTurtle.rotate(0, 5, 0)
    BoxTurtle.cube(0, 0, 0, 10)

*(This will create a cube that has been rotated around the x axis slightly)*

---

- stampaxis(size)

Draw the x, y and z axis on the plane to help to show rotations. Note that this will not update when rotations are increased or decreased, and can only be hidden by calling clear(). It effectively acts the same as the regular stamp() method, only it draws the axis instead of the turtle. The function takes an argument for size, but if none is given it will default to 20.

    BoxTurtle.stampaxis(size)

Example:

    BoxTurtle.stampaxis(20)

*(Will draw the x, y and z axis scaled to 20)*

---

- movecam(x, y, z)

Move the camera through the plane. The function takes three arguments, one for x, y, and z, and each determine how much the cam is moved. Just like the rotate function, this only applies to anything drawn after the function is called.

    BoxTurtle.movecam(x, y, z)

Example:

    BoxTurtle.movecam(5, -5, 0)

*(Will move the cam right 5 and down 5)

---

- Other functions

*Note: The functions listed below are the only functions from the original turtle module usable BoxTurtle library. Any other functions that you wish to use from the original turtle library can only be used if you import the turtle library seperatly. Be wary of doing this, as it may override any functions called from BoxTurtle or cause errors.*

*Once again, I do not claim credit for any of the functions in this library shown below, I simply imported the turtle package and redefined them so they could be used in combonation with BoxTurtle. The only functions I wrote are the ones displayed above, all of which were written using the 3D projection formula and existing turtle functions.*

---

bgcolor()

begin_fill()

end_fill()

speed()

title()

done()

penup()

pendown()

color()

pensize()

clear()

tracer()

*Note: tracer() can now only take one argument. In order to turn off refreshing use tracer(False), or tracer(True) to turn it back on.*

update()

Screen()

mainloop()

setup()

stamp()

BoxTurtle()

exitonclick()

bye()

fillcolor()

hideturtle()

showturtle()

---

- Known issues:

There may be some problems with using showturtle, so by default, the turtle is hidden. There are also known issues with using fill, so if you use the begin_fill() command, keep in mind it may not work properly.

---

*Build v1.1.2*

---

*GitHub: https://github.com/chadwickjr*

---