from pprint import pprint
from feast import FeatureStore
import pandas as pd

fs = FeatureStore(
    "/Users/shaurya.rawat/Documents/mlplatform/feature-store/local_store/feature_repo"
)

pprint(
    list(map(lambda x: str(x), fs.registry.list_data_sources(project="local_store")))
)

# Get online features
serving_features = fs.get_online_features(
    features=[
        "source1_feature_view:mean radius",
        "source1_feature_view:mean texture",
        "source1_feature_view:mean perimeter",
        "source1_feature_view:mean area",
        "source1_feature_view:mean smoothness",
        "source2_feature_view:mean compactness",
        "source2_feature_view:mean concavity",
        "source2_feature_view:mean concave points",
        "source2_feature_view:mean symmetry",
        "source2_feature_view:mean fractal dimension",
        "source3_feature_view:radius error",
        "source3_feature_view:texture error",
        "source3_feature_view:perimeter error",
        "source3_feature_view:area error",
        "source3_feature_view:smoothness error",
        "source3_feature_view:compactness error",
        "source3_feature_view:concavity error",
        "source4_feature_view:concave points error",
        "source4_feature_view:symmetry error",
        "source4_feature_view:fractal dimension error",
        "source4_feature_view:worst radius",
        "source4_feature_view:worst texture",
        "source4_feature_view:worst perimeter",
        "source4_feature_view:worst area",
        "source4_feature_view:worst smoothness",
        "source4_feature_view:worst compactness",
        "source4_feature_view:worst concavity",
        "source4_feature_view:worst concave points",
        "source4_feature_view:worst symmetry",
        "source4_feature_view:worst fractal dimension",
    ],
    entity_rows=[{"patient_id": 567}, {"patient_id": 566}],
).to_dict()

pprint(serving_features)
