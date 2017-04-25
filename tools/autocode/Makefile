NAME=ac
TMP_DIR=tmp
FLEX_OUTPUT=$(TMP_DIR)/lex.yy.c
BISON_SOURCE=$(TMP_DIR)/$(NAME).tab.c
BISON_OUTPUT=$(BISON_SOURCE) $(TMP_DIR)/$(NAME).tab.h

all: $(NAME)

$(TMP_DIR):
	mkdir -p $@

$(FLEX_OUTPUT): $(TMP_DIR) src/$(NAME).l
	cd $(TMP_DIR); flex ../src/$(NAME).l

$(BISON_OUTPUT): $(TMP_DIR) src/$(NAME).y
	cd $(TMP_DIR); bison -d ../src/$(NAME).y

$(NAME): $(FLEX_OUTPUT) $(BISON_OUTPUT)
	gcc $(BISON_SOURCE) $(FLEX_OUTPUT) -lfl -o $@

clean:
	rm -fr $(NAME) $(TMP_DIR)
