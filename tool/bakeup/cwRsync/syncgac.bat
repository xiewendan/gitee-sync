@ECHO off
rem ʹ��rsyncͬ��������ϵĿͻ���
rem by LD
rem 2015-03-06
rem �������ͬ���Ŀͻ��˺�ʵ�ʲ�һ�£�����ϵ���˲�֤��лл

rem color 2f

echo %date%%time%

ECHO ����Զ��Ŀ¼
rem �����ǽ�Զ��Ŀ¼����ΪW�����������Ҫ��������Ŀ¼���������޸ģ�һ�㲻��Ҫ��
net use W: \\192.168.228.24\Release_Package\develop
w:
ECHO ��ȡ��ͬ����Ŀ¼:

SET index=1

SETLOCAL ENABLEDELAYEDEXPANSION
FOR /d %%f IN (P1.255.255-*) DO (
   SET path!index!=%%f
   ECHO !index! - w:\%%f
   SET /A index=!index!+1
)

SETLOCAL DISABLEDELAYEDEXPANSION

ECHO.
SET /P selection="��ѡ��ͬ����ԴĿ¼:"

SET path%selection% >nul 2>&1

IF ERRORLEVEL 1 (
   ECHO invalid number selected   
   EXIT /B 1
)

CALL :RESOLVE %%path%selection%%%

ECHO ͬ����ԴĿ¼Ϊ: w:\%path_name%
ECHO ��ʼͬ��
rem �����  p/P1.255.255.255.255/ ��Ӧ����  p:\P1.255.255.255.255\ Ŀ¼��һ������£�ֻ��Ҫ�޸��Լ���ŵ�·������
rem D:\cwRsync\rsync -rv --delete --stats --size-only --progress /cygdrive/w/%path_name%/    /cygdrive/p/P1.255.255.255.255/
rem D:\cwRsync\rsync -av --delete --stats --block-size=512 --progress --modify-window=1 --protocol=29 /cygdrive/w/%path_name%/    /cygdrive/p/P1.255.255.255.255/
D:\cwRsync\rsync -acv --delete --stats --progress /cygdrive/w/%path_name%/    /cygdrive/p/P1.255.255.255.255/

rem �������е�d�����£��Ա�ж��w������ʱ�򲻻ᱨ��
d:

ECHO ж��Զ��Ŀ¼
net use w: /delete /Y

echo %date%%time%

pause
@ECHO on
GOTO :EOF

:RESOLVE
SET path_name=%1
GOTO :EOF