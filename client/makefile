CC = gcc
CFLAGS = -g -Wall
EXECUTABLES = bin/clique_counter bin/tuple_worker
USER_OBJS = bin/clique_counter.o bin/tuple_worker.o

all: $(EXECUTABLES)

clique_counter: bin/clique_counter.o
	$(CC) $(CFLAGS) -o bin/clique_counter bin/clique_counter.o

tuple_worker: bin/tuple_worker.o
	$(CC) $(CFLAGS) -o bin/tuple_worker bin/tuple_worker.o

bin/%.o: src/%.c  
	$(CC) $(CFLAGS) -c src/$*.c -o bin/$*.o

clean:
	rm -f bin/*.o core $(EXECUTABLES) 