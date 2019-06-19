@ECHO OFF
set outputFolder=build\dist
pyinstaller --onefile ".\Source\Streamlabs Rcon Integration.py" --workpath ".\build" --clean --distpath ".\build\dist" --specpath ".\build"
if not exist "%outputFolder%\config.json" (
    xcopy "Source\config.sample.json" "%outputFolder%" /q /y /i
    ren "%outputFolder%\config.sample.json" "config.json"
)
xcopy "Source\eventDefinitions.json" "%outputFolder%" /q /y /i
xcopy "Profiles" "%outputFolder%\Profiles" /q /s /y /i
xcopy "README.md" "%outputFolder%" /q /y /i
xcopy "LICENSE" "%outputFolder%" /q /y /i
pause