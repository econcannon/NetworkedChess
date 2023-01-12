

ECHO OFF
set PORT=12004
set RULE_NAME="Open Port %PORT%"

netsh advfirewall firewall show rule name=%RULE_NAME% >nul
if not ERRORLEVEL 1 (
    rem Rule %RULE_NAME% doesn't Exist.
    echo Hey, there are no rules by that name
) else (
    echo Rule %RULE_NAME% does exist. Deleting...
    netsh advfirewall firewall delete rule name=%RULE_NAME%
)