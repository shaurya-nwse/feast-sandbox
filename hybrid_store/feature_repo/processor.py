from typing import Optional, Callable, Any, List
from dataclasses import dataclass
import pandas as pd
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import from_json, col
from pyspark.sql.avro.functions import from_avro

from feast import FeatureStore, StreamFeatureView
from feast.data_source import KafkaSource, PushMode
from feast.data_format import JsonFormat, AvroFormat


@dataclass(frozen=True)
class ProcessorConfig:
    mode: str
    spark_session: SparkSession
    processing_time: str
    query_timeout: int


class SparkProcessor:
    config: ProcessorConfig
    format: str
    preprocess_fn: Optional[Callable[[Any], Any]]
    join_keys: List[str]

    def __init__(
        self,
        *,
        fs: FeatureStore,
        sfv: StreamFeatureView,
        config: ProcessorConfig,
        preprocess_fn: Optional[Callable[[Any], Any]] = None
    ) -> None:
        assert isinstance(sfv.stream_source, KafkaSource), "Data Source is not Kafka!"
        assert isinstance(
            sfv.stream_source.kafka_options.message_format, (JsonFormat, AvroFormat)
        ), "Data format should be Json or Avro!"
        self.format = (
            "json"
            if isinstance(sfv.stream_source.kafka_options.message_format, JsonFormat)
            else "avro"
        )
        self.store = fs
        self.stream_fv = sfv
        self.spark = config.spark_session
        self.preprocess_fn = preprocess_fn
        self.query_timeout = config.query_timeout
        self.processing_time = config.processing_time
        self.join_keys = [
            self.store.get_entity(entity).join_key for entity in self.stream_fv.entities
        ]

    def ingest_stream_into_online_store(self, to: PushMode = PushMode.ONLINE) -> None:
        stream_df = self._ingest_stream_into_dataframe()
        transformed_df = self._maybe_execute_udf(stream_df)
        online_story_query = self._write_to_redis(transformed_df, to)
        return online_story_query

    def _ingest_stream_into_dataframe(self) -> DataFrame:
        if self.format == "json":
            return (
                self.spark.readStream.format("kafka")
                .option(
                    "kafka.bootstrap.servers",
                    self.stream_fv.stream_source.kafka_options.kafka_bootstrap_servers,
                )
                .option("subscribe", self.stream_fv.stream_source.kafka_options.topic)
                .option("startingOffsets", "latest")
                .load()
                .selectExpr("CAST(value AS STRING)")
                .select(
                    from_json(
                        col("value"),
                        self.stream_fv.stream_source.kafka_options.message_format.schema_json,
                    ).alias("table")
                )
                .select("table.*")
            )
        else:
            (
                self.spark.readStream.format("kafka")
                .option(
                    "kafka.bootstrap.servers",
                    self.stream_fv.stream_source.kafka_options.kafka_bootstrap_servers,
                )
                .option("subscribe", self.stream_fv.stream_source.kafka_options.topic)
                .option("startingOffsets", "latest")
                .load()
                .selectExpr("CAST(value AS STRING)")
                .select(
                    from_avro(
                        col("value"),
                        self.stream_fv.stream_source.kafka_options.message_format.schema_json,
                    ).alias("table")
                )
                .select("table.*")
            )

    def _maybe_execute_udf(self, df: DataFrame) -> DataFrame:
        return self.stream_fv.udf.__call__(df) if self.stream_fv.udf else df

    def _write_to_redis(self, df: DataFrame, to: PushMode):
        def _batch_write(row: DataFrame, epoch_id: int):
            """Only write the latest values for an entity"""
            rows: pd.DataFrame = row.toPandas()
            rows = (
                rows.sort_values(
                    by=[*self.join_keys, self.stream_fv.timestamp_field],
                    ascending=False,
                )
                .groupby(self.join_keys)
                .nth(0)
            )
            rows["created"] = pd.to_datetime("now", utc=True)
            rows = rows.reset_index()

            if self.preprocess_fn:
                rows = self.preprocess_fn(rows)

            if rows.size > 0:
                if to == PushMode.ONLINE or to == PushMode.ONLINE_AND_OFFLINE:
                    self.store.write_to_online_store(self.stream_fv.name, rows)
                if to == PushMode.OFFLINE or to == PushMode.ONLINE_AND_OFFLINE:
                    self.store.write_to_offline_store(self.stream_fv.name, rows)

        query = (
            df.writeStream.outputMode("update")
            .option("checkpointLocation", "/tmp/checkpoint/")
            .trigger(processingTime=self.processing_time)
            .foreachBatch(_batch_write)
            .start()
        )
        query.awaitTermination(timeout=self.query_timeout)
        return query
