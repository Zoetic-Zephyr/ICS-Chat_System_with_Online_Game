from breakout_simple import *
# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([800, 600])

# Set the title of the window
pygame.display.set_caption('Breakout')

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

player2 = Player()
allsprites.add(player2)


# Create the ball
ball = Ball()
allsprites.add(ball)
balls.add(ball)

# The top of the block (y position)
top = 80

# Number of blocks to create
blockcount = 32
'''
We don't need to create the blocks in our game.
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
'''
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
    screen.fill(black)

    # Process the events in the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_program = True

    # Update the ball and player position as long
    # as the game is not over.
    if not game_over:
        # Update the player and ball positions
        player1.update()
        player2.update()
        game_over = ball.update()

    # If we are done, print game over
    if game_over:
        text = font.render("Game Over", True, white)
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

    # Check for collisions between the ball and the blocks
    deadblocks = pygame.sprite.spritecollide(ball, blocks, True)

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
