FROM python:3.8-slim
RUN pip3 install "feast[redis]"

COPY feature_repo/feature_store.yaml feature_store.yaml
RUN sed -i 's/localhost:6379/redis:6379/g' feature_store.yaml
ENV FEAST_USAGE=False

CMD ["feast", "serve", "-h", "0.0.0.0"]