from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3 as sql
import sqlite3

app = Flask(__name__)


@app.route("/index")
def index():
    conn = sql.connect("db_web.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("select * from users")
    data = cur.fetchall()
    return render_template("index.html", datas=data)

@app.route('/')
def home():
    return render_template('home.html')

def get_db_connection():
    conn = sqlite3.connect('countries.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/countries', methods=['GET', 'POST'])
def countries():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        search_query = request.form['search_query']

        # Corrected SQL query with parameter substitution
        cur.execute('''SELECT * FROM country_list
                        WHERE eventid LIKE ?
                        OR iyear LIKE ?
                        OR imonth LIKE ?
                        OR iday LIKE ?
                        OR country_name LIKE ?
                        OR region LIKE ?
                        OR region_txt LIKE ?
                        OR provstate LIKE ?
                        OR city LIKE ?
                        OR targettype_txt LIKE ?
                        OR targetsubttype_txt LIKE ?
                        OR corp1 LIKE ?''',
                        ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%',
                         '%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%',
                         '%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%',
                         '%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))

        countries = cur.fetchall()

        # Check if results were found
        if not countries:
            not_found_message = "result not found."
        else:
            not_found_message = None

    else:
        cur.execute('SELECT * FROM country_list')
        countries = cur.fetchall()
        not_found_message = None

    conn.close()
    return render_template('countries.html', countries=countries, not_found_message=not_found_message)


@app.route('/history')
def history():
    return render_template('history.html')


@app.route('/attack-motive')
def attack_motive():
    return render_template('attack_motive.html')

@app.route('/awareness')
def awareness():
    return render_template('awareness.html')

@app.route('/get')
def get():
    return render_template('get.html')



@app.route("/add_user",methods=['POST','GET'])
def add_user():
    if request.method=='POST':
        uname = request.form['uname']
        email_id=request.form['email_id']
        password=request.form['password']
        Age=request.form['Age']
        Country=request.form['Country']
        contact=request.form['contact']
        conn=sql.connect("db_web.db")
        cur=conn.cursor()
        cur.execute("INSERT into users (UNAME,EMAIL_ID,PASSWORD,AGE,COUNTRY,CONTACT) values (?,?,?,?,?,?)",(uname,email_id,password,Age,Country,contact))
        conn.commit()
        flash('Details added','success')
        return redirect(url_for("index"))
    return render_template("add_user.html")

@app.route("/edit_user/<string:uid>", methods=['POST', 'GET'])
def edit_user(uid):
    if request.method == 'POST':
        uname = request.form['uname']
        email_id = request.form['email_id']
        password = request.form['password']
        Age = request.form['Age']
        Country = request.form['Country']
        contact = request.form['contact']
        conn = sql.connect("db_web.db")
        cur = conn.cursor()
        cur.execute("update users set UNAME=?, EMAIL_ID=?,PASSWORD=?,AGE=?,COUNTRY=?,CONTACT=? where UID=?", (uname,email_id,password,Age,Country,contact,uid))
        conn.commit()
        flash('Details Updated', 'success')
        return redirect(url_for("index"))
    conn = sql.connect("db_web.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("select * from users where UID=?", (uid,))
    data = cur.fetchone()
    return render_template("edit_user.html", datas=data)

@app.route("/delete_user/<string:uid>", methods=['GET'])
def delete_user(uid):
    conn = sql.connect("db_web.db")
    cur = conn.cursor()
    cur.execute("delete from users where UID=?", (uid,))
    conn.commit()
    flash('Details Deleted', 'warning')
    return redirect(url_for("index"))


if __name__=='__main__':
    app.secret_key='moni123'
    app.run(host='127.0.0.1',port=8005,debug=True)