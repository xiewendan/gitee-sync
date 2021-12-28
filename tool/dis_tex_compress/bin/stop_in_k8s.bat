echo off
title stop in k8s

cd ..

kubectl delete -f res/deploy.yaml

cd bin

pause