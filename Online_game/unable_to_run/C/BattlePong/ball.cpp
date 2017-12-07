/* Battle Pong - a pong game with some extra features */
/* Copyright (C) 2003 Dana Olson                      */
/* For more info, read the LICENSE file               */

#include "ball.h"

Ball::Ball()
{
    xSpeed = 0;
    ySpeed = 0;
    pause = 3;
    resetBall(3);
}

Ball::~Ball()
{
}

void Ball::setWorldPos(Sint16 x, Sint16 y)
{
    location.x = x;
    location.y = y;
}

int Ball::move(float scaleIt)
{
  pause -= (scaleIt/20.0);
  if (pause > 0) { return 0; } /* This allows the ball to freeze for a while */

  location.x+=Sint16(xSpeed * scaleIt);
  location.y+=Sint16(ySpeed * scaleIt);

  if (location.x<=0-location.w)
  {
    resetBall(5);
    //printf("Score on player 1\n");
    return 2; /* Player 2 scored a point */
  }

  if (location.x>SCREEN_WIDE+location.w)
  {
    resetBall(5);
    //printf("Score on player 2\n");
    return 1; /* Player 1 scored a point */
  }

  if (location.y < SCR_TOP) { bounceY(SCR_TOP); return -1; }
  if (location.y > (SCR_BOT-location.h-5)) { bounceY(SCR_BOT-location.h-5); return -1; }

return 0;
}

int Ball::isPaused()
{
  if (pause > 0) { return (int)pause+1; }
return 0;
}

void Ball::resetBall(int delay)
{
  /* Initialize the position of the pong ball */
  setWorldPos((SCREEN_WIDE/2)-(sprDims.w/2),(SCREEN_HIGH/2)-(sprDims.h/2));

  /* Reset the speeds */
  setSpeed(BSPEEDMAX,(double)getRandom(BSPEEDMAX)*2-BSPEEDMAX);

  /* Keep it still for a few seconds */
  pause = delay;
}

void Ball::bounceX(int offset)
{
  xSpeed=-xSpeed;
  location.x=offset;
  /* Set a random y speed */
  ySpeed=getRandom(BSPEEDMAX);
}

void Ball::bounceY(int offset)
{
  ySpeed=-ySpeed;
  location.y=offset;
}

void Ball::setSpeed(double x, double y)
{
  xSpeed = x;
  ySpeed = y;
}

