FROM python:3.9.15-bullseye

COPY ./ /app
WORKDIR /app
RUN apt update && apt install -y libpcap-dev make && apt-get clean  \
    && wget "https://golang.org/dl/go1.19.2.linux-amd64.tar.gz"  \
    && tar -C /usr/local -xzf go1.19.2.linux-amd64.tar.gz && rm go1.19.2.linux-amd64.tar.gz
ENV PATH /usr/local/go/bin:$PATH
RUN go install -v github.com/boy-hack/ksubdomain/cmd/ksubdomain@latest && python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python", "main.py"]
