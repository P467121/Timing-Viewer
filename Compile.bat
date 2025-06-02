@echo off
rmdir /s /q "%~dp0\dist"
rmdir /s /q "%~dp0\build"
cd %~dp0\
pyinstaller TimingViewer.spec /f
exit