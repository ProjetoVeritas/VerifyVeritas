# Veritas Verify API

This API is responsible for different routes in the Projeto Veritas:

* Receive new fakes and register in the DB

* Answer verify queries, returning the answer for fakes

* Give available fakes to answer

* Update unanswered fake entries in DB

## Environment Variables

* user: Elasticsearch user

* password: Elasticsearch password

* host: Elasticsearch host

* TIKA_SERVER: Tika text extractor host

* TRANSCRIBE_SERVER: Transcriber service host

## How to run

```shell script
cd flaskapp
flask run
```
