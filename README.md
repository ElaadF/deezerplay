# deezerplay

## prerequisites
+ Python 3
+ virtualenv
+ Django
+ requests (Python 3)
+ keras
+ tensorflow
+ pandas
+ sklearn

## Install

1. Install virtualenv   
```bash
pip install virtualenv
```

After your installation, you will be able to use a virtual env for your python program. You will need 3 commands :   

+ create a virtual environnement
```bash
python3 -m venv <directory's path>
```
+ activate envrionnement
```bash
source <env's path>/bin/activate
```
+ deactivate env
```
deactivate
```

Virtualenv allows you to install python package independently from your system. You will need to activate every time the envrionnement before 

2. Install requierements    
```bash
 pip3 install -r requirements.txt
```
## Run
1. Activate envrionnement
```bash
source <env's path>/bin/activate
```
2. In the root of the project run :
```bash
python3 manage.py runserver
```
3. Acces locally : http://localhost:8000
