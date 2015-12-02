.PHONY: all clean

all: clean final_slides.pdf

clean:
	rm -f final_slides.pdf

final_slides.pdf: final_slides.md
	pandoc -t beamer -s final_slides.md -o final_slides.pdf
