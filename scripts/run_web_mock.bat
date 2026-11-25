@echo off
cd /d %~dp0..
pytest -m mock --headed --slowmo 400 %*
