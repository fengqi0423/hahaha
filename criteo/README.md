http://www.kaggle.com/c/criteo-display-ad-challenge
=========

Folders:

    .               -- Makefiles and configuration files
    src/            -- source codes
    data/           -- raw data files
    build/
        feature/    -- features built from data
        model/      -- models saved
        metric/     -- metrics of models for validation data
        val/        -- predictions for validation data
        tst/        -- predictions for test data and submission files

To train a GBRT model:

    $ make -f Makefile.xg

The metrics for the validation data will be available in the `build/metric` folder.

