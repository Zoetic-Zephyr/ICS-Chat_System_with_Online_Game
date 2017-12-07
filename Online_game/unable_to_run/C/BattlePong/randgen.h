/* Battle Pong - a pong game with some extra features */
/* Copyright (C) 2003 Dana Olson                      */
/* For more info, read the LICENSE file               */

#ifndef _RANDGEN_H_
#define _RANDGEN_H_

#include <time.h>
#include "SDL.h"

void initRandom(); /* Call this to initialize the random number generator */
unsigned int getRandom(int); /* call this with a parameter to return a random number between 0 and n-1 */

#endif
