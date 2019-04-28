rem rsync d drive to G drive

echo %date%%time%

echo 本地备份

f:\portable\cwRsync\rsync -av --delete --stats /cygdrive/E/Documents/yitian/ /cygdrive/G/local/yitian/
f:\portable\cwRsync\rsync -av --delete --stats /cygdrive/E/Documents/doc/ /cygdrive/G/local/doc/

f:\portable\cwRsync\rsync -av --delete --stats /cygdrive/C/Users/xx.GAME/.vim /cygdrive/G/local/users/.vim
f:\portable\cwRsync\rsync -av --delete --stats /cygdrive/C/Users/xx.GAME/Desktop /cygdrive/G/local/users/Desktop
f:\portable\cwRsync\rsync -av --delete --stats /cygdrive/C/Users/xx.GAME/.viminfo /cygdrive/G/local/users/.viminfo
f:\portable\cwRsync\rsync -av --delete --stats /cygdrive/C/Users/xx.GAME/_vimrc /cygdrive/G/local/users/_vimrc


echo 硬盘备份
D:\portable\cwRsync\rsync -av --delete --stats /cygdrive/O/book/ /cygdrive/P/G/book/

D:\portable\cwRsync\rsync -av --delete --stats /cygdrive/O/mystage/ /cygdrive/G/P/mystage/

D:\portable\cwRsync\rsync -av --delete --stats /cygdrive/O/document/ /cygdrive/G/P/document/

D:\portable\cwRsync\rsync -av --delete --stats /cygdrive/O/photo/ /cygdrive/G/P/photo/

D:\portable\cwRsync\rsync -av --delete --stats /cygdrive/O/project/ /cygdrive/G/P/project/

D:\portable\cwRsync\rsync -av --delete --stats /cygdrive/O/report/ /cygdrive/G/P/report/

D:\portable\cwRsync\rsync -av --delete --stats /cygdrive/O/works/ /cygdrive/G/P/works/

echo %date%%time%

pause