import random
import json
import requests.adapters
from locust import HttpUser, task, between


class FeastUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        print("Staring load test")

    def on_stop(self):
        print("Stopping load test")

    @staticmethod
    def _get_random_request():
        choices = [
            {
                "features": [
                    "zipcode_features:city",
                    "zipcode_features:state",
                    "zipcode_features:location_type",
                    "zipcode_features:tax_returns_filed",
                    "zipcode_features:population",
                    "zipcode_features:total_wages",
                    "credit_history_features:credit_card_due",
                    "credit_history_features:mortgage_due",
                    "credit_history_features:student_loan_due",
                    "credit_history_features:vehicle_loan_due",
                    "credit_history_features:hard_pulls",
                    "credit_history_features:missed_payments_2y",
                    "credit_history_features:missed_payments_1y",
                    "credit_history_features:missed_payments_6m",
                    "credit_history_features:bankruptcies",
                ],
                "entities": {"zipcode": ["92871"], "dob_ssn": ["19580608_5408"]},
            },
            {
                "features": [
                    "zipcode_features:city",
                    "zipcode_features:state",
                    "zipcode_features:location_type",
                    "zipcode_features:tax_returns_filed",
                    "zipcode_features:population",
                    "zipcode_features:total_wages",
                    "credit_history_features:credit_card_due",
                    "credit_history_features:mortgage_due",
                    "credit_history_features:student_loan_due",
                    "credit_history_features:vehicle_loan_due",
                    "credit_history_features:hard_pulls",
                    "credit_history_features:missed_payments_2y",
                    "credit_history_features:missed_payments_1y",
                    "credit_history_features:missed_payments_6m",
                    "credit_history_features:bankruptcies",
                ],
                "entities": {
                    "zipcode": [14772, 54529, 29527, 4066, 90086, 89021, 16230, 83241],
                    "dob_ssn": [
                        "19910103_1162",
                        "19630625_9081",
                        "19750328_2653",
                        "19770625_2263",
                        "19770322_3942",
                        "19940305_6239",
                        "19641204_9427",
                        "19981030_5808",
                    ],
                },
            },
            {
                "features": [
                    "zipcode_features:city",
                    "zipcode_features:state",
                    "zipcode_features:location_type",
                    "zipcode_features:tax_returns_filed",
                    "zipcode_features:population",
                    "zipcode_features:total_wages",
                ],
                "entities": {
                    "zipcode": [14772, 54529, 29527, 4066, 90086, 89021, 16230, 83241]
                },
            },
        ]
        return json.dumps(random.choice(choices))

    @task
    def get_online_features(self):
        adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
        self.client.mount("http://", adapter)
        self.client.post("/get-online-features", data=self._get_random_request())
