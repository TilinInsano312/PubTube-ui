"""Verify real Gateway metrics through Prometheus and provisioned Grafana.

Run from the repository root with GRAFANA_ADMIN_PASSWORD in the environment.
This check sends only safe health requests; it does not change configuration.
"""

from __future__ import annotations

import base64
import json
import math
import os
from pathlib import Path
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def get(url: str, authorization: str | None = None) -> dict:
    headers = {"Authorization": authorization} if authorization else {}
    with urlopen(Request(url, headers=headers), timeout=5) as response:
        return json.load(response)


def query(base: str, expression: str, authorization: str | None = None) -> list:
    response = get(base + "/api/v1/query?" + urlencode({"query": expression}), authorization)
    if response.get("status") != "success":
        raise ValueError("Prometheus query did not succeed")
    series = response["data"]["result"]
    if not series or not all(math.isfinite(float(item["value"][1])) for item in series):
        raise ValueError("Query has no finite samples yet")
    return series


def verify() -> None:
    password = os.environ.get("GRAFANA_ADMIN_PASSWORD")
    if not password:
        raise ValueError("Set GRAFANA_ADMIN_PASSWORD in the environment")
    user = os.environ.get("GRAFANA_ADMIN_USER", "admin")
    authorization = "Basic " + base64.b64encode(f"{user}:{password}".encode()).decode()
    gateway = os.environ.get("GATEWAY_URL", "http://localhost:8000").rstrip("/")
    prometheus = os.environ.get("PROMETHEUS_URL", "http://localhost:9090").rstrip("/")
    grafana = os.environ.get("GRAFANA_URL", "http://localhost:3000").rstrip("/")
    source = json.loads((Path(__file__).resolve().parents[2] /
                         "observability/grafana/dashboards/pubtube-gateway.json").read_text(encoding="utf-8"))
    for _ in range(3):
        get(gateway + "/api/health")
    print("PASS Gateway health (3 safe requests)", flush=True)
    with urlopen(prometheus + "/-/healthy", timeout=5) as response:
        if response.status != 200:
            raise ValueError("Prometheus is not healthy")
    print("PASS Prometheus health", flush=True)
    targets = get(prometheus + "/api/v1/targets")["data"]["activeTargets"]
    if not any(target["labels"].get("job") == "pubtube-gateway" and target["health"] == "up"
               for target in targets):
        raise ValueError("pubtube-gateway target is not UP")
    print("PASS Prometheus target pubtube-gateway UP", flush=True)
    health = get(grafana + "/api/health")
    if health.get("database") != "ok":
        raise ValueError("Grafana database is not healthy")
    print("PASS Grafana health, version " + health.get("version", "unknown"), flush=True)
    datasource = get(grafana + "/api/datasources/uid/pubtube-prometheus", authorization)
    if (datasource.get("type"), datasource.get("url"), datasource.get("access"),
        datasource.get("isDefault"), datasource.get("readOnly")) != (
            "prometheus", "http://prometheus:9090", "proxy", True, True):
        raise ValueError("Provisioned datasource differs from the contract")
    ds_health = get(grafana + "/api/datasources/uid/pubtube-prometheus/health", authorization)
    if ds_health.get("status") != "OK":
        raise ValueError("Grafana datasource health is not OK")
    print("PASS Datasource pubtube-prometheus, read-only, health OK", flush=True)
    response = get(grafana + "/api/dashboards/uid/pubtube-gateway", authorization)
    dashboard = response["dashboard"]
    if (dashboard.get("uid") != source["uid"] or dashboard.get("title") != source["title"]
            or dashboard.get("editable") is not False or not response["meta"].get("provisioned")):
        raise ValueError("Dashboard is not provisioned from Git")
    loaded = {panel["id"]: panel for panel in dashboard["panels"]}
    operational = [panel for panel in source["panels"] if panel["type"] != "row"]
    for panel in operational:
        actual = loaded[panel["id"]]
        for field in ("title", "type", "description", "datasource", "fieldConfig", "targets"):
            if actual.get(field) != panel.get(field):
                raise ValueError(f"Provisioned panel {panel['id']} differs in {field}")
    if loaded[8].get("collapsed") is not True or loaded[8].get("panels") != source["panels"][-1]["panels"]:
        raise ValueError("Future row differs from the versioned preparation")
    print("PASS Dashboard pubtube-gateway, 7 operational panels and collapsed future row", flush=True)
    proxy = grafana + "/api/datasources/proxy/uid/pubtube-prometheus"
    for metric in ("pubtube_gateway_requests_total", "pubtube_gateway_request_duration_seconds_bucket"):
        query(prometheus, metric + '{job="pubtube-gateway"}')
    print("PASS Real Gateway counter and histogram series", flush=True)
    # Bound retries to allow two 15-second scrapes without fabricating data.
    for attempt in range(12):
        try:
            evidence = []
            for panel in operational:
                expression = panel["targets"][0]["expr"]
                direct = query(prometheus, expression)
                through_grafana = query(proxy, expression, authorization)
                if panel["id"] == 1 and not all(float(item["value"][1]) == 1 for item in through_grafana):
                    raise ValueError("Gateway status query is not UP")
                evidence.append(f"PASS Panel {panel['id']} {panel['title']}: "
                                f"Prometheus={len(direct)} series, Grafana={len(through_grafana)} series; "
                                f"sample={through_grafana[0]['value'][1]}")
            print("\n".join(evidence), flush=True)
            print("PASS All operational queries through provisioned datasource; future metrics excluded", flush=True)
            return
        except ValueError:
            if attempt == 11:
                raise
            get(gateway + "/api/health")
            time.sleep(5)


if __name__ == "__main__":
    try:
        verify()
    except (HTTPError, URLError, ValueError, KeyError, OSError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
