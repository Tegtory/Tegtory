FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python -m grpc_tools.protoc --proto_path=./protos/ --python_out=. --grpc_python_out=. protos/tegtory/*.proto

CMD ["python", "-m", "tegtory"]