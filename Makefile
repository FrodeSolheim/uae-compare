all: clean
	python uae-compare.py

clean:
	rm -Rf WinUAE fs-uae PUAE
