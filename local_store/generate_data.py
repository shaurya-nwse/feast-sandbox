import sys
from sklearn import datasets
import pandas as pd

data = datasets.load_breast_cancer()
data_df = pd.DataFrame(data=data.data, columns=data.feature_names)

# Split into arbitrary set of features
df1 = data_df[data.feature_names[:5]]
df2 = data_df[data.feature_names[5:10]]
df3 = data_df[data.feature_names[10:17]]
df4 = data_df[data.feature_names[17:30]]
target_df = pd.DataFrame(data=data.target, columns=["target"])

# Feast needs timestamps for the data
timestamps = pd.date_range(
    end=pd.Timestamp.now(), periods=len(data_df), freq="D"
).to_frame(name="event_timestamp", index=False)

# df with timestamp
df1 = pd.concat([df1, timestamps], axis=1)
df2 = pd.concat([df2, timestamps], axis=1)
df3 = pd.concat([df3, timestamps], axis=1)
df4 = pd.concat([df4, timestamps], axis=1)
target_df = pd.concat([target_df, timestamps], axis=1)

# Create ids for feature rows
patient_ids = pd.DataFrame(data=list(range(len(data_df))), columns=["patient_id"])

df1 = pd.concat([df1, patient_ids], axis=1)
df2 = pd.concat([df2, patient_ids], axis=1)
df3 = pd.concat([df3, patient_ids], axis=1)
df4 = pd.concat([df4, patient_ids], axis=1)
target_df = pd.concat([target_df, patient_ids], axis=1)

# Save to parquet
df1.to_parquet(
    engine="pyarrow",
    path="feature_repo/data/df1.parquet",
)
df2.to_parquet(
    engine="pyarrow",
    path="feature_repo/data/df2.parquet",
)
df3.to_parquet(
    engine="pyarrow",
    path="feature_repo/data/df3.parquet",
)
df4.to_parquet(
    engine="pyarrow",
    path="feature_repo/data/df4.parquet",
)
target_df.to_parquet(
    engine="pyarrow",
    path="feature_repo/data/target.parquet",
)
