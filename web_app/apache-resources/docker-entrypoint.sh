#!/bin/bash
cd /code
exec gunicorn web_app.wsgi -b localhost:8000
