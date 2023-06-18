FROM tensorflow/tensorflow:2.3.4-gpu

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
