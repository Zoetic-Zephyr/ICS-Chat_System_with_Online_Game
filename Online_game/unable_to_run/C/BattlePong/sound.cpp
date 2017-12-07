/* Battle Pong - a pong game with some extra features */
/* Copyright (C) 2003 Dana Olson                      */
/* For more info, read the LICENSE file               */

#include "sound.h"

int initSound()
{
  SDL_version compileVersion;
  MIX_VERSION(&compileVersion);
  printf("Compiled with SDL_mixer version: %d.%d.%d\n",
    compileVersion.major,
    compileVersion.minor,
    compileVersion.patch);

#if !WIN32_VERSION
  const SDL_version *linkedVersion(Mix_Linked_Version());
  printf("Running with SDL_mixer version: %d.%d.%d\n",
    linkedVersion->major,
    linkedVersion->minor,
    linkedVersion->patch);
#endif

  if(Mix_OpenAudio(SND_FREQUENCY, MIX_DEFAULT_FORMAT, STEREO, SND_CHUNKSIZE)==-1) {
    printf("Mix_OpenAudio error: %s\n", Mix_GetError());
    return 1;
  }

  /* Allocate the channels we want */
  Mix_AllocateChannels(SND_MAXCHANS);

return 0;
}

int playSound(SND_Data *sndSetup)
{

  Mix_Volume(sndSetup->channel,sndSetup->volume);

  if(!Mix_SetPosition(sndSetup->channel, sndSetup->angle, sndSetup->distance)) {
    printf("Mix_SetPosition: %s\n", Mix_GetError());
    return 1;
  }

  if(Mix_PlayChannel(sndSetup->channel, sndSetup->sample, sndSetup->loops)==-1)
  {
    printf("Mix_PlayChannel: %s\n",Mix_GetError());
    return 1;
  }

return 0;
}
