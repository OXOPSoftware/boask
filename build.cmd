@echo off
echo Cleaning old build artifacts...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "boask.egg-info" rmdir /s /q "boask.egg-info"
echo.
echo Building new distribution packages...
python -m build
echo.
echo Uploading to PyPI...
twine upload dist/*
echo.
echo Done! Press any key to exit.
pause