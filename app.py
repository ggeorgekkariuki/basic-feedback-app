from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

#Initialise the Flask object called 'app' - gateway to the web page and server
app = Flask(__name__)

#Configurations 
ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:PASSWORD@localhost/lexus'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://txlzzbzxtdttgf:80b88875f3a12afb48986e80e7a752ca87a4492e47ddc49bf0e1d95beeb3c8ac@ec2-54-210-128-153.compute-1.amazonaws.com:5432/dbt9dk9m51dnk0'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Initialise the SQLAlchemy object 'db'
db = SQLAlchemy(app)

#Creating a model for our table
class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(100), unique=True)
    dealer = db.Column(db.String(100))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    #Class constructor
    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments
    ## SEE NOTES AT THIS POINT ##

#Route to index page
@app.route('/')
def index():
    return render_template('index.html')

#Route to handle submission and redirect to success page
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']

        # Add validations to the form and display a message if otherwise
        if customer == "" or dealer == "":
            return render_template('index.html', message="Please enter required fields!")
        
        # Only allow new customers to submit feedback
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            ## SEE NOTES AT THIS POINT
            # After the data has been saved on the PSQL database, send an email now
            send_mail(customer, dealer, rating, comments)
            return render_template('success.html')
        else:
            return render_template('index.html', message="You cannot submit feedback twice!")
    
if __name__ == "__main__":
    app.run()