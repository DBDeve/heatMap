# heatMap
A program that consists of an HTML front-end, a Flesk backend, and a MySQL database.

Through the interface you can reset and reload clicks as well as download a .csv file with all the click data inside.
It is also possible to upload clicks made in a specific period of time.

## how to use the program
1. create the venv: python -m venv .venv
2. activate venv: source .venv/bin/activate o .venv\Scripts\activate o .venv\Scripts\Activate.ps1
3. install flesk: pip install flask
4. add flesk_cors: pip install flask_cors
5. activate flesk: python app.py