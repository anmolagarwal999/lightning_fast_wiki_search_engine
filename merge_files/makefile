CC = g++
CFLAGS =  -Wall  -g -c
LDFLAGS =
OBJFILES = merge.o utils.o
TARGET = a

all:$(TARGET)

$(TARGET): $(OBJFILES)
	$(CC) -Wall -g  $(OBJFILES) -o $(TARGET) 

merge.o: merge.cpp
	$(CC) $(CFLAGS) merge.cpp

utils.o: utils.cpp
	$(CC) $(CFLAGS) utils.cpp
