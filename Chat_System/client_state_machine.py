# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
from chat_utils import *
import breakout_simple as bs



class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.opponent = ''
        self.out_msg = ''
        self.s = s
        self.playerOne = True

    def set_state(self, state):
        self.state = state
        
    def get_state(self):
        return self.state
    
    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me
        
    def connect_to(self, peer):
        msg = M_CONNECT + peer
        mysend(self.s, msg)
        response = myrecv(self.s)
        if response == (M_CONNECT+'ok'):
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        elif response == (M_CONNECT + 'busy'):
            self.out_msg += 'User is busy. Please try again later\n'
        elif response == (M_CONNECT + 'hey you'):
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)

    def disconnect(self):
        msg = M_DISCONNECT
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def run_game_client(self):
        import pygame
        import math
        # Call this function so the Pygame library can initialize itself
        pygame.init()

        # Create an 800x600 sized screen
        screen = pygame.display.set_mode([400, 600])

        # Set the title of the window
        pygame.display.set_caption('Bottom line')

        # Enable this to make the mouse disappear when over our window
        pygame.mouse.set_visible(0)

        # This is a font we use to draw text on the screen (size 36)
        font = pygame.font.Font(None, 36)

        # Create a surface we can draw on
        background = pygame.Surface(screen.get_size())

        #Loop the background music
        pygame.mixer.music.load('loop.ogg')
        pygame.mixer.music.play(-1)


        # Load the sound to be played
        s_thump = pygame.mixer.Sound('thump.ogg')
        '''
        s_sidehit = pygame.mixer.Sound('sidehit.ogg')
        s_power = pygame.mixer.Sound('power.ogg')
        s_fire = pygame.mixer.Sound('fire.ogg')
        '''


        # Create sprite lists
        # blocks = pygame.sprite.Group()
        balls = pygame.sprite.Group()
        allsprites = pygame.sprite.Group()

        # Create the player paddle object
        self.me = bs.Player()
        self.opponent = bs.Player()
        # self.playerNumber = -1 or 1;
        allsprites.add(self.me)
        allsprites.add(self.opponent)

        # Create the ball

        ball = bs.Ball(self.playerOne)
        allsprites.add(ball)
        balls.add(ball)


        # Clock to limit speed
        clock = pygame.time.Clock()

        # Is the game over?
        game_over = False

        # Exit the program?
        exit_program = False
        # Main program loop
        while not exit_program:
            # print('me', self.me.rect.height, 'opponent', self.opponent.rect.height)
            # Limit to 30 fps
            clock.tick(30)

            # Clear the screen
            screen.fill(bs.white)

            # Construct the arena.
            pygame.draw.line(screen, bs.black, (0, 300), (150, 300))
            pygame.draw.circle(screen, bs.black, (200, 300), 10)
            pygame.draw.circle(screen, bs.black, (200, 300), 15, 1)
            pygame.draw.circle(screen, bs.black, (200, 300), 50, 1)
            pygame.draw.line(screen, bs.black, (250, 300), (400, 300))
            pygame.draw.rect(screen, bs.blue, (0, 570, 400, 30), 0)
            pygame.draw.rect(screen, bs.red, (0, 0, 400, 30), 0)

            health = str(ball.health)
            text = font.render(health, True, bs.black)
            textpos = text.get_rect(centerx=background.get_width() / 2)
            textpos.top = 570
            screen.blit(text, textpos)


            '''
            text = font.render("----------------------------------------", True, bs.black)
            textpos = text.get_rect(centerx=background.get_width() / 2)
            textpos.top = 300
            screen.blit(text, textpos)
            '''

            '''
            text = font.render("Instructions", True, bs.black)
            textpos = text.get_rect(centerx=background.get_width() / 2)
            textpos.top = 300
            screen.blit(text, textpos)

            textpos = text.get_rect(centerx=background.get_width() / 2)
            '''
            # pygame.draw.line(screen, bs.black, (0, 300), (400, 300), width=1)

            # Process the events in the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_program = True

            # Update the ball and player position as long
            # as the game is not over.
            if not game_over:
                # Update the player and ball positions

                #should then plot this position
                self.me.update()
                mysend(self.s, M_GAME + str(self.me.rect.x))
                got = myrecv(self.s)[1:]
                self.opponent.set_x(320 - int(got))
                game_over = ball.update()


            # If we are done, print game over
            if game_over:
                text = font.render("Game Over", True, bs.black)
                textpos = text.get_rect(centerx=background.get_width() / 2)
                textpos.top = 300
                screen.blit(text, textpos)
            '''
            # See if the ball hits the player paddle
            #here I delete the player argument
            if pygame.sprite.spritecollide(self.me, balls, False):
                # The 'diff' lets you try to bounce the ball left or right
                # depending where on the paddle you hit it
                diff1 = (self.me.rect.x + self.me.width / 2) - (ball.rect.x + ball.width / 2)
                print('diff1', diff1)

                # Set the ball's y position in case
                # we hit the ball on the edge of the paddle
                ball.rect.y = screen.get_height() - self.me.rect.height - ball.rect.height - 1
                ball.bounce(diff1)
            '''
            # See if the ball hits the player paddle
            #here I delete the player argument
            if ball.x >= self.me.rect.x and ball.x <= self.me.rect.x + self.me.rect.width:
                # if ball.y + ball.height / 2 >= self.me.rect.y:
                if ball.y + ball.height / 2 >= self.me.rect.y - 6:
                    s_thump.play()
                    # The 'diff' lets you try to bounce the ball left or right
                    # depending where on the paddle you hit it
                    diff1 = (self.me.rect.x + self.me.width / 2) - (ball.rect.x + ball.width / 2)
                    print('diff1', diff1)

                    # Set the ball's y position in case
                    # we hit the ball on the edge of the paddle
                    ball.rect.y = screen.get_height() - self.me.rect.height - ball.rect.height - 5 - 30
                    ball.bounce(diff1)

            '''
            if pygame.sprite.spritecollide(self.opponent, balls, False):
                # The 'diff' lets you try to bounce the ball left or right
                # depending where on the paddle you hit it
                diff2 = (ball.rect.x + ball.width / 2) - (self.opponent.rect.x + self.opponent.width / 2) - 2
                print('diff2', diff2)
                # Set the ball's y position in case
                # we hit the ball on the edge of the paddle
                # ball.rect.y = screen.get_height() - self.opponent.rect.height - ball.rect.height - 1
                ball.rect.y = self.opponent.rect.height + 1
                ball.bounce(diff2)
            '''
            if ball.x >= self.opponent.rect.x and ball.x <= self.opponent.rect.x + self.opponent.rect.width:
                # if ball.y - ball.height / 2 <= self.opponent.rect.y:
                if ball.y - ball.height / 2 <= self.opponent.rect.y + 6:
                    s_thump.play()
                    # The 'diff' lets you try to bounce the ball left or right
                    # depending where on the paddle you hit it
                    diff2 = (ball.rect.x + ball.width / 2) - (self.opponent.rect.x + self.opponent.width / 2) + 1
                    print('diff2', diff2)

                    # Set the ball's y position in case
                    # we hit the ball on the edge of the paddle
                    ball.rect.y = self.opponent.rect.height + 5 + 30
                    ball.bounce(diff2)
            '''
            # Check for collisions between the ball and the blocks
            deadblocks = pygame.sprite.spritecollide(ball, blocks, True)

            # If we actually hit a block, bounce the ball
            if len(deadblocks) > 0:
                ball.bounce(0)

                # Game ends if all the blocks are gone
                if len(blocks) == 0:
                    game_over = True
            '''
            # Draw Everything
            allsprites.draw(screen)

            # Flip the screen and show what we've drawn
            pygame.display.flip()

            pressed = pygame.key.get_pressed()
            exit_program = pressed[pygame.K_q]

        pygame.quit()


    def proc(self, my_msg, peer_code, peer_msg):
        # message from user is in my_msg, if it has an argument (e.g. "p 3")
        # the the argument is in my_msg[1:]
        self.out_msg = ''
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:
                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE
                    
                elif my_msg == 'time':
                    mysend(self.s, M_TIME)
                    time_in = myrecv(self.s)
                    self.out_msg += "Time is: " + time_in
                            
                elif my_msg == 'who':
                    mysend(self.s, M_LIST)
                    info = myrecv(self.s)
                    self.out_msg += 'Here are all the users in the system:\n' + info

                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer):
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to {}. Chat away!\n\n'.format(peer)
                        self.out_msg += '-'*35
                        self.out_msg += '\n\n'

                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, M_SEARCH + term)
                    result = myrecv(self.s)[1:].strip()
                    if len(result) > 0:
                        self.out_msg += 'Here is the result: ' + result + '\n\n'
                    else:
                        self.out_msg += term + 'not found\n\n'
                        
                elif my_msg[0] == 'p':
                    if my_msg[1].isdigit():
                        poem_idx = my_msg[1:].strip()
                        mysend(self.s, M_POEM + poem_idx)
                        poem = myrecv(self.s)[1:].strip()
                        if len(poem) > 0:
                            self.out_msg += 'Here is the poem you want: ' + poem + '\n\n'
                        else:
                            self.out_msg += 'No such poem\n\n'
                    elif my_msg == 'ping blah blah':
                        self.out_msg += 'pang blah blah' + '\n\n' + menu

                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                if peer_code == M_CONNECT:
                    self.peer = peer_msg
                    self.out_msg += 'Request from {0} \n'.format(self.peer)
                    self.out_msg += 'You are connect with {0}. Chat away! \n\n'.format(self.peer)
                    self.out_msg += '-'*35
                    self.out_msg += '\n'
                    self.state = S_CHATTING

#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:     # my stuff going out
                if my_msg[0:2] == '#g':
                    self.opponent = my_msg.split()[-1]
                    mysend(self.s, M_EXCHANGE + M_GAME + self.opponent)
                    self.playerOne = True
                    self.state = S_GAMING
                else:
                    print('my_msg', my_msg)
                    mysend(self.s, M_EXCHANGE + "[" + self.me + "] " + my_msg)
                    if my_msg == 'bye':
                        self.disconnect()
                        self.state = S_LOGGEDIN
                        self.peer = ''

            if len(peer_msg) > 0:    # peer's stuff, coming in
                # when peer_msg is "bye", peer_code will be M_DISCONNECT
                if peer_code == M_CONNECT:
                    self.out_msg += ('{0} joined'.format(peer_msg))
                elif peer_code == M_GAME:
                    '''
                    self.opponent = peer_msg
                    self.out_msg += 'Game challenge from {0} \n'.format(self.opponent)
                    self.out_msg += 'Have fun with {0}. Fuck him! \n\n'.format(self.opponent)
                    self.out_msg += '-' * 35
                    self.out_msg += '\n'
                    '''
                    self.playerOne = False
                    self.state = S_GAMING
                    print('I am in game mode')
                else:
                    self.out_msg += peer_msg


            # I got bumped out
            if peer_code == M_DISCONNECT:
                self.state = S_LOGGEDIN


            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu

            elif self.state == S_GAMING:
                print('now we run game')
                self.run_game_client()
                self.state = S_CHATTING

#==============================================================================
# invalid state                       
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)
            
        return self.out_msg


