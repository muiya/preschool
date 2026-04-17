@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

set count=0
set folders=traits imagine notslave discipline parents singleparent art speech activity social earlyschool sleep toilet focus lying shy jealousy dependency

for %%T in (%folders%) do (
    if exist "%%T" (
        for /d %%S in ("%%T\*") do (
            set /a count+=1
            echo [Processing] %%T\%%~nxS
            pushd "%%S"
            if exist "generate_audio.py" (
                python generate_audio.py
            ) else (
                echo [Error] No python file in %%S
            )
            popd
            echo.
        )
    )
)

echo ====================================
echo Finished! Total: !count!
echo ====================================
pause