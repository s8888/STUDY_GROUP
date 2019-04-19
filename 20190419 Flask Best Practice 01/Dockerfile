ARG BASE_CONTAINER=blueswen/flask-best-practice:1.0
FROM $BASE_CONTAINER

USER root

# Install all OS dependencies for fully functional notebook server
RUN pip --no-cache-dir install --upgrade \
    flask_script \
    flask_migrate \
    psycopg2-binary \
    flask_restful \
    && rm -rf /var/lib/apt/lists/*

# Switch back to jovyan to avoid accidental container runs as root
USER $NB_UID
