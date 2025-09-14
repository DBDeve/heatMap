# heatMap
A program that consists of an HTML front-end, a Flesk backend, and a MySQL database.

Through the interface you can reset and reload clicks as well as download a .csv file with all the click data inside.
It is also possible to upload clicks made in a specific period of time.

## how to use the program
1. clone the repository (git clone https://github.com/DBDeve/heatMap.git) or download the zip file.
2. create the venv: python -m venv .venv
3. activate venv: source .venv/bin/activate o .venv\Scripts\activate o .venv\Scripts\Activate.ps1
4. install flesk: pip install flask
5. add flesk_cors: pip install flask_cors
6. activate flesk: python app.py