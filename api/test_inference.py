from inference import FEATURE_NAMES, predict_single

sample = {
    feature: 0
    for feature in FEATURE_NAMES
}

sample["Destination Port"] = 80
sample["Flow Duration"] = 1000

result = predict_single(sample)

print(result)