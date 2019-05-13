@ECHO off
rem 使用rsync同步打包机上的客户端
rem by LD
rem 2015-03-06
rem 如果发现同步的客户端和实际不一致，请联系本人查证，谢谢

rem color 2f

echo %date%%time%

ECHO 挂载远程目录
rem 这里是将远程目录挂载为W分区，如果需要挂载其他目录，可自行修改，一般不需要动
net use W: \\192.168.228.24\Release_Package\develop
w:
ECHO 获取可同步的目录:

SET index=1

SETLOCAL ENABLEDELAYEDEXPANSION
FOR /d %%f IN (P1.255.255-*) DO (
   SET path!index!=%%f
   ECHO !index! - w:\%%f
   SET /A index=!index!+1
)

SETLOCAL DISABLEDELAYEDEXPANSION

ECHO.
SET /P selection="请选择同步的源目录:"

SET path%selection% >nul 2>&1

IF ERRORLEVEL 1 (
   ECHO invalid number selected   
   EXIT /B 1
)

CALL :RESOLVE %%path%selection%%%

ECHO 同步的源目录为: w:\%path_name%
ECHO 开始同步
rem 下面的  p/P1.255.255.255.255/ 对应的是  p:\P1.255.255.255.255\ 目录，一般情况下，只需要修改自己存放的路劲即可
rem D:\cwRsync\rsync -rv --delete --stats --size-only --progress /cygdrive/w/%path_name%/    /cygdrive/p/P1.255.255.255.255/
rem D:\cwRsync\rsync -av --delete --stats --block-size=512 --progress --modify-window=1 --protocol=29 /cygdrive/w/%path_name%/    /cygdrive/p/P1.255.255.255.255/
D:\cwRsync\rsync -acv --delete --stats --progress /cygdrive/w/%path_name%/    /cygdrive/p/P1.255.255.255.255/

rem 这里是切到d分区下，以便卸载w分区的时候不会报错
d:

ECHO 卸载远程目录
net use w: /delete /Y

echo %date%%time%

pause
@ECHO on
GOTO :EOF

:RESOLVE
SET path_name=%1
GOTO :EOF