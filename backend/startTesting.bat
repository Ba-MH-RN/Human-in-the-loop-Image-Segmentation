@echo off
CALL .\venv\Scripts\activate.bat

pytest tests/ -v -W ignore::DeprecationWarning