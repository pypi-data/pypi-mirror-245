import os
import requests

from rmbclient.exceptions import ResourceExists, Unauthorized, ResourceNotFound, ServerInternalError


class APIRequest:
    ## TODO: 添加异常处理

    token = os.environ.get("RMB_TOKEN", "token1")
    api_url = os.environ.get("RMB_API_URL", "http://127.0.0.1:5000")
    debug = os.environ.get("RMB_DEBUG", "True").lower() == "true"

    def _handle_response(self, response, method, endpoint, data):
        if self.debug:
            print(f"Request: {method} {endpoint} with Data {data}")
            print(f"Response: {response.status_code} {response.text}")
        return response.json()


    def send(self, endpoint, method, data=None) -> dict or None:
        headers = {"Authorization": f"Bearer {self.token}"}
        url = f"{self.api_url}{endpoint}"
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError("Unsupported HTTP method")

        if response.status_code in (200, 201):
            if method == 'DELETE':
                return True
            else:
                return response.json()

        try:
            _res = response.json()
        except Exception:
            _res = str(response)

        log_record = {'response': _res, 'method': method, 'endpoint': endpoint, 'data': data}

        if response.status_code == 409:
            raise ResourceExists("Resource already exists")
        elif response.status_code == 401:
            raise Unauthorized("Unauthorized")
        elif response.status_code in (404, 403):
            raise ResourceNotFound(f"Resource not found: {log_record}")
        elif response.status_code == 500:
            raise ServerInternalError(f"Server Internal Error: {log_record}")
        elif response.status_code == 400:
            raise ValueError(f"Bad Request: {log_record}")
        else:
            raise Exception(f"Error: {log_record}")


rmb_api = APIRequest()