/* Battle Pong - a pong game with some extra features */
/* Copyright (C) 2003 Dana Olson                      */
/* For more info, read the LICENSE file               */

#include "player.h"

Player::Player()
{
}

Player::~Player()
{
}

void Player::reset()
{
    speed = 0;
    hp = 100;
    ammo = 5 * 10; /* You get 10 chances per life to kill the enemy */
    score = 0;
}

void Player::setWorldPos(Sint16 x, Sint16 y)
{
    location.x = x;
    location.y = y;
}

int Player::setGamepad(int gpNum)
{
    if (gpNum > SDL_NumJoysticks())
    {
      printf("Error in setGamepad - not enough gamepads connected.\n");
      return 1;
    }
    pad = SDL_JoystickOpen(gpNum);
    if (pad == NULL)
    {
      printf("Error opening game pad.\n");
      return 1;
    }
return 0;
}

void Player::shootBullet()
{
  if (ammo == 0) { return; }

  /* Insert bullet firing code here */
  printf("Bullet fired.\n");
  ammo--;
}

int Player::getAmmo()
{
  return ammo;
}

int Player::getScore()
{
  return (int)score;
}

void Player::move(float scaleIt)
{
  /* Move the player's coordinates */
  location.y+=Sint16(speed * scaleIt);

  /* If the player hits the top, stop movement */
  if (location.y+dims.y/2+2<=SCR_TOP)
  {
    setSpeed(0);
    location.y=SCR_TOP-dims.y/2-2;
  }

  /* If the player hits the bottom, stop movement */
  if (location.y>=SCR_BOT-sprDims.h+dims.y/2)
  {
    setSpeed(0);
    location.y=SCR_BOT-sprDims.h+dims.y/2;
  }
}

void Player::setSpeed(double i)
{
  speed = i;
}

void Player::incScore()
{
  score++;
}

