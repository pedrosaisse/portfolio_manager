FROM python:3.11-slim

WORKDIR /portfolio_api
COPY . .
RUN pip install -r requirements.txt
CMD [ "uvicorn", "service.app:app", "--host", "0.0.0.0", "--port", "80"]
