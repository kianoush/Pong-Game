"""
Pong game
"""

import turtle
import os
import HandTrackingModule as htm
import cv2
import time

# Define windows and background
win = turtle.Screen()
win.title("Pong_Game")
win.bgcolor("black")
win.setup(width=800, height=600)
win.tracer(0)


# Score
score_a = 0
score_b = 0
speed = 0
Paddle_movement = 40



# Paddle A
paddle_a = turtle.Turtle()
paddle_a. speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)


# Paddle B
paddle_b = turtle.Turtle()
paddle_b. speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)


# Ball
ball = turtle.Turtle()
ball. speed(0)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 2
ball.dy = 2


# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 280)
pen.write("Player A: 0 Player B: 0", align="center", font=("Courier", 12, "normal"))



# Function
def paddle_a_up():
    y = paddle_a.ycor()
    y += Paddle_movement
    paddle_a.sety(y)

def paddle_a_down():
    y = paddle_a.ycor()
    y -= Paddle_movement
    paddle_a.sety(y)

def paddle_b_up():
    y = paddle_b.ycor()
    y += Paddle_movement
    paddle_b.sety(y)

def paddle_b_down():
    y = paddle_b.ycor()
    y -= Paddle_movement
    paddle_b.sety(y)


# keyboard binding
win.listen()
win.onkeypress(paddle_a_up, "w")
win.onkeypress(paddle_a_down, "s")

win.onkeypress(paddle_b_up, "Up")
win.onkeypress(paddle_b_down, "Down")

# webcam
wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime =0
detector = htm.handDerector(detectionCon=0.7)



# Main game loop
while True:

    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)


    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        print(lmList[2], lmList[4])

    x1, y1 = lmList[4][1], lmList[4][2]

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)),(10,30), cv2.FONT_HERSHEY_COMPLEX, .5,
            (255,0,0), 2)





    # move the ball
    win.update()
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border checking
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1

    if ball.xcor() >= 340:
        speed += 1
        if speed >= 5:
            ball.dx = ball.dx * 2
            ball.dy = ball.dy * 2
            speed = 0
            Paddle_movement += 20



    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_a += 1
        pen.clear()
        pen.write("Player A: {} Player B: {}". format(score_a, score_b), align="center", font=("Courier", 12, "normal"))
        speed = 0

    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_b += 1
        pen.clear()
        pen.write("Player A: {} Player B: {}".format(score_a, score_b), align="center", font=("Courier", 12, "normal"))
        speed = 0


        # Paddle and ball collisions
    if (ball.xcor() > 340 and ball.xcor() < 350) and (ball.ycor() < paddle_b.ycor() + 40 and ball.ycor() > paddle_b.ycor() - 40):
        ball.setx(340)
        ball.dx *= -1

    if (ball.xcor() < -340 and ball.xcor() > -350) and (ball.ycor() < paddle_a.ycor() + 40 and ball.ycor() > paddle_a.ycor() - 40):
        ball.setx(-340)
        ball.dx *= -1


    cv2.imshow("Img", img)
    cv2.waitKey(1)

    print(speed)