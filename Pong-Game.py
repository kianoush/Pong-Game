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
ball.dx = 3
ball.dy = 3

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 280)
pen.write("Player A: 0 Player B: 0", align="center", font=("Courier", 12, "normal"))



# Function
def paddle_a_movement(y):
    paddle_a.sety(y)

def paddle_b_movement(y):
    paddle_b.sety(y)


# webcam
wCam, hCam = 800, 600

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime =0
detector = htm.HandDetector(detectionCon=0.7)

# Main game loop
while True:

    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img, draw=True)

    lmList = detector.findPosition(img, handNo=0, draw=True)
    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        print(lmList[4][1], lmList[4][2])

        if y1 <= 225:
            y1 = 275 - y1
        else:
            y1 = - (y1 - 275)

        if x1 <= 400:
            paddle_a_movement(y1)
        else:
            paddle_b_movement(y1)

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
        # if speed >= 5:
        #     ball.dx = ball.dx * 2
        #     ball.dy = ball.dy * 2
        #     speed = 0
        #     Paddle_movement += 20



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

    #print(speed)