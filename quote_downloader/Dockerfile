FROM python:3.8-slim

RUN pip install --upgrade pip && pip install yfinance psycopg2-binary


COPY quotes_downloader.py quotes_downloader.py
RUN chmod +x quotes_downloader.py

CMD python ./quotes_downloader.py
