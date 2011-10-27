BARCODE:=	/home/mjd/rpmbuild/BUILD/barcode-0.98/barcode
ENCODING:=	128b
UNITS:=		mm
ROWS:=		26
COLS:=		5
LMARG:=		3
RMARG:=		$(LMARG)
TMARG:=		12
BMARG:=		11
# Internal white area surrounding each barcode
MARGIN:=	5,1
# PAGE:=		297x210 # Defaults to A4, so not necessary
START:=		1000

TABLE:=		$(COLS)x$(ROWS)+$(LMARG)+$(BMARG)-$(RMARG)-$(TMARG)
COUNT:=		$(shell expr $(COLS) '*' $(ROWS))
END:=		$(shell expr $(START) + $(COUNT) - 1)
PREFIX:=	%AFD

all: barcode.ps

barcode.txt:
	seq -w $(START) $(END) | sed -e 's/^/$(PREFIX)/g' > $@

barcode-tmp.ps: barcode.txt
	$(BARCODE) $(strip $(if $(ENCODING),-e $(ENCODING)) $(if $(UNITS),-u $(UNITS)) $(if $(GEOM),-g $(GEOM)) $(if $(MARGIN),-m $(MARGIN)) $(if $(PAGE),-p $(PAGE)) -t $(TABLE)) -i $< -o $@

frame.ps: frame.py
	./$< > $@

barcode.ps: frame.ps barcode-tmp.ps
	grep -v '^%#' < $< | gawk '$$0~/^% INSERT-POINT$$/{while((getline<"barcode-tmp.ps")){if($$1=="showpage")break;if($$0~/^% Printing/)P=1;if(P==1)print}close("barcode-tmp.ps");next}{print}' > $@

.PHONY: clean
clean:
	-rm -f barcode.txt barcode-tmp.ps frame.ps barcode.ps 
