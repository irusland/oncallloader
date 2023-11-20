FROM mwalbeck/python-poetry:1.3.2-3.11

WORKDIR /prober

COPY README.md /prober/README.md
COPY poetry.lock /prober/poetry.lock
COPY pyproject.toml /prober/pyproject.toml
COPY scripts/run_exporter.py /prober/scripts/run_exporter.py

RUN poetry install

COPY exporter /prober/exporter
COPY oncall_client /prober/oncall_client
COPY scripts /prober/scripts

EXPOSE 7777

ENV PYTHONPATH=.

RUN chmod +x scripts/run_exporter.py

CMD ["poetry", "run", "prober"]
