OUTPUT=georgios
SRC=vm_src

all:
	g++ -g $(SRC)/main.cpp $(SRC)/execute.cpp -o $(OUTPUT)

clean:
	rm -fr $(OUTPUT)

