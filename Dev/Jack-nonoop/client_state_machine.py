# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
from chat_utils import *
from breakout_simple import *
# import breakout_simple as gmst
# import subprocess


class ClientSM:

    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s
        
        # self.opponent = ''

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
        if response == (M_CONNECT + 'ok'):
            self.peer = peer
            self.out_msg += 'You are connected with ' + self.peer + '\n'
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
        # Call this function so the Pygame library can initialize itself
        pygame.init()
        # Create an 800x600 sized screen
        screen = pygame.display.set_mode([600, 800])
        # Set the title of the window
        pygame.display.set_caption('Battle_Pong')
        # Enable this to make the mouse disappear when over our window
        pygame.mouse.set_visible(0)
        # This is a font we use to draw text on the screen (size 36)
        font = pygame.font.Font(None, 36)
        # Create a surface we can draw on
        background = pygame.Surface(screen.get_size())
        # Create sprite lists
        blocks = pygame.sprite.Group()
        balls = pygame.sprite.Group()
        allsprites = pygame.sprite.Group()
        # Create the player paddle object
        player1 = Player()
        allsprites.add(player1)
        player2 = Player2()
        allsprites.add(player2)
        # Create the ball
        ball = Ball()
        allsprites.add(ball)
        balls.add(ball)
        # The top of the block (y position)
        top = 80

        # Number of blocks to create
        blockcount = 32

        # We don't need to create the blocks in our game.
        # --- Create blocks

        # Five rows of blocks
        for row in range(5):
            # 32 columns of blocks
            for column in range(0, blockcount):
                # Create a block (color,x,y)
                block = Block(blue, column * (block_width + 2) + 1, top)
                blocks.add(block)
                allsprites.add(block)
            # Move the top of the next row down
            top += block_height + 2
        # Clock to limit speed
        clock = pygame.time.Clock()
        # Is the game over?
        game_over = False
        # Exit the program?
        exit_program = False
        # Main program loop
        while not exit_program:
            # Limit to 30 fps
            clock.tick(30)
            # Clear the screen
            screen.fill(white)
            # Process the events in the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_program = True
            # Update the ball and player position as long
            # as the game is not over.
            if not game_over:
                # Update the player and ball positions
                # player2.rect.x = myrecv(self.s)
                player1.update()
                mysend(self.s, M_EXCHANGE + M_GAME + str(player1.rect.x))
                got = myrecv(self.s)[2:]
                # print(got)
                player2.set_x(525 - int(got))
                # self.opponent.update()
                game_over = ball.update()

            # If we are done, print game over
            if game_over:
                text = font.render("Game Over", True, black)
                textpos = text.get_rect(centerx=background.get_width() / 2)
                textpos.top = 300
                screen.blit(text, textpos)

            # See if the ball hits the player paddle
            if pygame.sprite.spritecollide(player1, balls, False):
                # The 'diff' lets you try to bounce the ball left or right
                # depending where on the paddle you hit it
                diff1 = (player1.rect.x + player1.width / 2) - \
                    (ball.rect.x + ball.width / 2)

                # Set the ball's y position in case
                # we hit the ball on the edge of the paddle
                ball.rect.y = screen.get_height() - player1.rect.height - ball.rect.height - 1
                ball.bounce(diff1)

            # See if the ball hits the player paddle
            if pygame.sprite.spritecollide(player2, balls, False):
                # The 'diff' lets you try to bounce the ball left or right
                # depending where on the paddle you hit it
                diff2 = (player2.rect.x + player2.width / 2) - \
                    (ball.rect.x + ball.width / 2)

                # Set the ball's y position in case
                # we hit the ball on the edge of the paddle
                ball.rect.y = screen.get_height() - player2.rect.height - ball.rect.height - 1
                ball.bounce(diff2)
            # Check for collisions between the ball and the blocks
            deadblocks = pygame.sprite.spritecollide(ball, blocks, True)

            # If we actually hit a block, bounce the ball
            if len(deadblocks) > 0:
                ball.bounce(0)

                # Game ends if all the blocks are gone
                if len(blocks) == 0:
                    game_over = True
            # Draw Everything
            allsprites.draw(screen)

            # Flip the screen and show what we've drawn
            pygame.display.flip()

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
                # print(my_msg, peer_code, peer_msg)
                if my_msg == 'q':

                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'time':
                    mysend(self.s, M_TIME)
                    time_in = myrecv(self.s)
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who':
                    # print('This is the debug way.')
                    mysend(self.s, M_LIST)
                    logged_in = myrecv(self.s)
                    self.out_msg += "All users in the system:\n"
                    self.out_msg += logged_in

                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) is True:
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                        mysend(self.s, M_CONNECT)
                        self.state = S_CHATTING
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                    '''
                    self.connect_to(peer)
                    self.state = S_CHATTING
                    '''
                    # list_in = myrecv(self.s)
                    # print(list_in)

                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, M_SEARCH + term)
                    search_rslt = myrecv(self.s)[1:].strip()
                    if len(search_rslt) > 0:
                        self.out_msg += search_rslt + '\n\n'
                    else:
                        print('search term not found')
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'

                elif my_msg[0] == 'p':
                        # unfinished
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, M_POEM + poem_idx)
                    poem = myrecv(self.s)[1:].strip()
                    if len(poem) > 0:
                        self.out_msg += poem + '\n\n'
                    else:
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'
                # elif my_msg[0] == 'g':
                #     opponent = my_msg[1:].strip()
                #     print(opponent)
                #     mysend(self.s, M_GAME + opponent)
                #     # subprocess.Popen("breakout_runner.py 1", shell=True)
                #     self.run_game_client()
                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                if peer_code == M_CONNECT:
                    self.peer = peer_msg
                    self.out_msg += 'Request from ' + self.peer + '\n'
                    self.out_msg += 'You are connected with ' + self.peer
                    self.out_msg += '. Chat away!\n\n'
                    self.out_msg += '-----------------------------------\n'
                    self.state = S_CHATTING
                '''
                elif peer_code == M_GAME:
                    self.opponent = peer_msg
                    self.out_msg += 'Game challenge from ' + self.opponent + '\n'
                    self.out_msg += 'Have fun with ' + self.opponent
                    self.out_msg += '. Fuck him!\n\n'
                    self.out_msg += '-----------------------------------\n'
                    self.state = S_GAMING
                '''

#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:     # my stuff going out
                if my_msg[0:2] == '#g':
                    mysend(self.s, M_EXCHANGE + my_msg)
                    self.state = S_GAMING
                    '''
                    print(my_msg)
                    player2 = my_msg.split()[-1]
                    print('Your opponent is:', player2 + '.','beat him!')
                    mysend(self.s, M_EXCHANGE + M_GAME + player2)
                    '''
                    # subprocess.Popen("breakout_runner.py 1", shell=True)
                else:
                    mysend(self.s, M_EXCHANGE + "[" + self.me + "] " + my_msg)
                    if my_msg == 'bye':
                        self.disconnect()
                        self.state = S_LOGGEDIN
                        self.peer = ''

            if len(peer_msg) > 0:    # peer's stuff, coming in`
                # when peer_msg is "bye", peer_code will be M_DISCONNECT
                if peer_msg[0:2] == '#g':
                    self.state = S_GAMING
                elif peer_msg == 'bye':
                    peer_code = M_DISCONNECT
                if peer_code == M_CONNECT:
                    self.out_msg += '(' + peer_msg + ' joined)\n'
                else:
                    self.out_msg += peer_msg

            # I got bumped out
            if peer_code == M_DISCONNECT:
                self.state = S_LOGGEDIN

            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu
            elif self.state == S_GAMING:
                self.run_game_client()
#==============================================================================
# invalid state
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg
