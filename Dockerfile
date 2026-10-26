FROM apache/airflow:3.3.2

WORKDIR /opt/airflow

RUN pip install --no-cache-dir \
    "apache-airflow==${AIRFLOW_VERSION}" \
    "python-dotenv>=1,<2" \
    "psycopg2-binary>=2.9,<3"\
    "sqlalchemy>=2.0.52"

COPY --chown=airflow:root src/ /opt/airflow/src/

ENV PYTHONPATH=/opt/airflow/src