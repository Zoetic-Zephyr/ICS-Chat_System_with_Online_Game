#include "collide.h"

/* Checks centerpoint of box2 to see if it's in box1 */
int collisionDetectPIR(SDL_Rect box1, SDL_Rect box2)
{
  int midx=box2.x+(box2.w/2);
  int midy=box2.y+(box2.h/2);

  if ((midx>box1.x)&&(midx<box1.x+box1.w)&&(midy>box1.y)&&(midy<box1.y+box1.h)) return 1;

return 0;
}

/* Checks if two rectangles overlap */
int collisionDetectRIR(SDL_Rect box1, SDL_Rect box2)
{
  if ((box2.x>box1.x)&&((box1.x+box1.w)>box2.x))
    if ((box2.y>box1.y)&&((box1.y+box1.h)>box2.y)) return 1;

return 0;
}

/* Checks if two rectangles overlap w/ X and W modifiers for box1 */
int collisionDetectRIRmW(SDL_Rect box1, SDL_Rect box2, int xMod, int wMod)
{
  box1.x += xMod; box1.w += wMod; /* Apply modifiers */
  if ((box2.x>box1.x)&&((box1.x+box1.w)>box2.x))
    if ((box2.y>box1.y)&&((box1.y+box1.h)>box2.y)) return 1;

return 0;
}
