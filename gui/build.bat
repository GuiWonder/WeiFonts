@echo off

echo Begin

msbuild WeiFonts.sln /p:Configuration=Release /p:Platform=x64

echo End
pause
