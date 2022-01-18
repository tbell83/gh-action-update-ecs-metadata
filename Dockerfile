FROM python:alpine3.15

RUN python -m pip install boto3

COPY metadata.py /metadata.py
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
