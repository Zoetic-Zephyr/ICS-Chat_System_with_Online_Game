/* Battle Pong - a pong game with some extra features */
/* Copyright (C) 2003 Dana Olson                      */
/* For more info, read the LICENSE file               */

#include "init.h"

Player Players[2];
Ball PongBall;
int numPlayers(2);
int maxPlayers(2);
SDL_Surface *screen;
SDL_Surface *scoreText[2];
TTF_Font *font;
SDL_Color txtClr = { 0x00, 0x00, 0x00, 0 };
SDL_Rect src, dest;
float timeScaler(1);
int quitFlag;
int ballType(0);

int initGame()
{
    if (SDL_Init( SDL_INIT_VIDEO | SDL_INIT_AUDIO | SDL_INIT_JOYSTICK ) < 0) {
        printf("Couldn't initialize SDL: %s\n", SDL_GetError());
        return 1;
    }

    printVersion();

    if (initSound() != 0) {
      printf("Error during sound init.\n");
      return 1;
    }

    #if ICEBOXONLY || WIN32_VERSION
      SDL_ShowCursor(SDL_DISABLE);
    #endif

    SDL_WM_SetCaption("Battle Pong", "Battle Pong");

    /* Set the video mode */
#if WIN32_VERSION
    screen = SDL_SetVideoMode(SCREEN_WIDE,SCREEN_HIGH,SCREEN_DEPTH,SDL_FULLSCREEN);
    //screen = SDL_SetVideoMode(SCREEN_WIDE,SCREEN_HIGH,SCREEN_DEPTH,NULL);
#elif ICEBOXONLY
    screen = SDL_SetVideoMode(SCREEN_WIDE,SCREEN_HIGH,SCREEN_DEPTH,SDL_DOUBLEBUF|SDL_FULLSCREEN);    
#else	
    screen = SDL_SetVideoMode(SCREEN_WIDE,SCREEN_HIGH,SCREEN_DEPTH,SDL_DOUBLEBUF);
#endif	

    if (screen == NULL) {
      printf("Unable to set video mode: %s\n",SDL_GetError());
      return 1;
    }

    if (TTF_Init() < 0)
    { printf("Error initializing TTF library. %s\n",SDL_GetError());
      return 1;
    }

    font = TTF_OpenFont(FONT_NAME, 15);  //
    if ( font == NULL )
    { printf("Error loading font. %s\n", SDL_GetError());
      return 1;
    }

    printf("Found %i gamepads...\n", SDL_NumJoysticks());

    if (Players[ONE].setGamepad(ONE) != 0) {
      printf("Error setting player one gamepad.\n");
#if !ENABLE_KEYBOARD
      return 1;
#endif
    }

    if (Players[TWO].setGamepad(TWO) != 0) {
      printf("Error setting player two gamepad.\n");
#if !ENABLE_KEYBOARD
      maxPlayers=1; /* This means only one player */
#endif
    }

    #if !defined(ICEBOXONLY) || ICEBOXONLY
      /* Stop game from working if it's not Interact contollers */
      /* This is for IceBox builds, and doesn't work yet        */
    //  if (SDL_JoystickName(ONE)!="S.T.D. Interact Gaming Device") { printf("Non-IceBox game pad connected.\n"); return 1; }
    //  if ((numPlayers!=3)&&(SDL_JoystickName(TWO)!="S.T.D. Interact Gaming Device")) { printf("Non-IceBox game pad connected.\n"); return 1; }
    #endif

    printf("Player One is using a %i-button, %i-axed %s\n", SDL_JoystickNumButtons(Players[ONE].pad), SDL_JoystickNumAxes(Players[ONE].pad), SDL_JoystickName(ONE));
    if (maxPlayers!=1) { printf("Player Two is using a %i-button, %i-axed %s\n", SDL_JoystickNumButtons(Players[TWO].pad), SDL_JoystickNumAxes(Players[TWO].pad), SDL_JoystickName(TWO)); }

return 0;
}

void printVersion()
{
  SDL_version compileVersion;
  SDL_VERSION(&compileVersion);
  printf("Compiled with SDL version: %d.%d.%d\n",
    compileVersion.major,
    compileVersion.minor,
    compileVersion.patch);

#if !WIN32_VERSION
  const SDL_version *linkedVersion(SDL_Linked_Version());
  printf("Running with SDL version: %d.%d.%d\n",
    linkedVersion->major,
    linkedVersion->minor,
    linkedVersion->patch);
#endif

}

void initPlayers()
{
    /* Set up the dimensions of the player sprites */
    Players[ONE].sprDims.x=1;  Players[ONE].sprDims.y=1; Players[ONE].sprDims.w=22; Players[ONE].sprDims.h=99;
    Players[TWO].sprDims = Players[ONE].sprDims; Players[TWO].sprDims.x=25;

    /* The width and height won't change */
    Players[ONE].location.w=Players[ONE].sprDims.w; Players[ONE].location.h=Players[ONE].sprDims.h;
    Players[TWO].location.w=Players[TWO].sprDims.w; Players[TWO].location.h=Players[TWO].sprDims.h;

    /* Set the dimensions of the paddle surface for collision detection */
    /* Try modifying the x and w coords for better collision detection??? */
    Players[ONE].dims.x = 3; Players[ONE].dims.y = 13; Players[ONE].dims.w = 18; Players[ONE].dims.h = 79;
    Players[TWO].dims = Players[ONE].dims; Players[ONE].dims.x = 3; Players[ONE].dims.y = 13;

    /* Set the starting locations for the players */
    Players[ONE].location.x=1;
    Players[ONE].location.y=(SCREEN_HIGH/2)-(Players[ONE].sprDims.h/2);

    Players[TWO].location.x=SCREEN_WIDE-Players[TWO].sprDims.w-2;
    Players[TWO].location.y=(SCREEN_HIGH/2)-(Players[TWO].sprDims.h/2);

    /* Set up the dimensions of the ball sprite */
    PongBall.sprDims.x=1+(ballType*13); PongBall.sprDims.y=114; PongBall.sprDims.w=12; PongBall.sprDims.h=12;
    PongBall.location.w=PongBall.sprDims.w; PongBall.location.h=PongBall.sprDims.h;

    /* Initialize the position of the pong ball - MOVE TO SEPARATE RESET BALL FUNCTION */
    PongBall.resetBall(INITIALDELAY+1);
}

void quitGame()
{
    Mix_CloseAudio();
    SDL_Quit();
    TTF_Quit();
    printf("SDL, SDL_mixer, and TTF have been shut down.\n");
}
