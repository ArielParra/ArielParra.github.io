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

LANGS := es fr pt
all: en_all $(LANGS) sitemap humans

en_all: index portfolio contact credentials 404

# Index
index: index.html
index.html: index.md $(script)
	$(PYTHON) $(call FixPath,$(script)) $(call FixPath,$<) $(call FixPath,$@) --lang en

# Portfolio
portfolio_md: portfolio/index.md
portfolio: portfolio/index.html
portfolio/index.html: portfolio/index.md $(script)
	$(PYTHON) $(call FixPath,$(script)) $(call FixPath,$<) $(call FixPath,$@) --lang en

portfolio/index.md: portfolio/data/projects.json scripts/manage_portfolio.py
	@echo "Generating portfolio/index.md file..."
	$(PYTHON) $(call FixPath,scripts/manage_portfolio.py) generate

# Contact
contact: contact/index.html
contact/index.html: contact/index.md $(script)
	$(PYTHON) $(call FixPath,$(script)) $(call FixPath,$<) $(call FixPath,$@) --lang en

# Credentials
credentials_md: credentials/index.md
credentials: credentials/index.html
credentials/index.html: credentials/index.md $(script)
	$(PYTHON) $(call FixPath,$(script)) $(call FixPath,$<) $(call FixPath,$@) --lang en

credentials/index.md: credentials/data/credentials.json scripts/manage_credentials.py
	@echo "Sorting credentials.json..."
	$(PYTHON) $(call FixPath,scripts/manage_credentials.py) sort
	@echo "Generating credentials/index.md file..."
	$(PYTHON) $(call FixPath,scripts/manage_credentials.py) generate

# 404
404: 404.html
404.html: 404.md $(script)
	$(PYTHON) $(call FixPath,$(script)) $(call FixPath,$<) $(call FixPath,$@) --lang en

# Other Languages
define BUILD_LANG
$(1): $(1)/index.html $(1)/portfolio/index.html $(1)/contact/index.html $(1)/credentials/index.html $(1)/404.html

$(1)/index.html: index.md $$(script)
	$$(PYTHON) $$(call FixPath,$$(script)) $$(call FixPath,$$<) $$(call FixPath,$$@) --lang $(1)

$(1)/portfolio/index.html: portfolio/index.md $$(script)
	$$(PYTHON) $$(call FixPath,$$(script)) $$(call FixPath,$$<) $$(call FixPath,$$@) --lang $(1)

$(1)/contact/index.html: contact/index.md $$(script)
	$$(PYTHON) $$(call FixPath,$$(script)) $$(call FixPath,$$<) $$(call FixPath,$$@) --lang $(1)

$(1)/credentials/index.html: credentials/index.md $$(script)
	$$(PYTHON) $$(call FixPath,$$(script)) $$(call FixPath,$$<) $$(call FixPath,$$@) --lang $(1)

$(1)/404.html: 404.md $$(script)
	$$(PYTHON) $$(call FixPath,$$(script)) $$(call FixPath,$$<) $$(call FixPath,$$@) --lang $(1)
endef

$(eval $(call BUILD_LANG,es))
$(eval $(call BUILD_LANG,fr))
$(eval $(call BUILD_LANG,pt))

# Sitemap
sitemap:
	@echo "Generating sitemap.xml..."
	$(PYTHON) $(call FixPath,scripts/generate_sitemap.py)

# Humans.txt
humans:
	@echo "Updating humans.txt..."
	$(PYTHON) $(call FixPath,scripts/update_humans.py)

clean:
	rm -f $(call FixPath,./index.html)
	rm -f $(call FixPath,./portfolio/index.html)
	rm -f $(call FixPath,./contact/index.html)
	rm -f $(call FixPath,./credentials/index.html)
	rm -f $(call FixPath,./404.html)
	rm -rf $(call FixPath,./es)
	rm -rf $(call FixPath,./fr)
	rm -rf $(call FixPath,./pt)

validate:
	$(PYTHON) $(call FixPath,scripts/validate.py)
	@echo "Running Lighthouse..."
	$(PYTHON) -m http.server 8000 & \
	PID=$$! ; \
	sleep 2 ; \
	${NPX} -y lighthouse http://localhost:8000/ --output html --output-path ./lighthouse-report.html --chrome-flags="--headless --no-sandbox" ; \
	RESULT=$$? ; \
	kill $$PID ; \
	exit $$RESULT

lint:
	${NPX} eslint "js/**/*.js"
	@echo "🎉 All JS files passed validation!"
	$(PYTHON) -m flake8 scripts/ --extend-ignore=E501
	@echo "🎉 All Python scripts passed validation!"
	$(PYTHON) $(call FixPath,scripts/validate_json.py)
	@echo "🎉 All JSON files passed validation!"
	
.PHONY: all clean en_all index portfolio_md portfolio contact credentials_md credentials 404 sitemap humans validate lint es fr pt
