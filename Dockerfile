FROM python:3.11-slim
WORKDIR /app
COPY requirements.pip .
RUN pip install --no-cache-dir -r requirements.pip
COPY . .
RUN python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["gunicorn", "planning_app.wsgi:application", "--bind", "0.0.0.0:8000"]