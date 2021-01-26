FROM golang

LABEL Version="0.2.1"
LABEL Vendor="dNation"
LABEL Description="Prometheus exporter for ClusterLint"

WORKDIR /opt/clusterlint

RUN apt-get update && apt-get install -y \
  python3 \
  python3-dev \
  python3-pip \
  && rm -rf /var/lib/apt/lists/*

#install clusterlint
RUN go get github.com/digitalocean/clusterlint/cmd/clusterlint

RUN pip3 install prometheus_client

#Add exporter
ADD exporter/prometheus_exporter_lint.py /opt/clusterlint/

#run exporter
CMD python3 /opt/clusterlint/prometheus_exporter_lint.py
