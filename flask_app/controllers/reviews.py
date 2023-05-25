from flask_app import app 
from flask import render_template, redirect, request, session
from flask_app.models.review import Review
from flask_app.models.user import User

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/jobs')
def jobs():
    return render_template('job.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/user/login')
    user = User.get_by_id({"id":session['user_id']})

    if not user:
        return redirect('/user/logout')
    return render_template('dashboard.html',user=user, reviews=Review.get_all())

@app.route('/reviews/new')
def create_review():
    if 'user_id' not in session:
        return redirect('/user/login')
    return render_template ('review_new.html')

@app.route('/reviews/new/process', methods=['POST'])
def process_review():
    if 'user_id' not in session: 
        return redirect ('/user/login')
    if not Review.validate_review(request.form):
        return redirect('/reviews/new')
    
    data = {
        'user_id': session['user_id'],
        'name': request.form['name'],
        'review': request.form['review'],
        'date_made': request.form['date_made'],
        'image_data': request.form['image_data'],
    }
    Review.save(data)
    return redirect('/dashboard')

@app.route('/reviews/<int:id>')
def view_review(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    return render_template('review_view.html',review=Review.get_by_id({'id': id}))

@app.route('/reviews/edit/<int:id>')
def edit_review(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    return render_template('review_edit.html',review=Review.get_by_id({'id': id}))

@app.route('/reviews/edit/process/<int:id>',methods=['POST'])
def process_edit_review(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    if not Review.validate_review(request.form):
        return redirect(f'/reviews/edit/{id}')
    
    data = {
        'id': id,
        'name': request.form['name'],
        'review': request.form['review'],
        'date_made': request.form['date_made'],
    }
    Review.update(data)
    return redirect('/dashboard')

@app.route('/reviews/destroy/<int:id>')
def destroy_review(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    
    Review.destroy({'id':id})
    return redirect('/dashboard')




# @app.route('/reviews/new', methods=['GET', 'POST'])
# def upload():
#     if request.method == 'POST':
#         image = request.files['image']
#         # Store image in the database
#         cursor = mysql.connection.cursor()
#         cursor.execute("INSERT INTO images (image_data) VALUES (%s)", (image.read(),))
#         mysql.connection.commit()
#         cursor.close()
#         return 'Image uploaded and stored in the database!'
#     return render_template('review_new.html')

# # Route for displaying reviews
# @app.route('/reviews/<int:id>')
# def reviews():
#     cursor = mysql.connection.cursor()
#     cursor.execute("SELECT image_data FROM reviews")
#     reviews = cursor.fetchall()
#     cursor.close()
#     return render_template('review_view.html', reviews=reviews)