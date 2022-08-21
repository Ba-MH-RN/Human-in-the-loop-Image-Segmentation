@echo off
CALL .\venv\Scripts\activate.bat

::pytest tests/ImageSegmentation/ -v -W ignore::DeprecationWarning
pytest tests/REST_Server/data/util -v -W ignore::DeprecationWarning