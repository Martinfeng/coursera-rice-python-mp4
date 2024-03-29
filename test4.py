# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [0, 0]
    ball_vel[1] -= random.randrange(1,3)
    if direction == RIGHT:
        ball_vel[0] += random.randrange(2, 4)
    elif direction == LEFT:
        ball_vel[0] -= random.randrange(2, 4)


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = [HALF_PAD_WIDTH, HEIGHT / 2]
    paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2]
    paddle1_vel = [0, 0]
    paddle2_vel = [0, 0]
    score1 = 0
    score2 = 0
    spawn_ball(LEFT)

    
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS :
        ball_vel[1] = -ball_vel[1]
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if ball_pos[1] >= paddle1_pos[1] - PAD_HEIGHT/2 and ball_pos[1] <= paddle1_pos[1] + PAD_HEIGHT/2 :
            ball_vel[0] = -ball_vel[0]
        elif ball_pos[1] < paddle1_pos[1] - PAD_HEIGHT/2 or ball_pos[1] > paddle1_pos[1] + PAD_HEIGHT/2:
            score2 +=1
            ball_vel[0] = -ball_vel[0]
            ball_pos = [WIDTH / 2, HEIGHT / 2]
            spawn_ball(RIGHT)

    if ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH :
        if ball_pos[1] >= paddle2_pos[1] - PAD_HEIGHT/2 and ball_pos[1] <= paddle2_pos[1] + PAD_HEIGHT/2 :
            ball_vel[0] = -ball_vel[0]
        elif ball_pos[1] < paddle2_pos[1] - PAD_HEIGHT/2 or ball_pos[1] > paddle2_pos[1] + PAD_HEIGHT/2:
            score1 +=1
            ball_vel[0] = -ball_vel[0]
            ball_pos = [WIDTH / 2, HEIGHT / 2]
            spawn_ball(LEFT)
            

    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, 'Red', 'White')
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos[1] += paddle1_vel[1]
    paddle2_pos[1] += paddle2_vel[1]
    if paddle1_pos[1] <= PAD_HEIGHT/2 :
        paddle1_pos[1] = PAD_HEIGHT/2
    elif paddle1_pos[1] >= HEIGHT - PAD_HEIGHT/2:
        paddle1_pos[1] = HEIGHT - PAD_HEIGHT/2
    if paddle2_pos[1] <= PAD_HEIGHT/2 :
        paddle2_pos[1] = PAD_HEIGHT/2
    elif paddle2_pos[1] >= HEIGHT - PAD_HEIGHT/2:
        paddle2_pos[1] = HEIGHT - PAD_HEIGHT/2
    # draw paddles
    canvas.draw_line((paddle1_pos[0],paddle1_pos[1]-PAD_HEIGHT/2),(paddle1_pos[0],paddle1_pos[1]+PAD_HEIGHT/2),PAD_WIDTH,'Red')
    canvas.draw_line((paddle2_pos[0],paddle2_pos[1]-PAD_HEIGHT/2),(paddle2_pos[0],paddle2_pos[1]+PAD_HEIGHT/2),PAD_WIDTH,'Red')
    # draw scores
    canvas.draw_text(str(score1),(140,70),30,'White')
    canvas.draw_text(str(score2),(440,70),30,'White')
    canvas.draw_text('China',(ball_pos[0]-14,ball_pos[1]+3), 10,'Red')

    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel[1] = -10
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel[1] = 10
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel[1] = -10
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel[1] = 10
        
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel = [0,0]
    paddle2_vel = [0,0]
    
def button_handler():
    new_game()


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button = frame.add_button('Restart', button_handler)


# start frame
new_game()
frame.start()
