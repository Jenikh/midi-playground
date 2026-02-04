@echo off
setlocal enableDelayedExpansion
(
  python -m pip install -r requirements.txt
  set "errorlevel=1"
  set "errorlevel="
  if !errorlevel! neq 0 (python -m pip install -r requirements.txt)
)