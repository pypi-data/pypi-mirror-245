# DOCS : https://enableapi.docs.apiary.io/#reference/security/access-tokens

import uuid
import requests
import json
import jwt
from datetime import datetime, timedelta
from dataclasses import dataclass
from Columns import Columns


@dataclass
class AuthTokenNotCreated(Exception):
    def __str__(self):
        return f"auth_token is None, get_authorisation_token must be called first"


@dataclass
class InvalidReport(Exception):
    message: str = ""

    def __str__(self):
        return f"Invalid Report Type, valid reports: [{self.message}]"
    
@dataclass
class InvalidExportColumns(Exception):
    message: str = ""

    def __str__(self):
        return f"One or more columns are invalid, valid columns: [{self.message}]"


class VirtualCollegeAPI:
    report_types = ("modules", "users", "evaluation", "event")
    report_paths = {
            "modules": "/reporting/learn/moduleAllocation",
            "users": "/reporting/core/users",
            "evaluation": "/reporting/learn/evaluationQuestion",
            "event": "/reporting/events/eventSession",
        }
    report_columns = {
            "modules": Columns.columns_module_export,
            "users": Columns.columns_user_export,
            "evaluation": Columns.columns_evaluation_export,
            "event": Columns.columns_evaluation_export,
        }
    

    def get_header(self):
        # request a new token if it has less than a minute of lifetime
        if self.expiry and self.expiry <= (datetime.now() - timedelta(0, 60)):
            self.get_access_token()
        return {
            "User-Agent": "DataReportOC/0.1",
            "Content-Type": "application/json",
            "x-api-version": "1.0",
            "x-api-nonce": uuid.uuid4().hex,
            "x-api-access-token": self.access_token,
            "x-api-language": "en-GB"
        }

    def get_request(self, path):
        res = requests.get(f"{self.domain}{path}", headers=self.get_header())
        res.raise_for_status()
        return res.text

    def post_request(self, path, body: dict):
        res = requests.post(
            f"{self.domain}{path}", headers=self.get_header(), data=json.dumps(body)
        )
        res.raise_for_status()
        return res.text

    def get_access_token(self):
        if self.auth_token is None:
            raise AuthTokenNotCreated()
        request_token = jwt.encode(self.auth_token, self.key)
        request_body = {
            "domainReference": self.instance,
            "signedAuthorisationToken": request_token,
        }
        res = self.post_request("/access-tokens/", request_body)
        res = json.loads(res)
        self.access_token = res["accessToken"]
        self.expiry = datetime.strptime(res["tokenExpiry"][:-2], "%Y-%m-%dT%H:%M:%S.%f")

    def get_authorisation_token(self):
        res = self.get_request(f"/authorisation-tokens/{self.instance}")
        self.auth_token = json.loads(res)

    def __init__(self, InstanceReference, PublicKeyAPI, APIDomain):
        self.instance = InstanceReference
        self.key = PublicKeyAPI
        self.domain = APIDomain
        self.access_token = ""
        self.expiry = None
        self.auth_token = None
        self.get_authorisation_token()
        self.get_access_token()

    def export_report(self, report_type, reportID, columns: list[str], fp):
        if report_type not in self.report_types:
            raise InvalidReport(", ".join(self.report_types))
        
        if any(map(lambda x: x not in self.report_columns[report_type], columns)):
            raise InvalidExportColumns(", ".join(self.report_columns[report_type]))

        request_body = {"columns": columns}
        data = self.post_request(
            f"{self.report_paths[report_type]}/{reportID}/export", request_body
        )

        data = json.loads(data)
        is_first_line = True
        for row in data.get("rows", {}):
            cells = row.get("cells", [])
            if cells:
                if is_first_line:
                    fp.write(",".join(map(lambda c : c["column"], cells))+"\n")
                    is_first_line = False
                fp.write(",".join(map(lambda c : c["value"], cells))+"\n")

    
    def export_add(self, report_type, name):
        if report_type not in self.report_types:
            raise InvalidReport(", ".join(self.report_types))
        
        request_body = {"name": name}
        return self.post_request(
            f"{self.report_paths[report_type]}", request_body
        )

    def list_reports(self, report_type):
        if report_type not in self.report_types:
            raise InvalidReport(", ".join(self.report_types))
            
        return self.get_request(self.report_paths[report_type])

    def search_user(self, search):
        request_body = {
            "search": search,
            "pageSize": 24,
            "pageNumber": 1,
            "order": "DateDescending",
        }
        return self.post_request("/users/search", request_body)

    def count_users(self):
        return self.get_request("/users/recentCount")
