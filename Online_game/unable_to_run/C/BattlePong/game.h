/* Battle Pong - a pong game with some extra features */
/* Copyright (C) 2003 Dana Olson                      */
/* For more info, read the LICENSE file               */

#ifndef _BP_GAME_H_
#define _BP_GAME_H_

#include "SDL_image.h"
#include "init.h"
#include "collide.h"

void startGame();

void drawScreen();
void drawFaceoff();
void drawBackground();
void drawHUD();
void drawPlayers();
void drawBall();
void drawBullets();
void checkWinConditions();
void drawGameOver(int);
void updateState();
void updateInputs();
void aiUpdate();
int loadImages();
int loadSounds();
void resetAll();

#endif
