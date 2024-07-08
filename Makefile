ifdef OS  #Deteccion de Windows 
	CC := python.exe
	FixPath = $(subst /,\,$1)
else  	  #*NIX usando GNU make
	CC := python
	FixPath = $1
endif

# Common variables
script := md2html.py
index_en_path := $(call FixPath,./en.md)
index_es_path := $(call FixPath,./es/es.md)
portfolio_en_path := $(call FixPath,./portfolio/en.md)
portfolio_es_path := $(call FixPath,./portfolio/es/es.md)
contact_en_path := $(call FixPath,./contact/en.md)
contact_es_path := $(call FixPath,./contact/es/es.md)
blog_en_path := $(call FixPath,./blog/en.md)
blog_es_path := $(call FixPath,./blog/es/es.md)
achivements_en_path := $(call FixPath,./achivements/en.md)
achivements_es_path := $(call FixPath,./achivements/es/es.md)
404_en_path := $(call FixPath,./404.md)
404_es_path := $(call FixPath,./404/es/es.md) 

all: index portfolio contact blog achivements 404

index: $(index_en_path) $(index_es_path)
	$(CC) $(call FixPath,$(script)) $(index_en_path) $(call FixPath,./index.html)
	$(CC) $(call FixPath,$(script)) $(index_es_path) $(call FixPath,./es/index.html)

portfolio: $(portfolio_en_path) $(portfolio_es_path)
	$(CC) $(call FixPath,$(script)) $(portfolio_en_path) $(call FixPath,./portfolio/index.html)
	$(CC) $(call FixPath,$(script)) $(portfolio_es_path) $(call FixPath,./portfolio/es/index.html)

contact: $(contact_en_path) $(contact_es_path)
	$(CC) $(call FixPath,$(script)) $(contact_en_path) $(call FixPath,./contact/index.html)
	$(CC) $(call FixPath,$(script)) $(contact_es_path) $(call FixPath,./contact/es/index.html)

blog: $(blog_en_path) $(blog_es_path)
	$(CC) $(call FixPath,$(script)) $(blog_en_path) $(call FixPath,./blog/index.html)
	$(CC) $(call FixPath,$(script)) $(blog_es_path) $(call FixPath,./blog/es/index.html)

achivements: $(achivements_en_path) $(achivements_es_path)
	$(CC) $(call FixPath,$(script)) $(achivements_en_path) $(call FixPath,./achivements/index.html)
	$(CC) $(call FixPath,$(script)) $(achivements_es_path) $(call FixPath,./achivements/es/index.html)

404: $(404_en_path) $(404_es_path)
	$(CC) $(call FixPath,$(script)) $(404_en_path) $(call FixPath,./404.html)
	$(CC) $(call FixPath,$(script)) $(404_es_path) $(call FixPath,./404/es/index.html)


# Clean generated files
clean:
	rm -f $(call FixPath,./index.html) $(call FixPath,./es/index.html)
	rm -f $(call FixPath,./portfolio/index.html) $(call FixPath,./portfolio/es/index.html)
	rm -f $(call FixPath,./contact/index.html) $(call FixPath,./contact/es/index.html)
	rm -f $(call FixPath,./blog/index.html) $(call FixPath,./blog/es/index.html)
	rm -f $(call FixPath,./achivements/index.html) $(call FixPath,./achivements/es/index.html)
	rm -f $(call FixPath,./404.html) $(call FixPath,./404/es/index.html)

.PHONY: all clean