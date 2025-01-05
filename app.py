from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)

app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        if len(title) != 0:
            # If the 'todos' list does not exist in session, initialize it
            if 'todos' not in session:
                session['todos'] = []
            # Add a new todo to the session
            session['todos'].append({'title': title, 'desc': desc})
            session.modified = True  # Mark the session as modified so it will be saved
        return redirect('/')
    # Get the todos from session
    allTodo = session.get('todos', [])
    return render_template('index.html', allTodo=allTodo)


@app.route('/update/<int:index>', methods=['GET', 'POST'])
def update(index):
    if 'todos' not in session or len(session['todos']) <= index:
        return redirect('/')

    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        if len(title) != 0:
            # Update the todo at the specified index
            session['todos'][index]['title'] = title
            session['todos'][index]['desc'] = desc
            session.modified = True  # Mark the session as modified
        return redirect('/')

    todo = session['todos'][index]
    return render_template('update.html', todo=todo, index=index)


@app.route('/delete/<int:index>')
def delete(index):
    if 'todos' not in session or len(session['todos']) <= index:
        return redirect('/')
    
    # Remove the todo at the specified index
    del session['todos'][index]
    session.modified = True  # Mark the session as modified
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=False)
