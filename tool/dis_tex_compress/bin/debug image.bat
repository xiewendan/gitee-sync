title destroy image
cd ..
docker build -t stephenxjc/dis_tex_register_debug -f res/register/Dockerfile_debug .
docker build -t stephenxjc/dis_tex_executor_debug -f res/executor/Dockerfile_debug .

docker push stephenxjc/dis_tex_register_debug
docker push stephenxjc/dis_tex_executor_debug

cd bin

pause