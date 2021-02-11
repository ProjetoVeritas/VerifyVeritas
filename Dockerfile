FROM python:3.7-alpine
WORKDIR /flaskapp
ADD ./flaskapp/ /flaskapp
ADD ./requirements.txt /flaskapp
RUN pip install -r requirements.txt
CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "wsgi", "--timeout", "600"]