import time
import json
import pandas as pd
import pyarrow.parquet as pq
from kafka import KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError


class EventsProducer:
    def __init__(self, topic_name: str, path: str, bootstrap_servers: str) -> None:
        self.topic_name = topic_name
        self.path = path
        self.bootstrap_servers = bootstrap_servers
        self.producer = None
        self.admin = None
        self._bootstrap()

    def _bootstrap(self) -> None:
        for _ in range(20):
            try:
                self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)
                self.admin = KafkaAdminClient(bootstrap_servers=self.bootstrap_servers)
                try:
                    self.topic = NewTopic(
                        name=self.topic_name, num_partitions=3, replication_factor=1
                    )
                    self.admin.create_topics([self.topic])
                except TopicAlreadyExistsError as e:
                    print(f"Topic {self.topic_name} already exists", e)
                break
            except Exception as e:
                print(f"Exception while bootstrapping: {e}")
                time.sleep(10)

    def _read_pq_into_memory(self) -> pd.DataFrame:
        return pq.read_table(self.path).to_pandas()

    def start(self):
        print("Emitting events to stream...")
        data = self._read_pq_into_memory()
        i = 1
        while True:
            for row in data.to_dict("records"):
                row["event_timestamp"] = (
                    row["event_timestamp"] + pd.Timedelta(weeks=52 * i)
                ).strftime("%Y-%m-%d %H:%M:%S")
                row["created"] = row["created"].strftime("%Y-%m-%d %H:%M:%S")
                print("Sending message: ", i)
                self.producer.send(
                    topic=self.topic_name,
                    key=str(row["driver_id"]).encode(),
                    value=json.dumps(row).encode(),
                )
                print(row)
                print("Done!")
                time.sleep(1)
            i += 1

    def teardown(self):
        try:
            self.admin.delete_topics([self.topic_name])
            print(f"Topic {self.topic_name} deleted.")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    producer = EventsProducer(
        "drivers", "driver_stats_stream.parquet", "broker_feast:29092"
    )
    try:
        producer.start()
    finally:
        producer.teardown()
