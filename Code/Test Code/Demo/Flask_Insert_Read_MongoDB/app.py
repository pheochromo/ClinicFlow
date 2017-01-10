import pymongo #import pymongo to connect with MongoDB, need to download pymongo package first
from pymongo import MongoClient #import MongoDB
from flask import Flask, render_template, request, url_for # import Flask

# Initialize the Flask application
app = Flask(__name__)
# Initialize the MongoDB
client = MongoClient() #Call the local MongoDB server, later we can connect to Amazon MongoDB server
# To use local MongoDB server, need to download and install it first
db = client.capstone # create schema
patient_info = db.patients #create table

# Define a route for the default URL, which loads the main 
@app.route('/')
def main():
    return render_template('patient_data.html') # open patient_data.html
# Define a route for URL /hello, which add inputs to MongoDB
# There exists a mysterious error if I change 'hello' to other name, will cause internal server error
@app.route('/hello/', methods=['POST'])
def hello():
    pname=request.form['Pname'] #get the input from Pname
    rdate=request.form['Rdate'] #get the input from Rdate
    post ={"name":pname, 
           "date":rdate}# MongoDB data
    patient_info.insert_one(post) #insert into MongoDB
    return render_template('patient_data.html') #Stay at the page
# Defien the URL ,read database and open displaypatient.html
@app.route('/displaypatient/', methods=['POST'])
def displaypatient():
    names =[]
    dates =[]
    #read the MongoDB database
    for single in patient_info.find():
        names.append(single["name"])
        dates.append(single["date"])
    pats = zip(names,dates)
   #send data to displaypatient.html, construct a table
    return render_template('displaypatient.html', data = pats)
# Run the app :)
if __name__ == '__main__':
  app.run()