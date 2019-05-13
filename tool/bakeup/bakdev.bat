rem rsync d drive to G drive

echo %date%%time%

echo 本地备份

cwRsync\rsync -av --delete --stats /cygdrive/E/Documents/yitian/ /cygdrive/G/local/yitian/
cwRsync\rsync -av --delete --stats /cygdrive/E/Documents/doc/ /cygdrive/G/local/doc/
cwRsync\rsync -av --delete --stats /cygdrive/E/Documents/work/ /cygdrive/G/local/work/

cwRsync\rsync -av --delete --stats /cygdrive/C/Users/xx.GAME/.vim /cygdrive/G/local/users/.vim
cwRsync\rsync -av --delete --stats /cygdrive/C/Users/xx.GAME/Desktop /cygdrive/G/local/users/Desktop
cwRsync\rsync -av --delete --stats /cygdrive/C/Users/xx.GAME/.viminfo /cygdrive/G/local/users/.viminfo
cwRsync\rsync -av --delete --stats /cygdrive/C/Users/xx.GAME/_vimrc /cygdrive/G/local/users/_vimrc


echo %date%%time%

pause