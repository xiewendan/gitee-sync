rem rsync d drive to G drive

echo %date%%time%

echo 本地备份

cwRsync\rsync -av --delete --stats /cygdrive/F/Documents/yitian/ /cygdrive/G/local/yitian/
cwRsync\rsync -av --delete --stats /cygdrive/F/Documents/config/ /cygdrive/G/local/config/

cwRsync\rsync -av --delete --stats /cygdrive/C/Users/xxx/Desktop /cygdrive/G/local/users/Desktop


echo %date%%time%