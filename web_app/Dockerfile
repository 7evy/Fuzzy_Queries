FROM python:3.8
WORKDIR /
COPY . .
COPY req.txt req.txt
COPY ./data/db.csv db.csv
COPY ./data/stats.csv stats.csv
RUN pip install -r req.txt
# CMD ["python", "fill_db.py", "&&", "python", "manage.py", "runserver"]
