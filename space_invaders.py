#Space Invaders Game by Avi

import turtle
import os
import math
import random

#Set up game state variable
game_state = "splash"


#Set up the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")
wn.tracer(0)
wn.screensize(canvwidth=800, canvheight=800)
wn.bgpic("/Users/avi/Desktop/coding/Python/aviproject/games/turtle stuff/space invaders/images/si_bgpic.gif")

#Register the shapes
si_invader_file = "/Users/avi/Desktop/coding/Python/aviproject/games/turtle stuff/space invaders/images/si.gif"
si_shooter_file = "/Users/avi/Desktop/coding/Python/aviproject/games/turtle stuff/space invaders/images/si_shooter.gif"
start_screen_file = "/Users/avi/Desktop/coding/Python/aviproject/games/turtle stuff/space invaders/images/start_screen.gif"
si_bgpic_file = "/Users/avi/Desktop/coding/Python/aviproject/games/turtle stuff/space invaders/images/si_bgpic.gif"
si_losepic_file = "/Users/avi/Desktop/coding/Python/aviproject/games/turtle stuff/space invaders/images/lose_screen.gif"
wn.register_shape(si_invader_file)
wn.register_shape(si_shooter_file)
wn.register_shape(start_screen_file)
wn.register_shape(si_bgpic_file)
wn.register_shape(si_losepic_file)

#Define the border pen turtle
border_pen = turtle.Turtle()



#Create the player turtle
player = turtle.Turtle()
player.color("blue")
player.shape(si_shooter_file)
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)
player.shapesize(stretch_wid=50, stretch_len=50)

playerspeed = 21



#Choose a number of enemies
number_of_enemies = 30
#Create an empty list of enemies
enemies = []

#Add enemies to the list
for i in range(number_of_enemies):
    #Create the enemy
    enemies.append(turtle.Turtle())

enemy_start_x = -225
enemy_start_y = 250
enemy_number = 0

for enemy in enemies:
    enemy.color("red")
    enemy.shape(si_invader_file)
    enemy.penup()
    enemy.speed(0)
    x = enemy_start_x + (50 * enemy_number)
    y = enemy_start_y
    enemy.setposition(x, y)
    enemy.shapesize(stretch_wid=50, stretch_len=50)
    #Update the enemy number
    enemy_number += 1
    if enemy_number == 10:
        enemy_start_y -= 50
        enemy_number = 0

enemyspeed = 1

#Set the score to 0
score = 0

#Define the score pen turtle
score_pen = turtle.Turtle()



#Create the player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bulletspeed = 10

#Define bullet state
#ready = ready to fire
#fire - bullet is firing
bulletstate = "ready"

if game_state == "splash":
    player.hideturtle()
    for enemy in enemies:
        enemy.hideturtle()
    border_pen.hideturtle()
    score_pen.hideturtle()

# Game functions
#Move the player left and right
def move_left():
    x = player.xcor()
    x -= playerspeed
    if x < -280:
        x = - 280
    player.setx(x)

def move_right():
    x = player.xcor()
    x += playerspeed
    if x > 280:
        x = 280
    player.setx(x)

def fire_bullet():
    #Decalare bulletstate as a global if it needs to be changed
    global bulletstate
    if bulletstate  == "ready":
        bulletstate = "fire"
        #Move the bullet to just above the player
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()

def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    if distance < 15:
        return True
    else:
        return False

def draw_scorepen():
    #Draw score
    score_pen.speed(0)
    score_pen.color("white")
    score_pen.penup()
    score_pen.setposition(-290, 280)
    scorestring = "Score: {}".format(score)
    score_pen.write(scorestring, False, align="left", font=("Courier", 14, "normal"))
    score_pen.hideturtle()

def draw_borderpen():
    border_pen.speed(0)
    border_pen.color("white")
    border_pen.penup()
    border_pen.setposition(-300, -300)
    border_pen.pendown()
    border_pen.pensize(3)
    for side in range(4):
        border_pen.fd(600)
        border_pen.lt(90)
    border_pen.hideturtle()

def start_game():
    global game_state
    game_state = "game"
    wn.bgpic(si_bgpic_file)
    player.showturtle()
    for enemy in enemies:
        enemy.showturtle()
    if game_state == "game":
        draw_scorepen()
    if game_state == "game":
        draw_borderpen()

    print("game_started")

#Create keyboard bindings
wn.listen()
wn.onkeypress(lambda: move_left(), "Left")
wn.onkeypress(lambda: move_right(), "Right")
wn.onkeypress(lambda: fire_bullet(), "space")
wn.onkeypress(lambda: start_game(), "a")

#Main game loop
while True:
    wn.update()

    #Game code here
    if game_state == "splash":
        wn.bgpic(start_screen_file)

    if game_state == "game":
        wn.bgpic(si_bgpic_file)

        for enemy in enemies:
            #Move the enemy
            x = enemy.xcor()
            x += enemyspeed
            enemy.setx(x)

            #Move the enemy back and down
            if enemy.xcor() > 280:
                for e in enemies:
                    y = e.ycor()
                    y -= 40
                    e.sety(y)
                #Change enemy direction
                enemyspeed *= -1


            if enemy.xcor() < -280:
                for e in enemies:
                    y = e.ycor()
                    y -= 40
                    e.sety(y)
                #Change enemy direction
                enemyspeed *= -1

            #Check for a collision between the bullet and the enemy
            if isCollision(bullet, enemy):
                #Reset the bullet
                bullet.hideturtle()
                bulletstate = "ready"
                bullet.setposition(0, -400)
                #Reset the enemy
                enemy.setposition(0, 10000)
                #Update the score
                score += 10
                scorestring = "Score: {}".format(score)
                score_pen.clear()
                score_pen.write(scorestring, False, align="left", font=("Courier", 14, "normal"))

            #Check for a collision between the enemy and the player
            if isCollision(player, enemy):
                player.hideturtle()
                enemy.hideturtle()
                game_state = "you_lose"

    if game_state == "you_lose":
        wn.bgpic(si_losepic_file)
        game_state = "you_lose"
        player.hideturtle()
        for enemy in enemies:
            enemy.hideturtle()
        score_pen.hideturtle()
        border_pen.hideturtle()

        wn.onkeypress(lambda: start_game(), "a")



    #Move the bullet
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    #Check to see if the bullet has gone to the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"
