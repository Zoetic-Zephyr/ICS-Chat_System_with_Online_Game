/* Battle Pong - a pong game with some extra features */
/* Copyright (C) 2003 Dana Olson                      */
/* For more info, read the LICENSE file               */

#include "SDL.h"
#include <stdlib.h>
#include "gamedefs.h"
#include "randgen.h"
#include "init.h"
#include "menu.h"
#include "game.h"

int main(int argc, char *argv[])
{
    /* set up the random seed generator */
    initRandom();

    int result;
    result = initGame();
    if (result != 0) {
      printf("Some errors occurred during initialization.\n");
      return 1;
    }

    /* Start of super main loop */
    while (numPlayers != 0)
    {
      showMenu(); /* Show menu, which sets numPlayers */
      if (numPlayers != 0) { startGame(); } /* Start the game! */
    } /* End the super main loop */

    quitGame();

    printf("Battle Pong is exiting normally.\n");
    return 0;
}
