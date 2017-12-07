/* Battle Pong - a pong game with some extra features */
/* Copyright (C) 2003 Dana Olson                      */
/* For more info, read the LICENSE file               */

#include "randgen.h"

static Sint32 seed = 0;

void initRandom()
{
    seed = time(NULL);
}

unsigned int getRandom(int max)
{
    /* This algorithm is provided by Loki and John Hall */
    /* in the book Programming Linux Games.             */
    Sint32 p1 = 1103515245;
    Sint32 p2 = 12345;
    seed = (seed*p1+p2) % 2147483647;
    return (unsigned)seed/3 % max;
}
