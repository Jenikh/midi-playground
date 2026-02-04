@echo off
setlocal enableDelayedExpansion
(
  python main.py
  set "errorlevel=1"
  set "errorlevel="
  if !errorlevel! neq 0 (python main.py)
)