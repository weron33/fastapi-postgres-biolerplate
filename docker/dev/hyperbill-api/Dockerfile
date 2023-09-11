FROM hyperbill-api:0.0 AS base

COPY src /hyperbill-api/src

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]