import sqlite3
import flask


def run_sql(sql):
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row

        return connection.execute(sql).fetchall()


app = flask.Flask(__name__)


@app.get("/movie/<title>")
def step_1(title):
    sql = f''' select * from netflix where title = '{title}'
               order by date_added desc
               limit 1 '''

    result = None
    for item in run_sql(sql):
        result = dict(item)
    return flask.jsonify(result)


@app.get("/movie/<int:year1>/to/<int:year2>")
def step_2(year1, year2):
    sql = f''' select title, release_year from netflix 
               where release_year between {year1} and {year2}
               '''

    result = []
    for item in run_sql(sql):
        result.append(dict(item))
    return flask.jsonify(result)


@app.get("/rating/<rating>")
def step_3(rating):
    temp_dict = {
        "children": ("G", "G"),
        "family": ("G", "PG", "PG-13"),
        "adult": ("N", "NC-17")

    }

    sql = f''' select title, rating, description from netflix 
               where rating in {temp_dict.get(rating, ('PG-13', 'NC-17'))}
               '''

    result = []
    for item in run_sql(sql):
        result.append(dict(item))
    return flask.jsonify(result)


@app.get("/genre/<genre>")
def step_4(genre):
    sql = f''' select * from netflix 
               where listed_in like %{genre.title()}%
               '''

    result = []
    for item in run_sql(sql):
        result.append(dict(item))
    return flask.jsonify(result)


def step_5(name_1="Rose McIver", name_2="Ben Lamb"):
    sql = f''' select "cast" from netflix 
               where "cast" like %{name_1}% and "cast" like %{name_2}%
               '''

    result = []
    for item in run_sql(sql):
        result.append(dict(item))
    main_name = {}
    for item in result:
        names = item.get("cast").split(", ")
        for name in names:
            if name in main_name.keys():
                main_name[name] += 1
            else:
                main_name[name] = 1

    result=[]
    for item in main_name:
        if item not in (name_1, name_2) and main_name[item] >= 2:
            result.append(item)

    return result







if __name__ == '__main__':
    app.run(host='localhost', port=5000)
