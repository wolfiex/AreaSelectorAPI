'''
A quick and dirty database server written in python. 
Designed for testing the postcode selector. 


Dan Ellis 
'''
# app.py
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
app = Flask('SuperSecretSpyFinder')
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

import sqlite3
conn = sqlite3.connect('postcodes.db',check_same_thread=False)
cursor = conn.cursor()




######## HOME ############
@app.route('/')
def main():
    return 'This is the geography selector.'

######## Data fetch ############
@app.route('/postcode/<match>/<limit>', methods=['GET'])
def pfind(match,limit):
    r = conn.execute(r'SELECT POST,IDLSOA from POSTAREA WHERE PSELECT LIKE "{}%" LIMIT {};'.format(match.replace(' ','').upper(),int(limit))).fetchall()
    return jsonify(r)  # serialize and use JSON headers

@app.route('/name/<match>/<limit>', methods=['GET'])
def nfind(match,limit):
    r = conn.execute(r'SELECT * from NAMELIST WHERE NAME LIKE "{}%" LIMIT {};'.format(match.replace(' ','').upper(),int(limit))).fetchall()
    return jsonify(r)  # serialize and use JSON headers




@app.route('/lad/<value>', methods=['GET'])
def ladfind(value):
    r = conn.execute(r'SELECT CODE from LAD WHERE ID = %d;'%int(value)).fetchone()
    return jsonify(r)  # serialize and use JSON headers





# run app
app.run(port=5002,debug=True)