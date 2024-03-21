from locust import HttpUser, task, between, TaskSet
import random


TYPE = "sync"


class ProfileMain(HttpUser):
    wait_time = between(1, 2)

    @task(1)
    def profile_sync_select(self):
        self.client.get(f"/{TYPE}/select")

    @task(1)
    def profile_sync_insert(self):
        insert_num = random.randrange(0, 9999999999)
        self.client.post(f"/{TYPE}/insert/{insert_num}")

    @task(1)
    def profile_sync_delete(self):
        response = self.client.get(f"/{TYPE}/select")
        if response.status_code != 200:
            return

        data = response.json()
        select_data_list = data.get("data")
        if len(select_data_list) > 0:
            value = select_data_list[0]["data"]
            self.client.post(f"/{TYPE}/delete/{value}")
