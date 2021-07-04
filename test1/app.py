from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)


def get_cursor():
    config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'passwd': 'root',
        'db': 'ClassFive',
        'charset': 'utf8'
    }
    conn = pymysql.connect(**config)
    conn.autocommit(1)  # conn.autocommit(True)
    return conn.cursor()


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/index')
def index2():
    return render_template("index.html")


@app.route('/login', methods=['post'])
def login():
    name = request.form.get("name")
    password = request.form.get("password")
    print(name)
    print(password)
    cursor = get_cursor()  # 打开数据库
    row = cursor.execute("select * from manage where name = %s", (name))  # 获取查询到的信息条数
    if row:
        cursor.execute("select password from manage where name = %s", (name))
        message = cursor.fetchone()
        print(message[0])
        print(password)
        if password == str(message[0]):
            cursor.execute("select * from list")
            lists = cursor.fetchall()
            return render_template("manage.html", name=name, lists=lists)
        else:
            cursor.execute("select * from list")
            lists = cursor.fetchall()
            return render_template("student.html", name=name, lists=lists)
    else:
        msg = "您不是管理员！"
        return render_template("index.html", msg=msg)
    

@app.route('/insert', methods=['post'])
def insert():
    Name = request.form.get("Name")
    ID = request.form.get("ID")
    Sex = request.form.get("Sex")
    RoomID = request.form.get("RoomID")
    GPA = request.form.get("GPA")

    value = (Name, ID, Sex, RoomID, GPA)
    insert_sql = '''INSERT INTO list(Name,ID, Sex,RoomID,GPA) values (%s,%s,%s,%s,%s)'''
    cursor = get_cursor()  # 打开数据库
    cursor.execute(insert_sql, value)  # 执行sql语句
    msg="添加成功！"
    return msg


@app.route('/delete/<int:Name>')
def delete(Name):
    cursor = get_cursor()  # 打开数据库
    cursor.execute("delete from list where Name = %s", (Name))  # 删除某一行值
    msg="删除成功！"
    return msg


@app.route('/update',methods=['post'])
def update():
    Name = request.form.get("Name")
    ID = request.form.get("ID")
    Sex = request.form.get("Sex")
    RoomID = request.form.get("RoomID")
    GPA = request.form.get("GPA")
    value = ( ID, Sex, RoomID, GPA,Name)
    cursor = get_cursor()  # 打开数据库
    cursor.execute("update list set ID = %s,Sex = %s,RoomID =%s,GPA = %s  where Name = %s", value)  # 删除某一行值
    msg="编辑成功！"
    return msg


if __name__ == '__main__':
    app.run()
