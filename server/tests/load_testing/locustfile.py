from locust import task, TaskSet, HttpUser

"""Simple load test with locust"""


class WebsiteUser(HttpUser):
    def on_start(self):
        self.client.get("root")

    # request to parse info about AM company
    @task
    def get_info(self):
        self.client.get("v1/AM/summary/")

    # request to parse info about AM company and save it to db as myComp
    @task
    def save_info(self):
        self.client.post("companies/",
                         json={
                             "name": "myComp",
                             "symbol": "AM",
                             "fields": []
                         })

    # request to delete company "myComp" from db
    @task
    def delete_info(self):
        self.client.delete("companies/",
                           json={
                               "name": "myComp",
                               "symbol": "AM",
                               "fields": []
                           })

    # min time between commands
    min_wait = 1000

    # max time between commands
    max_wait = 5000
