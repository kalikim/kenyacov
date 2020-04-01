FROM python:3.7

EXPOSE 5000

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
RUN mkdir /app/uploads
#RUN chmod 777 /app/uploads

COPY . /app

CMD python app.py