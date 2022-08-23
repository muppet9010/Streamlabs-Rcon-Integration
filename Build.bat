@ECHO OFF
set buildFolder=build
set outputFolder=%buildFolder%\dist
rd /s /q %buildFolder%
pyinstaller --onefile ".\Source\Streamlabs Rcon Integration.py" --workpath ".\build" --clean --distpath ".\build\dist" --specpath ".\build"
xcopy "Source\config.sample.json" "%outputFolder%" /q /y /i
xcopy "Source\eventDefinitions.json" "%outputFolder%" /q /y /i
xcopy "Profiles" "%outputFolder%\Profiles" /q /s /y /i
xcopy "README.md" "%outputFolder%" /q /y /i
xcopy "LICENSE" "%outputFolder%" /q /y /i
pause