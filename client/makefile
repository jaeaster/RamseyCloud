CC = gcc
CFLAGS = -g -Wall
EXECUTABLES = RamseyC
USER_OBJS = bin/Actions.o bin/CliqueAnalyzer.o bin/MatrixAgent.o \
bin/bron.o bin/cliqueCounter.o bin/debug.o bin/io.o bin/main.o bin/prints.o \
bin/ten_clique_worker.o bin/tuples.o bin/network.o

all: $(EXECUTABLES)

$(EXECUTABLES): $(USER_OBJS)
	$(CC) $(CFLAGS) -o $(EXECUTABLES) $(USER_OBJS)

bin/%.o: src/%.c  
	$(CC) $(CFLAGS) -c src/$*.c -o bin/$*.o

clean:
	rm -f bin/*.o core $(EXECUTABLES) 