FROM apache/airflow:3.3.0


WORKDIR /opt/airflow

RUN pip install --no-cache-dir \
    "apache-airflow==${AIRFLOW_VERSION}" \
    "pandas==2.3.3" \
    "python-dotenv>=1,<2" \
    "psycopg2-binary>=2.9,<3"

COPY --chown=airflow:root src/ /opt/airflow/src/

ENV PYTHONPATH=/opt/airflow/src