FROM python:3.8
WORKDIR /
COPY . .
COPY req.txt req.txt
COPY ./data/db.csv db.csv
RUN pip install -r req.txt
# CMD ["python", "fill_db.py", "&&", "python", "manage.py", "runserver"]
