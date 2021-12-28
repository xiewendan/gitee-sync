title start in k8s debug

cd ..

start minikube mount %cd%:/host

timeout /nobreak /t 10

kubectl apply -f res/deploy_debug.yaml

minikube tunnel

cd bin

pause