import json

import pymysql


def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as behaviors_json_file:
        behaviors_json_str = behaviors_json_file.read()
        behaviors_json = json.loads(behaviors_json_str)

    return behaviors_json

def insert_data(data):
    behaviors = data.get("returnValue")
    db = pymysql.Connect(host="localhost", port=3306, user="root",
                         password="dchancjc@163",
                         database="Flask1026", charset='utf8')
    cursor = db.cursor()
    for behavior in behaviors:
        b_name = behavior.get("b_name")
        b_status = behavior.get("b_status")
        b_score = behavior.get("b_score")
        cursor.execute("INSERT INTO behavior(b_name, b_status, b_score) "
                       "VALUES('%s', '%s', %f);" % (b_name, b_status, b_score))
        db.commit()
        print(behavior)

if __name__ == '__main__':
    filepath = "D:/Pycharm/Practices/flaskProject/1026/doc/behaviors2.json"
    data = load_data(filepath)
    insert_data(data)
