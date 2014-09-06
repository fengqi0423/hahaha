include Makefile.feature.feature2

ITER := 20
LRATE := 0.1
B := 29
CMD := ~/vowpal_wabbit/vowpalwabbit/vw
ALGO_NAME := vw_$(ITER)_$(LRATE)_$(B)

MODEL_NAME := $(ALGO_NAME)_$(FEATURE_NAME)

MODEL_TRN := $(DIR_MODEL)/$(MODEL_NAME).trn.model
MODEL_TRN1 := $(DIR_MODEL)/$(MODEL_NAME).trn1.model
MODEL_TRNS := $(MODEL_TRN) $(MODEL_TRN1)

METRIC_VAL1 := $(DIR_METRIC)/$(MODEL_NAME).val1.txt
METRIC_VALS := $(METRIC_VAL1)

PREDICT_VAL1 := $(DIR_VAL1)/$(MODEL_NAME).val1.yht
PREDICT_VALS := $(PREDICT_VAL1) $(PREDICT_VAL2)
PREDICT_TST := $(DIR_TST)/$(MODEL_NAME).tst.yht

SUBMISSION_TST := $(DIR_TST)/$(MODEL_NAME).tst.csv

all: validation submission
validation: $(METRIC_VALS)
submission: $(SUBMISSION_TST)
retrain: clean_$(ALGO_NAME) validation

$(MODEL_TRN1): $(FEATURE_VW_TRN1) | $(DIR_MODEL)
	$(CMD) -d $< -f $@ --loss_function logistic --cache_file $<.tmp \
           --passes $(ITER) -l $(LRATE) -b $(B) -P 4.0 --holdout_off
#	-rm -f $@.tmp

$(MODEL_TRN): $(FEATURE_VW_TRN) | $(DIR_MODEL)
	$(CMD) -d $< -f $@ --loss_function logistic --cache_file $<.tmp \
           --passes $(ITER) -l $(LRATE) -b $(B) -P 4.0 --holdout_off
#	-rm -f $@.tmp

$(PREDICT_VAL1): $(MODEL_TRN1) $(FEATURE_VW_VAL1) | $(DIR_VAL1)
	$(CMD) -t -i $< -d $(lastword $^) -p $@

$(PREDICT_TST): $(MODEL_TRN) $(FEATURE_VW_TST) | $(DIR_TST)
	$(CMD) -t -i $< -d $(lastword $^) -p $@

$(SUBMISSION_TST): $(PREDICT_TST) $(HEADER) $(ID_TST) | $(DIR_TST)
	paste -d, $(lastword $^) $< > $@.tmp
	cat $(word 2, $^) $@.tmp > $@
	rm $@.tmp

$(METRIC_VAL1): $(PREDICT_VAL1) $(Y_VAL1) | $(DIR_METRIC)
	python ./src/evaluate.py -t $(lastword $^) -p $< > $@
	cat $@
	
clean:: clean_$(ALGO_NAME)

clean_$(ALGO_NAME):
	-rm $(METRIC_VALS) $(SUBMISSION_TST) $(PREDICT_VALS) $(PREDICT_TST) \
        $(MODEL_TRNS)
	find . -name '*.pyc' -delete

.DEFAULT_GOAL := all
