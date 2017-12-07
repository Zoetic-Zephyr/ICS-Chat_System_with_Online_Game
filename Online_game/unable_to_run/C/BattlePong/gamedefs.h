/* Battle Pong - a pong game with some extra features */
/* Copyright (C) 2003 Dana Olson                      */
/* For more info, read the LICENSE file               */

#ifndef _BP_GAMEDEFS_H_
#define _BP_GAMEDEFS_H_

/* Use Interact Hammerhead FX USB game pads only? */
#define ICEBOXONLY 0

/* Compiling on Windows? */
#define WIN32_VERSION 0

/* Use hat instead of axis? */
#define USE_HAT 0

/* The axis or hat to use on the game pad */
#define PADAXIS 5

/* Enable quick and dirty keyboard support? */
#define ENABLE_KEYBOARD 1

/* if so, define the keys */
#if ENABLE_KEYBOARD
  #define KEY_P1_UP SDLK_a
  #define KEY_P1_DOWN SDLK_z
  #define KEY_P1_BTN1 SDLK_x
  #define KEY_P1_BTN2 SDLK_c
    #define KEY_EXIT SDLK_ESCAPE
  #define KEY_P2_UP SDLK_KP4
  #define KEY_P2_DOWN SDLK_KP1
  #define KEY_P2_BTN1 SDLK_KP2
  #define KEY_P2_BTN2 SDLK_KP3
#endif

/* Sound settings */
#define STEREO 2
#define MONO 1
#define SND_FREQUENCY 44100
#define SND_FORMAT 16
#define SND_CHUNKSIZE 4096
#define SND_NEXTCHAN -1
#define SND_MAXCHANS 4
#define SND_INFINITELOOP -1
#define SND_NOLOOP 0
#define SND_MUSIC_VOL 64

/* We can use PI in our forumulas with this. */
#define PI (3.141592654F)

/* these are to use for the players */
#define ONE 0
#define TWO 1

/* Paddle and ball speeds */
#define PSPEEDMAX 20
#define BSPEEDMAX 25

/* Initial ball pause */
#define INITIALDELAY 2

/* End game after this score */
#define MAXSCORE 5

/* Number of different pong balls */
#define DIFFBALLS 4

/* Screen size */
#define SCREEN_WIDE 640
#define SCREEN_HIGH 480

/* Screen depth */
#define SCREEN_DEPTH 32

/* Top and bottom screen limits */
#define SCR_TOP 14
#define SCR_BOT SCREEN_HIGH-14

/* This is the font to use */
#define FONT_NAME "img/hyperfont.ttf"

#endif
