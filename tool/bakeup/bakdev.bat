rem rsync d drive to G drive

echo %date%%time%

echo 本地备份

cwRsync\rsync -av --delete --stats /cygdrive/F/Documents/yitian/ /cygdrive/G/local/yitian/
cwRsync\rsync -av --delete --stats /cygdrive/F/Documents/doc/ /cygdrive/G/local/doc/
cwRsync\rsync -av --delete --stats /cygdrive/F/Documents/work/ /cygdrive/G/local/work/

cwRsync\rsync -av --delete --stats /cygdrive/C/Users/xxx/Desktop /cygdrive/G/local/users/Desktop


echo %date%%time%

pause