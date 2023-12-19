from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import smtplib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
# Initialize the database
db = SQLAlchemy(app)
app.app_context().push()

#Create db model
class Friends(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	# Create a function to return a string when we add
	def __repr__(self):
		return '<Name %r>' % self.name

subscribers = []

@app.route('/')
def index():
	title = "James McArthur Portfolio"
	return render_template('index.html', title=title)

@app.route('/about')
def about():
	names = ['Simon', 'Helen', 'James', 'Stewart', 'Dexter']
	return render_template('about.html', names=names)

@app.route('/friends', methods=['POST', 'GET'])
def friends():
	title = "My friend List"
	if request.method == "POST":
		friend_name = request.form['name']
		new_friend = Friends(name=friend_name)

		# Push to db
		try:
			db.session.add(new_friend)
			db.session.commit()
			return redirect('/friends')
		except:
			return "There was an error adding your friend!"

	else:
		friends = Friends.query.order_by(Friends.date_created)
		return render_template('friends.html', title=title, friends=friends)

@app.route('/delete/<int:id>')
def delete(id):
	friend_to_delete = Friends.query.get_or_404(id)

	try:
		db.session.delete(friend_to_delete)
		db.session.commit()
		return redirect('/friends')
	except:
		return "There was a problem deleting your friend!"

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
	friend_to_update = Friends.query.get_or_404(id)

	if request.method == "POST":
		friend_to_update.name = request.form['name']

		try:
			db.session.commit()
			return redirect('/friends')
		except:
			return "There was an error updating your friend!"

	else:
		return render_template('update.html', friend_to_update=friend_to_update)



@app.route('/subscribe')
def subscribe():
	title = "Subscribe to my Newsletter"
	return render_template('subscribe.html', title=title)

@app.route('/form', methods=["POST"])
def form():
	first_name = request.form.get("first_name")
	second_name = request.form.get("second_name")
	email = request.form.get("email")

	# code to send email to new subscriber - it stops the all form fields required from working
	# Could possibly shanged to a function
	'''
	message = "you have been subscribed to my email newsletter...."
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login("james.d.mcarthur@googlemail.com", "pxgdcomsujwxtjnf")
	server.sendmail("james.d.mcarthur@googlemail.com", email, message)
	'''
	if not first_name or not second_name or not email:
		error_statement = "All form fields Required..."
		return render_template("subscribe.html", 
			error_statement=error_statement, 
			first_name=first_name,
			second_name=second_name,
			email=email)

	subscribers.append(f"{first_name} {second_name} | {email}")
	title = "Thank you!"
	return render_template('form.html', title=title, subscribers=subscribers)

@app.route('/css_cheatsheet')
def css_cheatsheet():
	names = ['Simon', 'Helen', 'James', 'Stewart', 'Dexter']
	return render_template('css_cheatsheet.html', names=names)