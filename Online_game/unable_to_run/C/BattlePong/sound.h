/* Battle Pong - a pong game with some extra features */
/* Copyright (C) 2003 Dana Olson                      */
/* For more info, read the LICENSE file               */

#ifndef _BP_SOUND_H_
#define _BP_SOUND_H_

#include "SDL_mixer.h"
#include "gamedefs.h"

typedef struct {
  Uint8 volume;   /* 0-255                         */
  Uint8 distance; /* 0-255                         */
  Sint16 angle;   /* 0-360, 0 in front, 90 to left */
  Mix_Chunk *sample;
  int channel;
  int loops;
} SND_Data;

int initSound();
int playSound(SND_Data*);

#endif

/*

TODO

- load sample
- play it in left channel when ball hits player1
- play it in right channel when ball his player2
- load other sample
- play it in

REMEMBER

To wait for a sound to finish playing, do this:
while(Mix_Playing(-1)>0) { SDL_Delay(100); }


for the chunk size, do this:

sampling rate / 11025 = factor1
format / 8 = factor2
channels = factor3

chunksize = 256 * factor1 * factor2 * factor3

Here is a sample to play a sound:

  ///////////////////START////////////////////////
  SND_Data testdata;
  testdata.sample=Mix_LoadWAV("snd/bounce.wav");
  if(testdata.sample == NULL) {
    printf("Mix_LoadWAV error occurred: %s\n", Mix_GetError());
    return 1;
  }

  testdata.volume=255; testdata.angle=270;
  testdata.distance=0; testdata.channel=1;
  testdata.loops=0;
  if(playSound(&testdata)!=0) { printf("Mix_PlayChannel: %s\n",Mix_GetError()); }

  while(Mix_Playing(-1)>0) { SDL_Delay(100); }

  Mix_FreeChunk(testdata.sample); testdata.sample=NULL;
  ///////////////////END////////////////////////


*/
