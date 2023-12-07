from datetime import datetime
import hashlib
import json
from traceback import print_exception
from typing import Any, Dict
import uuid
from delpinos.api.core.controllers import Controller
from delpinos.api.core.responses.api_response_abstract import ApiResponseAbstract


class EnqueueController(Controller):
    def add_endpoints(self):
        self.add_endpoint("/enqueue", self.enqueue, ["GET", "POST", "PUT", "DELETE"])

    def send_message(self, message: Dict[str, Any]):
        pass

    def _get_data_with_prefix(self, prefix: str, data: dict | None = None):
        if prefix is None or data is None:
            return {}

        return dict(
            {
                k[len(prefix) :]: v
                for k, v in dict(data).items()
                if v is not None and str(k).lower().startswith(prefix)
            }
        )

    def _format_header_key(self, key):
        base = []
        for parts in str(key).split("-"):
            base.append(
                parts[0].upper() + (parts[1:] if len(parts) > 1 else "").lower()
            )
        return "-".join(base)

    def _format_header(self, headers: dict):
        new_header = {}
        for key, value in headers.items():
            if value is not None:
                new_header[self._format_header_key(key)] = str(value)
        keys = list(new_header.keys())
        keys.sort()
        return {key: new_header.get(key) for key in keys}

    def _get_value(self, key, *args):
        keys = []
        if isinstance(key, str):
            keys.append(key)
        elif isinstance(key, list):
            keys = key
        else:
            return None

        def get_value(data: dict):
            for key in keys:
                value = data.get(key)
                if value is not None:
                    return value
            return None

        for data in args:
            if isinstance(data, dict):
                value = get_value(data)
                if value is not None:
                    return value
        return None

    def enqueue(self) -> ApiResponseAbstract:
        headers = {}
        request_query = self.request.query
        request_headers = self._format_header(self.request.headers)
        request_method = self.request.method
        utcnow = datetime.utcnow()
        timestamp = utcnow.strftime("%Y-%m-%dT%H:%M:%S.%f")
        unix_timestamp = utcnow.timestamp()
        headers.update(self._get_data_with_prefix("header-", request_query))
        headers.update(request_headers)
        exchange = request_headers.get("Exchange", request_query.get("exchange")) or ""
        app_id = request_headers.get("App-id", request_query.get("app_id")) or ""
        routing_key = (
            request_headers.get("Routing-Key", request_query.get("routing_key")) or ""
        )
        message_id = request_headers.get(
            "Message-Id", request_query.get("message_id")
        ) or str(uuid.uuid4())
        headers.update(
            {
                "App-id": app_id,
                "Message-Id": message_id,
                "Exchange": exchange,
                "Routing-Key": routing_key,
                "Timestamp": timestamp,
                "Unix-Timestamp": str(unix_timestamp),
                "Request-Method": request_method,
            }
        )
        headers["Authorization"] = headers.get(
            "Authorization",
            self._get_value(
                ["Authorization", "authorization"],
                self.request.headers,
                self.request.query,
            ),
        )
        response_headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Access-Control-Allow-Origin": "*",
        }
        try:
            content_type = str(headers.get("Receive-Content-Type"))
            if content_type.lower().startswith("application/x-www-form-urlencoded"):
                body = self.request.form
            elif content_type.lower().startswith("application/json"):
                body = self.request.body
            else:
                body = self.request.get_content()
            if not body:
                body = self._get_data_with_prefix("body-", self.request.query)
            if isinstance(body, dict):
                body = json.dumps(body)
                headers["Content-Type"] = "application/json; charset=utf-8"
            else:
                headers["Content-Type"] = content_type
            body = str(body)
            headers["Content-Md5"] = hashlib.md5(body.encode("utf-8")).hexdigest()
            headers["Content-Length"] = str(len(body))
            headers["Request-Query"] = json.dumps(request_query)
            headers = self._format_header(headers)
            response = {
                "id": message_id,
                "appId": app_id,
                "exchange": exchange,
                "routingKey": routing_key,
                "method": request_method,
                "headers": headers,
                "body": body,
                "timestamp": timestamp,
                "unixTimestamp": unix_timestamp,
            }
            if isinstance(body, dict):
                body = json.dumps(body)
            self.send_message(response)
            return self.response(
                status=200,
                response=response,
                headers=response_headers,
                content_type="application/json",
            )
        except Exception as e:
            print_exception(e)
            return self.response(
                status=400,
                headers=response_headers,
                content_type="application/json",
            )
