ifdef OS # WINDOWS
	PYTHON := python.exe
	NPX := npx.exe
	FixPath = $(subst /,\,$1)
else # NIX
	PYTHON := python
	NPX := npx
	FixPath = $1
endif

script := scripts/md2html.py

all: index portfolio contact credentials 404

# Index
index: index.html
index.html: index.md $(script)
	$(PYTHON) $(call FixPath,$(script)) $(call FixPath,$<) $(call FixPath,$@)

# Portfolio
portfolio_md: portfolio/index.md
portfolio: portfolio/index.html
portfolio/index.html: portfolio/index.md $(script)
	$(PYTHON) $(call FixPath,$(script)) $(call FixPath,$<) $(call FixPath,$@)

portfolio/index.md: portfolio/data/projects.json scripts/manage_portfolio.py
	@echo "Generating portfolio/index.md file..."
	$(PYTHON) $(call FixPath,scripts/manage_portfolio.py) generate

# Contact
contact: contact/index.html
contact/index.html: contact/index.md $(script)
	$(PYTHON) $(call FixPath,$(script)) $(call FixPath,$<) $(call FixPath,$@)

# Credentials
credentials_md: credentials/index.md
credentials: credentials/index.html
credentials/index.html: credentials/index.md $(script)
	$(PYTHON) $(call FixPath,$(script)) $(call FixPath,$<) $(call FixPath,$@)

credentials/index.md: credentials/data/credentials.json scripts/manage_credentials.py
	@echo "Sorting credentials.json..."
	$(PYTHON) $(call FixPath,scripts/manage_credentials.py) sort
	@echo "Generating credentials/index.md file..."
	$(PYTHON) $(call FixPath,scripts/manage_credentials.py) generate

# 404
404: 404.html
404.html: 404.md $(script)
	$(PYTHON) $(call FixPath,$(script)) $(call FixPath,$<) $(call FixPath,$@)

clean:
	rm -f $(call FixPath,./index.html)
	rm -f $(call FixPath,./portfolio/index.html)
	rm -f $(call FixPath,./contact/index.html)
	rm -f $(call FixPath,./credentials/index.html)
	rm -f $(call FixPath,./404.html)

validate:
	$(PYTHON) $(call FixPath,scripts/validate.py)

lint:
	${NPX} eslint "js/**/*.js"
	@echo "🎉 All JS files passed validation!"
	$(PYTHON) -m flake8 scripts/ --extend-ignore=E501
	@echo "🎉 All Python scripts passed validation!"
	$(PYTHON) $(call FixPath,scripts/validate_json.py)
	@echo "🎉 All JSON files passed validation!"
	
.PHONY: all clean index portfolio_md portfolio contact credentials_md credentials 404 validate lint
