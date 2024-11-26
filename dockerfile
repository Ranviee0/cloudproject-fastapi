FROM python:3.12

WORKDIR /code

# Define build arguments with default values
ARG DB_USERNAME=admin
ARG DB_PASSWORD=group9login
ARG DB_HOST=localhost:3306
ARG DB_DATABASE=CCTV_service

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /code/app

# Modify database.py directly using the arguments
RUN sed -i "s/^username = .*/username = '${DB_USERNAME}'/; s/^password = .*/password = '${DB_PASSWORD}'/; s/^host = .*/host = '${DB_HOST}'/; s/^database = .*/database = '${DB_DATABASE}'/;" /code/app/database.py

CMD ["fastapi", "run", "app/main.py", "--port", "80"]