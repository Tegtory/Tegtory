FROM python:3.12

WORKDIR /app

RUN pip install uv

COPY . .

RUN uv sync
RUN uv run python -m grpc_tools.protoc --proto_path=./protos/ --python_out=. --grpc_python_out=. protos/tegtory/*.proto

CMD ["uv", "run", "python", "-m", "tegtory"]