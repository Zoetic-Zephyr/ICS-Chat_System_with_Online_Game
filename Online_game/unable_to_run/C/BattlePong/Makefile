CFLAGS=`sdl-config --cflags`
CFLAGS2=-W -Wall -O2 -ggdb `sdl-config --cflags`
LIBS=-lm `sdl-config --libs` -lSDL_image -lSDL_ttf -lSDL_mixer
OBJS=sound.o collide.o ball.o game.o menu.o player.o randgen.o init.o main.o
CC=g++
OUTPUT=battlepong.exe

default: clean all

PHONY: clean run default

clean:
	@echo Cleaning...
	rm -f $(OUTPUT) $(OBJS)
	rm -f *~
	@echo Done.

run: clean all
	@echo Runing...
	./$(OUTPUT)

all: $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(OUTPUT) $(LIBS)

main.o:	 main.cpp gamedefs.h randgen.h init.h menu.h game.h
	$(CC) $(CFLAGS) -c main.cpp

sound.o: sound.cpp sound.h
	$(CC) $(CFLAGS) -c sound.cpp

randgen.o: randgen.cpp randgen.h
	$(CC) $(CFLAGS) -c randgen.cpp

collide.o: collide.cpp collide.h
	$(CC) $(CFLAGS) -c collide.cpp

game.o: game.cpp game.h gamedefs.h init.h
	$(CC) $(CFLAGS) -c game.cpp

menu.o: menu.cpp menu.h gamedefs.h init.h
	$(CC) $(CFLAGS) -c menu.cpp

init.o: init.cpp init.h gamedefs.h randgen.h player.h ball.h
	$(CC) $(CFLAGS) -c init.cpp

player.o: player.cpp player.h gamedefs.h
	$(CC) $(CFLAGS) -c player.cpp

ball.o: ball.cpp ball.h gamedefs.h randgen.h collide.h player.h
	$(CC) $(CFLAGS) -c ball.cpp
