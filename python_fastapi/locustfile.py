from locust import HttpUser, task, between, TaskSet
import random


class ProfileMain(HttpUser):
    wait_time = between(1, 2)

    @task(1)
    def profile_sync_select(self):
        self.client.get("/sync/select")

    @task(3)
    def profile_sync_insert(self):
        insert_num = random.randrange(0, 9999999999)
        self.client.post(f"/sync/insert/{insert_num}")

    @task(2)
    def profile_sync_delete(self):
        response = self.client.get("/sync/select")
        data = response.json()
        if select_data := data.get("data"):
            self.client.post(f"/sync/delete/{select_data[0]}")
