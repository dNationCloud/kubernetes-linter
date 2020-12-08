import json
import subprocess
import os
import logging
import time

from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY
from prometheus_client.metrics_core import GaugeMetricFamily, CounterMetricFamily

_HTTP_PORT = int(os.getenv("HTTP_PORT", "9102"))


class LintIntCollector:
    def __init__(self):
        self._log = logging.getLogger("LintIntCollector")

    def collect(self):
        # clusterlint --kubeconfig config run -o json
        try:
            raw = subprocess.check_output(["clusterlint", "run", "-o", "json"])
            data = json.loads(raw)
            items = {}

            # TODO: for now only one label per item
            for item in data['Diagnostics']:
                metric_name = item["Check"]
                metric_label = {}
                if "pod" in item["Kind"]:
                    metric_label = ("where", item["Object"]["ownerReferences"][0]["name"])
                else:
                    metric_label = None
                if metric_name not in items:
                    items[metric_name] = {}
                if metric_label in items[metric_name]:
                    items[metric_name][metric_label] += 1
                else:
                    items[metric_name][metric_label] = 1
            for key in items:
                metric_name = key.replace("-", "_")
                #TODO:For future labels will be list of possible labels
                metric = GaugeMetricFamily(name='linter_result', documentation=metric_name, labels=["name", "where"])
                for label in items[key]:
                    if not label:
                        #TODO:when there is no labels we use only name of problem
                        metric.add_metric([metric_name], value=items[key][label])
                    else:
                        #TODO:List of labels in same order as in create
                        metric.add_metric([metric_name, label[1]], value=items[key][label])
                yield metric

        except subprocess.CalledProcessError as e:
            print("error during run Linterint")
            print(e.output)


if __name__ == "__main__":
    start_http_server(_HTTP_PORT)
    REGISTRY.register(LintIntCollector())
    while True:
        time.sleep(1)
