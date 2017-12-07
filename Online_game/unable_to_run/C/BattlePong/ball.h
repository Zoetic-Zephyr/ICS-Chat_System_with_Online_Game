/* Battle Pong - a pong game with some extra features */
/* Copyright (C) 2003 Dana Olson                      */
/* For more info, read the LICENSE file               */

#ifndef _BP_BALL_H_
#define _BP_BALL_H_

#include <math.h>
#include "randgen.h"
#include "player.h"

class Ball
{
public:
    Ball();
    ~Ball();

    void setWorldPos(Sint16, Sint16);
    int move(float);
    void setSpeed(double, double);
    void bounceX(int);
    void bounceY(int);
    void resetBall(int);
    int isPaused();

    SDL_Rect sprDims;  /* dimensions of ball sprite                     */
    SDL_Rect location; /* location of ball                              */
    double xSpeed;     /* this is a double because it can be a fraction */
    double ySpeed;     /* this is a double because it can be a fraction */


protected:
    double pause;  /* this is the time to delay the ball */
};


#endif
