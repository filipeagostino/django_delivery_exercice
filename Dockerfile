FROM mysql:8

ENV MYSQL_ROOT_PASSWORD toor
ENV MYSQL_ROOT_USER root
ENV MYSQL_DATABASE delivery


COPY ./data.sql /docker-entrypoint-initdb.d.data.sql