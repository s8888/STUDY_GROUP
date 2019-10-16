# 10.95.28.159:5001/util/api-framework:v1.0.0
# ==================================================================
FROM 10.95.28.159:5001/util/api-framework/api_base:v1.0
RUN PIP_INSTALL="python -m pip --no-cache-dir install --upgrade" && \
    $PIP_INSTALL --extra-index-url http://10.60.78.14:8800/ --trusted-host 10.60.78.14 \
        api-framework 
