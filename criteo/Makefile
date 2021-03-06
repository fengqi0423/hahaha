# commands
SED := sed

# directories
DIR_DATA := data
DIR_BUILD := build
DIR_SRC := src
DIR_FEATURE := $(DIR_BUILD)/feature
DIR_METRIC := $(DIR_BUILD)/metric
DIR_MODEL := $(DIR_BUILD)/model


# data files
DATA_TRN := $(DIR_DATA)/train.csv
TRN_NUMBERS := $(shell seq 0 7)
DATA_TST := $(DIR_DATA)/test.csv
DATA_TRN_SAMPLE := $(DIR_DATA)/train_sample.csv
DATA_TST_SAMPLE := $(DIR_DATA)/test_sample.csv
DATA_TRN_HEADER := $(DIR_DATA)/header.trn.txt
DATA_TRNS := $(addprefix $(DIR_DATA)/train.part.csv.,${TRN_NUMBERS})
DATA_TRN_LASTDAY := $(DIR_DATA)/train.csv.lastday

.SECONDARY: $(DATA_TRNS)

# directories for the cross validation and ensembling
DIR_VAL1 := $(DIR_BUILD)/val1
DIR_TST := $(DIR_BUILD)/tst

DIRS := $(DIR_DATA) $(DIR_BUILD) $(DIR_FEATURE) $(DIR_METRIC) $(DIR_MODEL) \
        $(DIR_VAL1) $(DIR_TST)

# data files for training and predict
SUBMISSION_SAMPLE := $(DIR_DATA)/random_submission.csv

ID_TST := $(DIR_DATA)/id.tst.txt
HEADER := $(DIR_DATA)/header.txt

# initial setup
$(DIRS):
	mkdir -p $@

$(DATA_TRN_LASTDAY): | $(DIR_DATA)
	tail -n +39291958 $(DATA_TRN).all > $@.tmp
	cat $(DATA_TRN_HEADER) $@.tmp > $@

$(DIR_DATA)/train.part.csv.%: $(DATA_TRN_HEADER) | $(DIR_DATA)
	tail -n +2 $(DATA_TRN).all | awk "NR % 8 == $* {print}"  > $@.tmp
	cat $(DATA_TRN_HEADER) $@.tmp > $@

$(DATA_TRN_SAMPLE): $(DATA_TRN) | $(DIR_DATA)
	head -n 100 $<> $@

$(DATA_TST_SAMPLE): $(DATA_TST) | $(DIR_DATA)
	head -n 100 $<> $@

$(ID_TST): $(DATA_TST)
	cut -d, -f1  $< | tail -n +2 > $@

$(HEADER): $(SUBMISSION_SAMPLE) | $(DIR_DATA)
	head -n 1 $< > $@

$(DATA_TRN_HEADER): $(DATA_TRN) | $(DIR_DATA)
	head -n 1 $< > $@

# cleanup
clean::
	find . -name '*.pyc' -delete

clobber: clean
	-rm -rf $(DIR_DATA) $(DIR_BUILD)

.PHONY: clean clobber
