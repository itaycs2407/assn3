FROM python:alpine3.10

# 
WORKDIR /app

# 
COPY main.py .

# 
RUN pip install  flask
RUN pip install requests



# 
COPY . /app 

EXPOSE 8000

# 
CMD ["python", "main.py"]

