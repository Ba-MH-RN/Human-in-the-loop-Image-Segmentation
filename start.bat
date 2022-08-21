@echo off
start "Server" /D .\backend\ startServer.bat
start "Frontend" /D .\frontend\ start.bat
