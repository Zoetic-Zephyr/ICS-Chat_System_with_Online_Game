/* Battle Pong - a pong game with some extra features */
/* Copyright (C) 2003 Dana Olson                      */
/* For more info, read the LICENSE file               */

#include "menu.h"

SDL_Surface *bgMenu;
SDL_Surface *menuOpts;

int showMenu()
{
  printf("Showing menu now\n");

  /* Load the background PNG file */
  bgMenu = IMG_Load("img/menu.png");
  if (bgMenu == NULL) {
    printf("Unable to load a necessary PNG file.\n");
    numPlayers = 0;
    return 1;
  }

  /* Load the sprites PNG file */
  menuOpts = IMG_Load("img/menu-opts.png");
  if (menuOpts == NULL) {
    printf("Unable to load a necessary PNG file.\n");
    numPlayers = 0;
    return 1;
  }

  SND_Data menuSound;
  menuSound.sample=Mix_LoadWAV("snd/menu-opt.wav");
  if(menuSound.sample == NULL) {
    printf("Unable to load a necessary sound file.\n");
    numPlayers = 0;
    return 1;
  }
  menuSound.volume=255; menuSound.angle=0;
  menuSound.distance=100; menuSound.channel=2;
  menuSound.loops=0;

  Mix_Music *menuMusic;
  //menuMusic=Mix_LoadMUS("snd/Masquerade.ogg");
  menuMusic=Mix_LoadMUS("snd/menu-music.ogg");
  if(!menuMusic) {
    printf("Mix_LoadMUS() error: %s\n", Mix_GetError());
    numPlayers = 0;
    return 1;
  }

  /* Set the Music volume */
  Mix_VolumeMusic(SND_MUSIC_VOL);
  //printf("Music volume was: %d\n", Mix_VolumeMusic(SND_MUSIC_VOL));
  printf("Music volume set to: %d\n", Mix_VolumeMusic(-1));

  /* Start playback */
  Mix_PlayMusic(menuMusic,SND_INFINITELOOP);

  src.x=0;  src.y=0;  src.w=bgMenu->w;  src.h=bgMenu->h;
  dest=src;

  SDL_BlitSurface(bgMenu, &src, screen, &dest);

  int optSel(0); /* Default option is the first one */

  switchOption(optSel);

  quitFlag = 0;
  int lockFlag(1); /* Make the default to be locked, in case the pad is held down */

#if ENABLE_KEYBOARD
  Uint8 *keys;
  int lockFlagKb(1);
#endif

  while(quitFlag==0)
  {
    /* Someone on IRC told me to do this because of memory leaks */
    { SDL_Event ev; while(SDL_PollEvent(&ev)); }

#if ENABLE_KEYBOARD
    SDL_PumpEvents();

    keys = SDL_GetKeyState(NULL);

    if ((keys[KEY_P1_BTN1])||(SDL_JoystickGetButton(Players[ONE].pad, 0)))
#else
    SDL_JoystickUpdate();

    /* if the user presses button 1                 */
    if (SDL_JoystickGetButton(Players[ONE].pad, 0))
#endif
    {
      if (optSel==0) {
        numPlayers=1;
        quitFlag=1;
      } else if (optSel==1) {
        numPlayers=2;
        quitFlag=1;
      } else {
        numPlayers=0;
        quitFlag=1;
      }
      //PLAY A SOUND HERE!!!
    }

#if ENABLE_KEYBOARD
    if ((keys[KEY_P1_BTN2])||(SDL_JoystickGetButton(Players[ONE].pad, 1))) {
#else
    /* This cycles through the secret balls (quickly) */
    if (SDL_JoystickGetButton(Players[ONE].pad, 1)) {
#endif
      ballType++;
      if (ballType>=DIFFBALLS) { ballType=0; }
    }

#if ENABLE_KEYBOARD
    if ((keys[KEY_P1_UP])||(keys[KEY_P1_DOWN]))
    {
      if (lockFlagKb==0)
      {
        lockFlagKb=1;
        if (keys[KEY_P1_DOWN]) {
          optSel++; if (optSel>2) { optSel=0; }
        } else {
            optSel--; if (optSel<0) { optSel=2; }
        }
        switchOption(optSel);
        if (playSound(&menuSound)!=0) { printf("Mix_PlayChannel: %s\n",Mix_GetError()); }
      }
    } else { lockFlagKb=0; }
#endif

    /* This cycles through the options if the axis are moved from 0 position (uses a lock) */
#if USE_HAT
    if (((SDL_JoystickGetHat(Players[ONE].pad, PADAXIS)) & (SDL_HAT_LEFTDOWN|SDL_HAT_RIGHTDOWN|SDL_HAT_DOWN))||((SDL_JoystickGetHat(Players[ONE].pad, PADAXIS)) & (SDL_HAT_LEFTUP|SDL_HAT_RIGHTUP|SDL_HAT_UP)))
    {
      if (lockFlag==0)
      {
        lockFlag=1;
        if ((SDL_JoystickGetHat(Players[ONE].pad, PADAXIS)) & (SDL_HAT_LEFTDOWN|SDL_HAT_RIGHTDOWN|SDL_HAT_DOWN)) {
#else
    if ((SDL_JoystickGetAxis(Players[ONE].pad, PADAXIS)<-10000)||(SDL_JoystickGetAxis(Players[ONE].pad, PADAXIS)>10000))
    {
      if (lockFlag==0)
      {
        lockFlag=1;
        if (SDL_JoystickGetAxis(Players[ONE].pad, PADAXIS)>0) {
#endif
          optSel++; if (optSel>2) { optSel=0; }
        } else {
            optSel--; if (optSel<0) { optSel=2; }
        }
        /* Switch menu options */
        switchOption(optSel);
        /* Play the menu sound */
        if (playSound(&menuSound)!=0) { printf("Mix_PlayChannel: %s\n",Mix_GetError()); }
      }
    } else { lockFlag=0; }

    SDL_Flip(screen);
  } /* End menu loop */

  /* Fade music for one second */
  Mix_FadeOutMusic(1000);

  /* Finish playing last sound */
  while(Mix_Playing(-1)>0) { SDL_Delay(100); }

  /* Free up resources */
  Mix_FreeChunk(menuSound.sample); menuSound.sample=NULL;
  SDL_FreeSurface(bgMenu);
  SDL_FreeSurface(menuOpts);
  printf("Exiting menu.\n");

return 0;
}

void switchOption(int option)
{
  /* x,y,h for the three source sprites, and then the
     same for the destination surface.
     w will always be menu_opts->w
     [src][option][dim]                               */
  int optDims[2][3][3]={{{0,0,32},{0,66,33},{0,132,menuOpts->h-132}},
                        {{126,157,32},{126,223,33},{126,289,menuOpts->h-132}}};

  SDL_BlitSurface(bgMenu, &dest, screen, &dest);

  src.x=optDims[0][option][0];  src.y=optDims[0][option][1];  src.w=menuOpts->w;  src.h=optDims[0][option][2];
  dest.x=optDims[1][option][0]; dest.y=optDims[1][option][1]; dest.w=menuOpts->w; dest.h=optDims[1][option][2];

  SDL_BlitSurface(menuOpts, &src, screen, &dest);
}
