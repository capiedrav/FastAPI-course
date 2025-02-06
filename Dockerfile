FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# install dependencies
WORKDIR /fastAPI-course
COPY ./requirements.txt .
RUN pip install --no-cache -r requirements.txt

# create non-root user   
RUN adduser --disabled-password --no-create-home app-user

# copy source code
COPY . .

# change ownership of the files
RUN chown -R app-user .

# switch to django-user
USER app-user

# run uvicorn server
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]
