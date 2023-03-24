@echo off
@REM ***************************************************************************
@REM * Script to handle python environment and startup given script
@REM ***************************************************************************
setlocal EnableDelayedExpansion
@REM ***************************************************************************
@REM * Set base variables, you may tweak here
@REM ***************************************************************************
@REM Set name of python environment
set "ENV_NAME=venv"
@REM Set name of python environment list exported by pip freeze > %REQ_NAME%
set "REQ_NAME=requirements.txt"
@REM Get name of script to start
set "SCRIPT=%~nx1"
@REM Set default name of script to run
set "DEF_SCRIPT=program.py"
@REM ***************************************************************************
@REM * Set internal variables, don't touch unless you know what you're doing!
@REM ***************************************************************************
@REM Get startup path of script
set "PATH_BASE=%~dp0"
@REM Set FQN of environment
set "PATH_ENVIRONMENT=%PATH_BASE%\%ENV_NAME%"
@REM ***************************************************************************
@REM * Check environment for existence
@REM ***************************************************************************
if not exist "%PATH_ENVIRONMENT%" (
    @REM Create environment
    echo.Create missing environment [%ENV_NAME%]
    python -m venv %ENV_NAME%
    @REM Activate environment
    if ""=="%VIRTUAL_ENV%" (
        echo.Initial activation of environment [%ENV_NAME%]
        call ./%ENV_NAME%/Scripts/activate.bat
    )
    @REM Install required modules
    if exist "%REQ_NAME%" (
        echo.Install required modules in [%REQ_NAME%] to [%ENV_NAME%]
        type %REQ_NAME%
        pip install -r %REQ_NAME%
    ) else (
        echo.List of required modules [%REQ_NAME%] not found
    )
)
@REM ***************************************************************************
@REM * Activate environment if not already done
@REM ***************************************************************************
if ""=="%VIRTUAL_ENV%" (
    echo.Activate environment [%ENV_NAME%]
    call ./%ENV_NAME%/Scripts/activate.bat
)
@REM ***************************************************************************
@REM * Determine script to run, if no name is passed, set default value
@REM ***************************************************************************
if ""=="%SCRIPT%" (
    set "SCRIPT=%DEF_SCRIPT%"
)
@REM ***************************************************************************
@REM * Execute script
@REM ***************************************************************************
if exist "%SCRIPT%" (
    echo.Execute script [%SCRIPT%]
    python %SCRIPT%
) else (
    echo.Script [%SCRIPT%] not found :-()
)
endlocal
