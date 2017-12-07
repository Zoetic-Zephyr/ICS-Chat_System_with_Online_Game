/* Battle Pong - a pong game with some extra features */
/* Copyright (C) 2003 Dana Olson                      */
/* For more info, read the LICENSE file               */

#ifndef _BP_PLAYER_H_
#define _BP_PLAYER_H_

#include <stdlib.h>
#include "SDL.h"
#include "gamedefs.h"

class Player
{
public:
    Player();
    ~Player();

    void Player::reset();
    void setWorldPos(Sint16, Sint16);
    int setGamepad(int);
    void shootBullet();
    int getAmmo();
    void move(float);
    void setSpeed(double);
    void incScore();
    int getScore();

    SDL_Joystick *pad; /* Player's gamepad            */
    SDL_Rect sprDims;  /* Dimensions of player sprite */
    SDL_Rect dims;     /* Dimensions of player ship   */
    SDL_Rect location; /* Location of player ship     */

protected:
    double speed;           /* this is a double because it can be a fraction */
    int hp;                 /* hit points */
    int ammo;               /* ammo */
    //int lives;              /* lives */
    double score;           /* player's score */
};


#endif
