/* Battle Pong - a pong game with some extra features */
/* Copyright (C) 2003 Dana Olson                      */
/* For more info, read the LICENSE file               */

#ifndef _BP_INIT_H_
#define _BP_INIT_H_

#include <stdlib.h>
#include "SDL.h"
#include "SDL_ttf.h"
#include "randgen.h"
#include "sound.h"
#include "player.h"
#include "ball.h"

int initGame();
void printVersion();
void initPlayers();
void quitGame();

/* Global variables */
extern Player Players[2];
extern Ball PongBall;
extern int numPlayers;
extern int maxPlayers;
extern SDL_Surface *screen;
extern SDL_Surface *scoreText[2];
extern TTF_Font *font;
extern SDL_Color txtClr;
extern SDL_Rect src, dest;
extern SDL_Event event;
extern float timeScaler;
extern int quitFlag;
extern int ballType;

#endif
