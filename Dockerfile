FROM ubuntu AS src

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git &&\
    cd / && \
    git clone https://github.com/jura4x01/tictactoe-web


FROM python:3.6-alpine AS production

WORKDIR /usr/src/app

COPY --from=src /tictactoe-web/* /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD [ "python", "./tictactoe.py" ]
