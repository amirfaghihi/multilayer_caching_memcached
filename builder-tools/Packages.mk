LIBS := $(shell for pkg in `grep -o '"\.\.\/.*"' ./pyproject.toml | sed -e 's/"//g'`; do echo $$pkg; done)
WHEELS := $(LIBS:%=%/dist/*.whl)
BUILD_DIR := ../dist

.PHONY: all clean

all: $(BUILD_DIR)/*.whl

clean:
	-rm $(WHEELS) $(BUILD_DIR)/*.whl

reset: clean
	-rm -rf .venv poetry.lock dist
	/home/amir/.local/bin/poetry install

$(BUILD_DIR)/deps: 
	mkdir -p $(BUILD_DIR)/deps

$(WHEELS): $(BUILD_DIR)/deps 
	mkdir -p $(@D)
	cd $(@D)/../ && /home/amir/.local/bin/poetry build
	cp $@ ${BUILD_DIR}/deps/.

$(BUILD_DIR)/%.whl: $(BUILD_DIR)/deps/*.whl
	/home/amir/.local/bin/poetry build

$(BUILD_DIR)/deps/%.whl: $(WHEELS)
	@echo $@ > /dev/null



