#!/bin/bash
gunicorn -w 1 -k sync --timeout 120 --log-level debug -b 0.0.0.0:6001 app:app # 
