@echo off
chcp 65001 >nul
echo ====================================
echo 開始批次產生所有情境的語音檔
echo (每句一個 mp3,共 18 主題 / 82 情境)
echo ====================================
echo.

set count=0

for %%T in (traits imagine notslave discipline parents singleparent art speech activity social earlyschool sleep toilet focus lying shy jealousy dependency) do (
    for /d %%S in (%%T\*) do (
        set /a count+=1
        echo [處理中] %%T\%%~nxS
        cd %%S
        python generate_audio.py
        cd ..\..
        echo.
    )
)

echo.
echo ====================================
echo 全部完成!
echo ====================================
pause
