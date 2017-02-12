C=iverilog
FILES=src/main.v src/half_adder.v src/full_adder.v src/alu.v
OUTPUT=georgios

all:
	$(C) -o $(OUTPUT) $(FILES)

.PHONY: clean
clean:
	rm -f $(OUTPUT)
