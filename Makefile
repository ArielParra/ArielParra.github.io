ifdef OS
	PYTHON := python.exe
	FixPath = $(subst /,\,$1)
else
	PYTHON := python
	FixPath = $1
endif

script := scripts/md2html.py

all: index portfolio_md portfolio contact credentials_md credentials 404

index:
	$(PYTHON) $(call FixPath,$(script)) $(call FixPath,./index.md) $(call FixPath,./index.html)

portfolio_md:
	@echo "Generating portfolio/index.md file..."
	$(PYTHON) $(call FixPath,scripts/manage_portfolio.py) generate

portfolio:
	$(PYTHON) $(call FixPath,$(script)) $(call FixPath,./portfolio/index.md) $(call FixPath,./portfolio/index.html)

contact:
	$(PYTHON) $(call FixPath,$(script)) $(call FixPath,./contact/index.md) $(call FixPath,./contact/index.html)

credentials_md: 
	@echo "Sorting credentials.json..."
	$(PYTHON) $(call FixPath,scripts/manage_credentials.py) sort
	@echo "Generating credentials/index.md file..."
	$(PYTHON) $(call FixPath,scripts/manage_credentials.py) generate

credentials:
	$(PYTHON) $(call FixPath,$(script)) $(call FixPath,./credentials/index.md) $(call FixPath,./credentials/index.html)

404:
	$(PYTHON) $(call FixPath,$(script)) $(call FixPath,./404.md) $(call FixPath,./404.html)

clean:
	rm -f $(call FixPath,./index.html)
	rm -f $(call FixPath,./portfolio/index.html)
	rm -f $(call FixPath,./contact/index.html)
	rm -f $(call FixPath,./credentials/index.html)
	rm -f $(call FixPath,./404.html)

.PHONY: all clean index portfolio_md portfolio contact credentials_md credentials 404
