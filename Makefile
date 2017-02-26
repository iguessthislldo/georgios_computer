C := iverilog
TMP_DIR := tmp

# Adder Subtractor
ADDSUB_FILES := src/half_adder.v src/full_adder.v src/adder_subtractor.v
TEST_ADDSUB_FILES := test/test_adder_subtractor.v $(ADDSUB_FILES)
TEST_ADDSUB_OUTPUT := $(TMP_DIR)/test_addsub

FILES := src/main.v
OUTPUT=georgios

all:
	$(C) -o $(OUTPUT) $(FILES)

$(TMP_DIR):
	mkdir -p $(TMP_DIR)

.PHONY: test
test: $(TMP_DIR) $(TEST_ADDSUB_FILES)
	# Adder Subtractor
	$(C) $(TEST_ADDSUB_FILES) -o $(TEST_ADDSUB_OUTPUT)
	./$(TEST_ADDSUB_OUTPUT)

.PHONY: clean
clean:
	rm -fr $(OUTPUT) $(TMP_DIR)
