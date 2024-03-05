FROM python:3.9
WORKDIR app
COPY . /app
RUN pip install -r navigation_authentication_application/requirments/requirments.txt
EXPOSE 8001
CMD ["python","manage.py","runserver","0.0.0.0:8001"]
