FROM python:3.8-slim as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

COPY ./dist/*.whl ./
RUN pip install *.whl && rm -rf *.whl

COPY ./multilayer_caching_memcached/application.yml ./

CMD ["gunicorn", "multilayer_caching_memcached.wsgi:app", "-w", "1", "--bind", "0.0.0.0:8080"]