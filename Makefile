all:
	cd src ; \
	zip ../Readability-for-Alfred.alfredworkflow . -r --exclude=*.DS_Store* --exclude=*.pyc*

clean:
	rm -f *.alfredworkflow