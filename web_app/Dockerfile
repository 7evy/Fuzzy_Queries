FROM python:3.6
WORKDIR /
COPY . .
COPY req.txt req.txt
COPY db.csv db.csv
RUN pip install -r req.txt
CMD ["python3", "src/test.py"]
