CC = gcc
CFLAGS = -g -Wall
MAIN = bin/main.o
EXECUTABLES = main
USER_OBJS = bin/clique_count.o bin/tuple_worker.o

all: $(EXECUTABLES)

run: $(USER_OBJS) $(MAIN)
	$(CC) $(CFLAGS) -o main $(MAIN) $(USER_OBJS)
	python Main.py

main: $(USER_OBJS) $(MAIN)
	$(CC) $(CFLAGS) -o main $(MAIN) $(USER_OBJS)

bin/%.o: %.c  
	$(CC) $(CFLAGS) -c $*.c -o bin/$*.o

clean:
	rm -f bin/*.o core $(EXECUTABLES) 