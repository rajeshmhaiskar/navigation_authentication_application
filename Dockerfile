FROM Python 3.7.16
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python","apps.py"]
