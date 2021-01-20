# Copyright 2020 The dNation Kubernetes Linter Authors. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import subprocess
import os
import logging
import time

from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY
from prometheus_client.metrics_core import GaugeMetricFamily

_HTTP_PORT = int(os.getenv("HTTP_PORT", "9102"))


class ClusterLintCollector:
    def __init__(self):
        self._log = logging.getLogger("ClusterLintCollector")

    def metric_from_diagnostic(self, diag):
        base_name = diag["Check"].replace("-", "_")
        metric_name = f"clusterlint_{base_name}_total"
        labels = {}

        tmp = diag["Check"].replace("-", " ")
        labels["check_name"] = tmp[0].upper() + tmp[1:]
        labels["kind"] = diag["Kind"]
        labels["object_name"] = diag["Object"]["name"]
        if "namespace" in diag["Object"]:
            labels["namespace"] = diag["Object"]["namespace"]
        labels["message"] = diag["Message"]
        if diag["Severity"] == "error":
            labels["severity"] = "2"
        if diag["Severity"] == "warning":
            labels["severity"] = "1"

        return metric_name, labels

    def collect(self):
        try:
            raw = subprocess.check_output(["clusterlint", "run", "-o", "json"])
            data = json.loads(raw)
            items = {}

            for diag in data['Diagnostics']:
                metric_name, labels_dict = self.metric_from_diagnostic(diag)
                if labels_dict:
                    label_names, label_values = zip(*sorted(labels_dict.items()))
                else:
                    label_names, label_values = (), ()
                if metric_name not in items:
                    items[metric_name] = {}
                if label_names not in items[metric_name]:
                    items[metric_name][label_names] = {}
                if label_values not in items[metric_name][label_names]:
                    items[metric_name][label_names][label_values] = 1
                else:
                    items[metric_name][label_names][label_values] += 1

            for metric_name in items:
                for label_names in items[metric_name]:
                    metric_family = GaugeMetricFamily(name=metric_name, documentation=metric_name, labels=label_names)
                    for label_values, value in items[metric_name][label_names].items():
                        metric_family.add_metric(label_values, value)
                    yield metric_family

        except subprocess.CalledProcessError as e:
            print("error during running ClusterLintCollector")
            print(e.output)


if __name__ == "__main__":
    start_http_server(_HTTP_PORT)
    REGISTRY.register(ClusterLintCollector())
    while True:
        time.sleep(1)
