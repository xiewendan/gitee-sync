cd ..

pyinstaller main_frame/main.py -F --clean --distpath binexe --workpath temp

rm -rf temp

del /q main.spec

pause