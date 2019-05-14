rem rsync d drive to G drive

echo %date%%time%

echo 本地备份

F:

F:\Users\xxx\Documents\yitian

cwRsync\rsync -av --delete --stats /cygdrive/F/Users/xxx/Documents/yitian/ /cygdrive/G/local/yitian/
cwRsync\rsync -av --delete --stats /cygdrive/F/Users/xxx/Documents/config/ /cygdrive/G/local/config/

cwRsync\rsync -av --delete --stats /cygdrive/D/"Program Files (x86)"/Netease/POPO/users/ /cygdrive/G/local/POPO/

cwRsync\rsync -av --delete --stats /cygdrive/C/Users/xxx/Desktop/ /cygdrive/G/local/Desktop/

cwRsync\rsync -av --delete --stats /cygdrive/C/Users/xxx/.PyCharmCE2019.1/config/keymaps/ /cygdrive/G/local/pycharmconfig/keymaps/
cwRsync\rsync -av --delete --stats /cygdrive/C/Users/xxx/.PyCharmCE2019.1/config/templates/ /cygdrive/G/local/pycharmconfig/templates/


echo %date%%time%