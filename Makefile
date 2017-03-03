C := iverilog
TMP_DIR := tmp

FILES := src/main.v src/alu.v
OUTPUT=georgios

all:
	$(C) -o $(OUTPUT) $(FILES)

$(TMP_DIR):
	mkdir -p $(TMP_DIR)

.PHONY: test
test: $(TMP_DIR)
	# Nothing

.PHONY: clean
clean:
	rm -fr $(OUTPUT) $(TMP_DIR)
