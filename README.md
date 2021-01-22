# dNation Kubernetes Linter

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Artifact HUB](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/dnationcloud)](https://artifacthub.io/packages/search?repo=dnationcloud)

![dNation Kubernetes Linter GUI](https://cdn.ifne.eu/public/icons/dnation_kubernetes_linter_screenshot.png "dNation Kubernetes Linter GUI")

dNation Kubernetes Linter is a software stack for analysis of live Kubernetes clusters.

It consists of:
* [Clusterlint](https://github.com/digitalocean/clusterlint)
* Prometheus exporter for Clusterlint
* Grafana dashboard

Prometheus exporter for Clusterlint translates the results of the linter into Prometheus metrics.
Code is located in docker/exporter directory.

Grafana dashboard reads the linter results from Prometheus and visualizes them.
Code is located in examples directory.

## Installation

```bash
# Add dNation helm repository
helm repo add dnationcloud https://dnationcloud.github.io/helm-hub/
helm repo update

# Install dNation Kubernetes Linter
helm install dnation-kubernetes-linter dnationcloud/kubernetes-linter
```

Helm chart will install the [Clusterlint](https://github.com/digitalocean/clusterlint) and the prometheus exporter.

### Installation from local git repo

In case you also have installed [Prometheus Operator](https://github.com/prometheus-operator/prometheus-operator)
you can move file examples/servicemonitor.yaml to chart/templates and Prometheus Service Discovery will work out of the box:
```bash
mv examples/servicemonitor.yaml chart/templates/
helm install <release-name> chart
```

## Contribution guidelines

If you want to contribute, please read following:
1. [Contribution Guidelines](CONTRIBUTING.md)
1. [Code of Conduct](CODE_OF_CONDUCT.md)

We use GitHub issues to manage requests and bugs.

## Commercial support
This project has been developed, maintained and used in production by professionals to simplify their day-to-day monitoring tasks and reduce incident reaction time.

Commercial support is available, including 24/7, please [contact us](mailto:cloud@dNation.cloud?subject=Request%20for%20commercial%20support%20of%20dNation%20Kubernetes%20Linter).
