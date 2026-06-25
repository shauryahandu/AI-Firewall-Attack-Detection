from autogluon.tabular import TabularPredictor

predictor = TabularPredictor.load(
    r"models/autogluon/binary_ids/ds_sub_fit/sub_fit_ho"
)

print(
    predictor.class_labels
)