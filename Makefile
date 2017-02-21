C=iverilog
FILES=src/main.v src/half_adder.v src/full_adder.v src/adder_subtractor.v src/alu.v
OUTPUT=georgios

all:
	$(C) -o $(OUTPUT) $(FILES)

wave: all
	./$(OUTPUT)
	gtkwave dump.vcd

.PHONY: clean
clean:
	rm -f $(OUTPUT)
