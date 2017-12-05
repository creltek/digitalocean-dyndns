FROM alpine

RUN apk update \
    && apk add --no-cache python3 \
    && pip3 install requests

COPY dyndns.py /usr/local/bin/dyndns.py

ENTRYPOINT [ "python3", "/usr/local/bin/dyndns.py" ]
