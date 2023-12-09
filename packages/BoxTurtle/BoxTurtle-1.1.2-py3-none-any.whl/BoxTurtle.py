import turtle
import math


if __name__ == "__main__":
    print("Build v1.1.2")
    print("This was created using the Python turtle module. I do not take credit for the creation of the original Python turtle library")
    print("GitHub: https://github.com/chadwickjr (chadwickjr)")


camX, camY, camZ = 0.0001, 0.0001, -30.0001
rotationX, rotationY, rotationZ = 0, 0, 0
FOV = 500
penUp = False
turtsize = 1
tcolor = "black"
tfill = False
ttracer = True
tshowturtle = False


def stampaxis(width = 20):
    if width > 29:
        width = 29
    turtle.pensize(0.5)
    turtle.tracer(False)
    for num in range(-1 * width, width, 1):
        line(0, num + 0.25, 0, 0, num - 0.25, 0)
    for num in range(-1 * width, width, 1):
        line(num + 0.25, 0, 0, num - 0.25, 0, 0)
    for num in range(-1 * width, width, 1):
        line(0, 0, num + 0.25, 0, 0, num - 0.25)
    turtle.update()
    if ttracer:
        turtle.tracer(True)
    turtle.pensize(turtsize)


def movecam(x, y, z):
    global camX, camY, camZ
    camX += x
    camY += y
    camZ += z


def rotate(x, y, z):
    global rotationX, rotationY, rotationZ
    rotationX += x / 57.25
    rotationY += y / 57.25
    rotationZ += z / 57.25


def line(startX, startY, startZ, endX, endY, endZ):
    if tshowturtle:
        turtle.showturtle()
    else:
        turtle.hideturtle()
    startX *= -1
    startY *= -1
    startZ *= -1
    endX *= -1
    endY *= -1
    endZ *= -1
    
    if endZ < camZ + 5:
        endZ = camZ + 5
    if startZ < camZ + 5:
        startZ = camZ + 5

    cosZ = math.cos(rotationZ)
    sinZ = math.sin(rotationZ)
    cosX = math.cos(rotationX)
    sinX = math.sin(rotationX)
    cosY = math.cos(rotationY)
    sinY = math.sin(rotationY)

    x1 = startX * cosZ - startY * sinX
    y1 = startX * sinZ + startY * cosZ
    y1 = startY * cosX - startZ * sinX
    z1 = startY * sinX + startZ * cosX
    x1 = startX * cosY + startZ * sinY
    z1 = -1 * startX * sinY + startZ * cosY

    x2 = endX * cosZ - endY * sinX
    y2 = endX * sinZ + endY * cosZ
    y2 = endY * cosX - endZ * sinX
    z2 = endY * sinX + endZ * cosX
    x2 = endX * cosY + endZ * sinY
    z2 = -1 * endX * sinY + endZ * cosY

    turtle.penup()
    turtle.goto(FOV * ((x1 + camX) / (z1 + camZ)), FOV * ((y1 + camY) / (z1 + camZ)))
    turtle.pendown()
    turtle.goto(FOV * ((x2 + camX) / (z2 + camZ)), FOV * ((y2 + camY) / (z2 + camZ)))
    if penUp:
        turtle.penup()


def goto(x, y, z):
    if tshowturtle:
        turtle.showturtle()
    else:
        turtle.hideturtle()
    x *= -1
    y *= -1
    z *= -1

    cosZ = math.cos(rotationZ)
    sinZ = math.sin(rotationZ)
    cosX = math.cos(rotationX)
    sinX = math.sin(rotationX)
    cosY = math.cos(rotationY)
    sinY = math.sin(rotationY)

    x1 = x * cosZ - y * sinX
    y1 = x * sinZ + y * cosZ
    y1 = y * cosX - z * sinX
    z1 = y * sinX + z * cosX
    x1 = x * cosY + z * sinY
    z1 = -1 * x * sinY + z * cosY

    turtle.goto(FOV * ((x1 + camX) / (z1 + camZ)), FOV * ((y1 + camY) / (z1 + camZ)))


def cube(x = 0, y = 0, z = 0, size = 10):
    size /= 2
    line(x - size, y - size, z + size, x - size, y + size, z + size)
    line(x - size, y + size, z + size, x + size, y + size, z + size)
    line(x + size, y + size, z + size, x + size, y - size, z + size)
    line(x + size, y - size, z + size, x - size, y - size, z + size)
    line(x - size, y - size, z - size, x - size, y + size, z - size)
    line(x - size, y + size, z - size, x + size, y + size, z - size)
    line(x + size, y + size, z - size, x + size, y - size, z - size)
    line(x + size, y - size, z - size, x - size, y - size, z - size)
    line(x + size, y - size, z - size, x + size, y + size, z - size)
    line(x + size, y + size, z - size, x + size, y + size, z + size)
    line(x + size, y + size, z + size, x + size, y - size, z + size)
    line(x + size, y - size, z + size, x + size, y - size, z - size)
    line(x - size, y - size, z - size, x - size, y + size, z - size)
    line(x - size, y + size, z - size, x - size, y + size, z + size)
    line(x - size, y + size, z + size, x - size, y - size, z + size)
    line(x - size, y - size, z + size, x - size, y - size, z - size)


def bgcolor(color):
    turtle.bgcolor(color)

def begin_fill():
    tfill = True
    turtle.begin_fill()

def end_fill():
    tfill = False
    turtle.end_fill()

def speed(speed):
    turtle.speed(speed)

def title(title):
    turtle.title(title)

def done():
    turtle.done()

def penup():
    turtle.penup()
    penUp = True

def pendown():
    turtle.pendown()
    penUp = False

def color(color):
    tcolor = color
    turtle.color(color)

def pensize(size):
    turtsize = size
    turtle.pensize(size)

def clear():
    turtle.clear()

def tracer(a):
    global ttracer
    ttracer = a
    turtle.tracer(a)

def update():
    turtle.update()

def Screen():
    return turtle.Screen()

def mainloop():
    turtle.mainloop()

def setup(x, y):
    turtle.setup(x, y)

def stamp():
    turtle.stamp()

def exitonclick():
    turtle.exitonclick()

def bye():
    turtle.bye()

def fillcolor(color):
    turtle.fillcolor(color)

def showturtle():
    turtle.showturtle()
    tshowturtle = True

def hideturtle():
    turtle.hideturtle()
    tshowturtle = False