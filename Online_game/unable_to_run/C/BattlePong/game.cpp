/* Battle Pong - a pong game with some extra features */
/* Copyright (C) 2003 Dana Olson                      */
/* For more info, read the LICENSE file               */

#include "game.h"

SDL_Surface *sprites;
SDL_Surface *bgGame;
SND_Data hitSound, wallSound;
Mix_Music *gameMusic;
int resetGame(1);

void startGame()
{
  printf("Maximum human players: %i\n", maxPlayers);

  /* If there's only one game pad, only one player can play */
#if !ENABLE_KEYBOARD
  if (maxPlayers==1) { numPlayers=1; }
#endif

  printf("Starting a %i player game.\n", numPlayers);

  if (loadImages() != 0) {
    printf("Error loading images. Aborting.\n");
    exit(1);
  }

  if (loadSounds() != 0) {
    printf("Error loading sounds. Aborting.\n");
    exit(1);
  }

  /* Set the Music volume */
  Mix_VolumeMusic(SND_MUSIC_VOL);
  /* Start playback */
  Mix_PlayMusic(gameMusic,SND_INFINITELOOP);

  quitFlag = 0;

  /* Reset all game data */
  resetAll();

  while (quitFlag==0) /* Main Game Loop */
  {
    updateInputs(); /* Update the input devices                                   */
    updateState();  /* This takes care of calling the movement routines and so on */
    checkWinConditions(); /* Duh */
    drawScreen();   /* This takes care of drawing everything onto the screen.     */
  } /* End Main Game Loop */

  /* If someone won the game, do the gameover screen */
  if (quitFlag==1) {
    /* Fade music for 4 seconds */
    Mix_FadeOutMusic(4000);
    /* Show the game over screen now */
    drawGameOver(ONE);
  } else if (quitFlag==2) {
    /* Fade music for 4 seconds */
    Mix_FadeOutMusic(4000);
    /* Show the game over screen now */
    drawGameOver(TWO);
  } else { Mix_FadeOutMusic(1000); } /* Fade music for one second */

  /* Finish playing last sound */
  while(Mix_Playing(-1)>0) { SDL_Delay(100); }

  /* Free all sound buffers */
  Mix_FreeChunk(hitSound.sample); hitSound.sample = NULL;
  Mix_FreeChunk(wallSound.sample); wallSound.sample = NULL;

  /* Free all the surfaces when we're done */
  SDL_FreeSurface(scoreText[ONE]);
  SDL_FreeSurface(scoreText[TWO]);
  SDL_FreeSurface(bgGame);
  SDL_FreeSurface(sprites);
}

void resetAll()
{
  Players[ONE].reset();
  Players[TWO].reset();
  resetGame=1; /* This fixes the TimeScaler problem I was having in updateState() */
  initPlayers(); /* This will reset the pong ball and all dimensions of player/ball sprites */
}

void checkWinConditions()
{
  if (Players[ONE].getScore()>=MAXSCORE) { quitFlag=1; }
  if (Players[TWO].getScore()>=MAXSCORE) { quitFlag=2; }
}

void updateInputs()
{
#if ENABLE_KEYBOARD
  Uint8 *keys;
  int lockFlagKb(1);
#endif
  /* Someone on IRC told me to do this because of memory leaks */
  { SDL_Event ev; while(SDL_PollEvent(&ev)); }

#if ENABLE_KEYBOARD
  SDL_PumpEvents();
  keys = SDL_GetKeyState(NULL);
#else
  SDL_JoystickUpdate(); /* Does the same as PumpEvents, but faster */
#endif

/* Keyboard movement */
#if ENABLE_KEYBOARD
  if (keys[KEY_P1_DOWN]) { Players[ONE].setSpeed(PSPEEDMAX); }
  else if (keys[KEY_P1_UP]) { Players[ONE].setSpeed(-PSPEEDMAX); }
  else { Players[ONE].setSpeed(0); }
#endif

  /* set the movement according to what is pressed on the game pad */
#if USE_HAT
  if ((SDL_JoystickGetHat(Players[ONE].pad, PADAXIS)) & (SDL_HAT_LEFTDOWN|SDL_HAT_RIGHTDOWN|SDL_HAT_DOWN)) { Players[ONE].setSpeed(PSPEEDMAX); }
  else if ((SDL_JoystickGetHat(Players[ONE].pad, PADAXIS)) & (SDL_HAT_LEFTUP|SDL_HAT_RIGHTUP|SDL_HAT_UP)) { Players[ONE].setSpeed(-PSPEEDMAX); }
#else
  if (SDL_JoystickGetAxis(Players[ONE].pad, PADAXIS)>10000) { Players[ONE].setSpeed(PSPEEDMAX); }
  else if (SDL_JoystickGetAxis(Players[ONE].pad, PADAXIS)<-10000) { Players[ONE].setSpeed(-PSPEEDMAX); }
#endif

/* if the keyboard support is enabled, then the speed shouldn't get reset */
#if !ENABLE_KEYBOARD
  else { Players[ONE].setSpeed(0); }
#endif

#if ENABLE_KEYBOARD
  static int lockKb1a;
  /* Process key presses */
  if (!PongBall.isPaused()) { /* Can't shoot until the ball moves */
    if ((lockKb1a==0)&&(keys[KEY_P1_BTN1])) {
      Players[ONE].shootBullet();
      lockKb1a=1;
    } else { if (!keys[KEY_P1_BTN1]) { lockKb1a=0; } }
  }
#endif

  static int lockBtn1a;
  /* Process button presses */
  if (!PongBall.isPaused()) { /* Can't shoot until the ball moves */
    if ((lockBtn1a==0)&&(SDL_JoystickGetButton(Players[ONE].pad, 0))) {
      Players[ONE].shootBullet();
      lockBtn1a=1;
    } else { if (!SDL_JoystickGetButton(Players[ONE].pad, 0)) { lockBtn1a=0; } }
  }

  if (numPlayers==2) /* Now do the same for player two */
  {

#if ENABLE_KEYBOARD   /* Keyboard movement */
    if (keys[KEY_P2_DOWN]) { Players[TWO].setSpeed(PSPEEDMAX); }
    else if (keys[KEY_P2_UP]) { Players[TWO].setSpeed(-PSPEEDMAX); }
    else { Players[TWO].setSpeed(0); }
#endif

#if USE_HAT
    if ((SDL_JoystickGetHat(Players[TWO].pad, PADAXIS)) & (SDL_HAT_LEFTDOWN|SDL_HAT_RIGHTDOWN|SDL_HAT_DOWN)) { Players[TWO].setSpeed(PSPEEDMAX); }
    else if ((SDL_JoystickGetHat(Players[TWO].pad, PADAXIS)) & (SDL_HAT_LEFTUP|SDL_HAT_RIGHTUP|SDL_HAT_UP)) { Players[TWO].setSpeed(-PSPEEDMAX); }
#else
    if (SDL_JoystickGetAxis(Players[TWO].pad, PADAXIS)>10000) { Players[TWO].setSpeed(PSPEEDMAX); }
    else if (SDL_JoystickGetAxis(Players[TWO].pad, PADAXIS)<-10000) { Players[TWO].setSpeed(-PSPEEDMAX); }
#endif

/* if the keyboard support is enabled, then the speed shouldn't get reset */
#if !ENABLE_KEYBOARD
    else { Players[TWO].setSpeed(0); }
#endif

#if ENABLE_KEYBOARD
    static int lockKb1b;
    /* Process key presses */
    if (!PongBall.isPaused()) { /* Can't shoot until the ball moves */
      if ((lockKb1b==0)&&(keys[KEY_P2_BTN1])) {
        Players[TWO].shootBullet();
        lockKb1b=1;
      } else { if (!keys[KEY_P2_BTN1]) { lockKb1b=0; } }
    }
#endif

    static int lockBtn1b;
    if (!PongBall.isPaused()) {
      if ((lockBtn1b==0)&&(SDL_JoystickGetButton(Players[TWO].pad, 0))) {
        Players[TWO].shootBullet();
        lockBtn1b=1;
      } else { if (!SDL_JoystickGetButton(Players[TWO].pad, 0)) { lockBtn1b=0; } }
    }
  } else { aiUpdate(); } /* Unless it's a single-player game, in which case, the AI handles it */

#if ENABLE_KEYBOARD
  /* This is essentially the same as below, only using two locks */
  static int lockBtn2a, lockBtn2b, lockKb2a, lockKb2b;
  if (PongBall.isPaused())
  {
    if (((lockBtn2a==0)&&(lockKb2a==0)) && ((SDL_JoystickGetButton(Players[ONE].pad, 1))||(keys[KEY_P1_BTN2])))
    {
      PongBall.xSpeed=BSPEEDMAX;
      lockBtn2a=1; lockKb2a=1;
    } else {
      if (!SDL_JoystickGetButton(Players[ONE].pad, 1)) { lockBtn2a=0; }
      if (!keys[KEY_P1_BTN2]) { lockKb2a=0; }
    }
    if (numPlayers==2)
    {
      if (((lockBtn2b==0)&&(lockKb2b==0)) && ((SDL_JoystickGetButton(Players[TWO].pad, 1))||(keys[KEY_P2_BTN2])))
      {
        PongBall.xSpeed=-BSPEEDMAX;
        lockBtn2b=1; lockKb2b=1;
      } else {
        if (!SDL_JoystickGetButton(Players[TWO].pad, 1)) { lockBtn2b=0; }
        if (!keys[KEY_P2_BTN2]) { lockKb2b=0; }
      }
    } else if (getRandom(100)>80) { PongBall.xSpeed=-BSPEEDMAX; } /* Random chance for AI to win draw */
  }
  if ((keys[KEY_EXIT])||(SDL_JoystickGetButton(Players[ONE].pad, SDL_JoystickNumButtons(Players[ONE].pad)-1))) { quitFlag=-1; }
#else
  static int lockBtn2a, lockBtn2b;
  /* Do the ball face off */
  if (PongBall.isPaused()) {
    if ((lockBtn2a==0)&&(SDL_JoystickGetButton(Players[ONE].pad, 1))) { /* If the lock is off and btn 2 is hit*/
      PongBall.xSpeed=BSPEEDMAX; /* Set the ball direction */
      lockBtn2a=1; /* Set the lock */
    } else { /* Remove the lock, if the button is released */
      if (!SDL_JoystickGetButton(Players[ONE].pad, 1)) { lockBtn2a=0; }
    }
    if (numPlayers==2) {
      if ((lockBtn2b==0)&&(SDL_JoystickGetButton(Players[TWO].pad, 1))) { /* If the lock is off and btn 2 is hit*/
        PongBall.xSpeed=-BSPEEDMAX; /* Set the ball direction */
        lockBtn2b=1; /* Set the lock */
      } else { /* Remove the lock, if the button is released */
        if (!SDL_JoystickGetButton(Players[TWO].pad, 1)) { lockBtn2b=0; }
      }
    } else if (getRandom(100)>80) { PongBall.xSpeed=-BSPEEDMAX; } /* Random chance for AI to win draw */
  }
  /* A way to exit the game */
  if (SDL_JoystickGetButton(Players[ONE].pad, SDL_JoystickNumButtons(Players[ONE].pad)-1)) { quitFlag=-1; }
#endif

}

void aiUpdate()
{
  int midBall = PongBall.location.y+PongBall.location.h/2;
  int midPaddle = Players[TWO].location.y+Players[TWO].location.h/2;
  int diff=abs(midPaddle-midBall);
  int movement(PSPEEDMAX);

  /* This should stop the shakey AI */
  if (diff<PSPEEDMAX) { movement=diff; }

  if (PongBall.isPaused()) {
    /* Center the paddle if the ball is stopped */
    if ((SCREEN_HIGH/2)>midPaddle) { Players[TWO].setSpeed(movement); }
    else if ((SCREEN_HIGH/2)<midPaddle) { Players[TWO].setSpeed(-movement); }
    else { Players[TWO].setSpeed(0); }
  } else {
    /* Follow the ball as closely as possible */
    if (midBall>midPaddle) { Players[TWO].setSpeed(movement); }
    else if (midBall<midPaddle) { Players[TWO].setSpeed(-movement); }
    else { Players[TWO].setSpeed(0); }
  }

  /* Replace this later with some sort of random shooter */
  if (SDL_JoystickGetButton(Players[TWO].pad, 0)) { Players[TWO].shootBullet(); }
}

void updateState()
{
  /* for keeping track of timing */
  static int lastTime(0);
  int thisTime = SDL_GetTicks();

  if (resetGame!=0) {  /* safety precaution */
    lastTime = thisTime-30;
    resetGame=0; /* Fixed the bug I had with the TimeScaler */
  }

  thisTime = SDL_GetTicks();
  timeScaler = (float)(thisTime-lastTime)/60;

  Players[ONE].move(timeScaler);
  Players[TWO].move(timeScaler);
  int result=PongBall.move(timeScaler);
  if (result>0) {
    Players[result-1].incScore();
  } else if (result<0) {
    if (playSound(&wallSound)!=0) { printf("Mix_PlayChannel: %s\n",Mix_GetError()); }
  }

  if (collisionDetectRIRmW(Players[ONE].location, PongBall.location, -PongBall.location.w, 0))
  { PongBall.bounceX((int)Players[ONE].location.x+Players[ONE].location.w);
    /* Set the angle then play the sound */
    hitSound.angle=270;
    if (playSound(&hitSound)!=0) { printf("Mix_PlayChannel: %s\n",Mix_GetError()); }
  }

  if (collisionDetectRIRmW(Players[TWO].location, PongBall.location, 0, PongBall.location.w))
  { PongBall.bounceX((int)Players[TWO].location.x-PongBall.location.w);
    /* Set the angle then play the sound */
    hitSound.angle=90;
    if (playSound(&hitSound)!=0) { printf("Mix_PlayChannel: %s\n",Mix_GetError()); }
  }

  lastTime = thisTime;
}

void drawScreen()
{
  drawBackground();
  drawHUD();
  drawPlayers();
  drawBall();
  drawBullets();
  if (PongBall.isPaused()) { drawFaceoff(); }
  SDL_Flip(screen);
}

void drawFaceoff()
{
  if (PongBall.isPaused()<=INITIALDELAY+1) {
    src.x=1; src.y=127; src.w=139; src.h=27;
  } else {
    src.x=142; src.y=127; src.w=83; src.h=27;
  }
  dest=src; dest.x=SCREEN_WIDE/2-dest.w/2; dest.y=SCREEN_HIGH-dest.h-2;
  SDL_BlitSurface(sprites, &src, screen, &dest);
}

void drawBackground()
{
  src.x=0; src.y=0; src.w=bgGame->w; src.h=bgGame->h;
  dest=src;
  SDL_BlitSurface(bgGame, &src, screen, &src);
}

void drawHUD()
{
  char numVal[12];

  /* Some guy on IRC said this would work - don't ask me */
  sprintf(numVal, "%i", Players[ONE].getScore());
  /* Print the text onto the surface now */
  scoreText[ONE] = TTF_RenderText_Solid(font,numVal,txtClr);
  dest.x = 225; dest.y = 0; dest.w = scoreText[ONE]->w; dest.h = scoreText[ONE]->h;
  SDL_BlitSurface(scoreText[ONE],NULL,screen,&dest); /* Draw player one's score */

  sprintf(numVal, "%i", Players[TWO].getScore());
  /* Print the text onto the surface now */
  scoreText[TWO] = TTF_RenderText_Solid(font,numVal,txtClr);
  dest.x = SCREEN_WIDE-dest.x-scoreText[TWO]->w; dest.y = 0; dest.w = scoreText[TWO]->w; dest.h = scoreText[TWO]->h;
  SDL_BlitSurface(scoreText[TWO],NULL,screen,&dest); /* Draw player two's score */

  /* Draw the ammo meter for Player ONE */
  src.x=1; src.y=102; src.w=10; src.h=10; dest=src; dest.y=SCR_BOT+1;
  int x;
  for (x=0; x < int(Players[ONE].getAmmo()+1/2); x++)
  { dest.x = 10+x*2; SDL_BlitSurface(sprites, &src, screen, &dest); }

  /* Draw the ammo meter for Player TWO */
  src.x=12; src.y=102; src.w=10; src.h=10; dest=src; dest.y=SCR_BOT+1;
  for (x=(Players[TWO].getAmmo()+1/2); x > 0; x--)
  { dest.x = SCREEN_WIDE-19-x*2; SDL_BlitSurface(sprites, &src, screen, &dest); }

  /* Draw the lives for Player ONE */

  /* Draw the lives for Player TWO */

}

void drawPlayers()
{
  SDL_BlitSurface(sprites, &Players[ONE].sprDims, screen, &Players[ONE].location);
  SDL_BlitSurface(sprites, &Players[TWO].sprDims, screen, &Players[TWO].location);
}

void drawBall()
{
  SDL_BlitSurface(sprites, &PongBall.sprDims, screen, &PongBall.location);
}

void drawBullets()
{

}

void drawGameOver(int playerNum)
{
  src.x=23; src.y=102; src.w=11; src.h=src.w; dest=src;
  for(int x(0); x < SCREEN_WIDE; x+=src.w)
  {
    for (int y(0); y < SCREEN_HIGH; y+=src.h)
    {
      dest.x=x;dest.y=y;
      SDL_BlitSurface(sprites, &src, screen, &dest);
    }
  }

  src.x=49; src.y=1; src.w=349; src.h=27; dest=src;
  dest.x=SCREEN_WIDE/2-dest.w/2; dest.y=SCREEN_HIGH/2-dest.h-5;
  SDL_BlitSurface(sprites, &src, screen, &dest);

  dest.h=src.h; src.y=58-(playerNum*(src.h+1));
  dest.y=SCREEN_HIGH/2+dest.h+5;
  SDL_BlitSurface(sprites, &src, screen, &dest);

  SDL_Flip(screen);
  SDL_Delay(5000);
}

int loadImages()
{
  /* Load the background PNG file */
  bgGame = IMG_Load("img/game.png");
  if (bgGame == NULL) {
    printf("Unable to load a necessary PNG file.\n");
    return 1;
  }

  /* Load the sprites PNG file */
  sprites = IMG_Load("img/game-sprites.png");
  if (sprites == NULL) {
    printf("Unable to load a necessary PNG file.\n");
    return 1;
  }
return 0;
}

int loadSounds()
{
  /* Load the sounds up into the buffers */
  hitSound.sample=Mix_LoadWAV("snd/bounce.wav");
  if(hitSound.sample == NULL) {
    printf("Mix_LoadWAV error occurred: %s\n", Mix_GetError());
    return 1;
  }
  hitSound.volume=255; hitSound.angle=0;
  hitSound.distance=0; hitSound.channel=1;
  hitSound.loops=0;

  wallSound.sample=Mix_LoadWAV("snd/bounce.wav");
  if(wallSound.sample == NULL) {
    printf("Mix_LoadWAV error occurred: %s\n", Mix_GetError());
    return 1;
  }

  wallSound.volume=255; wallSound.angle=0;
  wallSound.distance=0; wallSound.channel=2;
  wallSound.loops=0;

  /* Load the music */
  gameMusic=Mix_LoadMUS("snd/game-music.ogg");
  if(!gameMusic) {
    printf("Mix_LoadMUS() error: %s\n", Mix_GetError());
    return 1;
  }
return 0;
}
