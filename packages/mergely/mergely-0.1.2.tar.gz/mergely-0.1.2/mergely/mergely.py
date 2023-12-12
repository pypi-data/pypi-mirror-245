import requests
import json


class MergelyException(Exception):
    pass


class Job:
    uuid: str
    biz: str
    input_param: dict
    status: str
    model: str
    model_version: str
    webhook: str

    def __init__(self):
        self.uuid = ''
        self.biz = ''
        self.input_param = {}
        self.status = ''


    def to_dict(self):
        return {
            'uuid': self.uuid,
            'biz': self.biz,
            'input_param': self.input_param,
            'status': self.status
        }


# 定义如何序列化MyObject类的方法
def serialize(obj):
    if isinstance(obj, Job):
        return obj.to_dict()  # 或者直接使用 {'name': obj.name, 'age': obj.age}
    raise TypeError(f"Type {type(obj)} is not serializable")


END_POINT = "https://console.mergely.app/api/v3/"


class Mergely:

    def __init__(self, token):
        self.token = token
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'Application/json',
            'Accept': 'Application/json'
        }

    def submit_job(self, job: Job):
        api = END_POINT + 'job/submit'
        body = json.dumps({'job': job}, default=serialize)
        response = requests.post(api, body, headers=self.headers)
        if response.status_code != 200:
            raise MergelyException(response.text)
        return response.json()

    def query_job(self, uuid: str):
        api = END_POINT + 'job/query?uuid=' + uuid
        response = requests.get(api, headers=self.headers)
        if response.status_code != 200:
            raise MergelyException(response.text)
        return response.json()

    def batch_query_jobs(self, biz: str, status: str, page: int = 0, page_size: int = 20):
        api = END_POINT + 'job/batch/query'
        response = requests.get(api, {
            'biz': biz,
            'status': status,
            'page': page,
            'page_size': page_size
        }, headers=self.headers)
        if response.status_code != 200:
            raise MergelyException(response.text)
        return response.json()

    def cancel_job(self, uuid: str):
        api = END_POINT + 'job/cancel?uuid=' + uuid
        response = requests.get(api, headers=self.headers)
        if response.status_code != 200:
            raise MergelyException(response.text)
        return response.json()

    def report_job_result(self, uuid: str, job: dict):
        api = END_POINT + 'job/report'
        body = json.dumps({'uuid': uuid, 'job': job})
        response = requests.post(api, body, headers=self.headers)
        if response.status_code != 200:
            raise MergelyException(response.text)
        return response.json()

    def batch_report(self, jobs: []):
        api = END_POINT + 'job/batch/report'
        body = json.dumps({'jobs': jobs}, default=serialize)
        response = requests.post(api, body, headers=self.headers)
        if response.status_code != 200:
            raise MergelyException(response.text)
        return response.json()
