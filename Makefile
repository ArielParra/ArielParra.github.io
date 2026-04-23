ifdef OS
	CC := python.exe
	FixPath = $(subst /,\,$1)
else
	CC := python
	FixPath = $1
endif

script := md2html.py

all: index portfolio contact credentials 404

index:
	$(CC) $(call FixPath,$(script)) $(call FixPath,./index.md) $(call FixPath,./index.html)

portfolio:
	$(CC) $(call FixPath,$(script)) $(call FixPath,./portfolio/index.md) $(call FixPath,./portfolio/index.html)

contact:
	$(CC) $(call FixPath,$(script)) $(call FixPath,./contact/index.md) $(call FixPath,./contact/index.html)

credentials:
	$(CC) $(call FixPath,$(script)) $(call FixPath,./credentials/index.md) $(call FixPath,./credentials/index.html)

404:
	$(CC) $(call FixPath,$(script)) $(call FixPath,./404.md) $(call FixPath,./404.html)

clean:
	rm -f $(call FixPath,./index.html)
	rm -f $(call FixPath,./portfolio/index.html)
	rm -f $(call FixPath,./contact/index.html)
	rm -f $(call FixPath,./credentials/index.html)
	rm -f $(call FixPath,./404.html)

.PHONY: all clean index portfolio contact credentials 404
