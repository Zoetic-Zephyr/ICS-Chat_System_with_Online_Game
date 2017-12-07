#ifndef _BP_COLLIDE_H_
#define _BP_COLLIDE_H_

#include <stdlib.h>
#include "SDL.h"

int collisionDetectPIR(SDL_Rect box1, SDL_Rect box2);
int collisionDetectRIR(SDL_Rect box1, SDL_Rect box2);
int collisionDetectRIRmW(SDL_Rect box1, SDL_Rect box2, int xMod, int wMod);

#endif
