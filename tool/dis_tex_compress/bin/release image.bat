cd ..
docker build -t stephenxjc/dis_tex_register -f res/register/Dockerfile .
docker build -t stephenxjc/dis_tex_executor -f res/executor/Dockerfile .

docker push stephenxjc/dis_tex_register
docker push stephenxjc/dis_tex_executor

cd bin

pause