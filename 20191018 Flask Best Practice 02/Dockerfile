ARG BASE_CONTAINER=blueswen/flask-best-practice:1.0
FROM $BASE_CONTAINER

USER root

# Install all OS dependencies for fully functional notebook server
RUN pip --no-cache-dir install --upgrade \
    flask-restplus==0.13.0 \
    pyyaml==5.1.2 \
    cookiecutter==1.6.0


# Switch back to jovyan to avoid accidental container runs as root
USER $NB_UID
