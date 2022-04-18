import json
import random
from datetime import timedelta

import dateutil.parser

from flask import Flask, render_template, request, make_response

app = Flask(__name__)

# json list of all comments
COMMENTS = []
for i in open("out.json").readlines():
    COMMENTS.append(json.loads(i))

print(len(COMMENTS))


# turns a json comment into html where it will be put in the website
def old_format_comment(data, timezone_offset=0.):

    top_level = False
    com = data['snippet']  # data of the comment
    if 'topLevelComment' in data['snippet']:  # need to do further unwrapping if it's the top level comment
        top_level = True
        com = data['snippet']['topLevelComment']['snippet']

    text = com['textOriginal']  # text of the comment
    author = com['authorDisplayName']  # author of the comment's name
    time = dateutil.parser.parse(com['publishedAt']) + timedelta(hours=timezone_offset)  # published at time
    time_string = time.strftime("%b %d, %Y, %r")

    # add a link to the comment if top_level and begin building the html
    if top_level:
        out = '<a href="https://www.youtube.com/watch?v=zK4TWXWEKAQ&lc={0}" style="color: white" target="_blank">' \
              'Link to comment</a>' \
            .format(data['snippet']['topLevelComment']['id'])
    else:
        out = ""

    # add the text into the html
    out += "<p>" + text + "</p>"
    out += "<h4>" + " - " + author + ", " + time_string + "</h4>"

    # html is janky
    out = out.replace("\n", "<br>")

    # add replies (using recursion)
    if "replies" in data:
        out += '<br><div style="margin-left: 40px;">'
        for i in data['replies']['comments'][::-1]:
            out += format_comment(i)

        out += "</div>"

    # redundant... i think?
    # left in just in case
    return out.replace("\n", "<br>")

def format_comment(data, timezone_offset=0):
    text = data['text']
    author = data['author']

    # add the text into the html
    out = "<p>" + text + "</p>"
    out += "<h4>" + " - " + author + "<h4>"

    # html is janky
    return out.replace("\n", "<br>")


@app.route('/')
def main():
    return render_template("base.html", page="index")


@app.route('/<p>')
def page(p):
    return render_template("base.html", page=p)


@app.route('/get/index')
def index():
    return render_template("index.html")


@app.route('/get/comments')
def comments():
    return render_template("comments.html")


@app.route('/get/about')
def about():
    return render_template("about.html")


@app.route('/random_comment')
def random_comment():
    comment = random.choice(COMMENTS)
    timezone_offset = float(request.cookies.get("timezone_offset"))
    try:
        return format_comment(comment, timezone_offset=timezone_offset)
    except Exception as e:
        return "Something messed up\n" + str(comment) + "\n" + str(e)


@app.route("/getTime", methods=['GET'])
def get_time():
    print("Got user local time of", request.args.get("time"))
    resp = make_response("Done")
    resp.set_cookie("timezone_offset", str(
        (int(request.args.get("time").split("GMT")[1][1:3]) +
         int(request.args.get("time").split("GMT")[1][3:5]) / 60)
        * -1 if request.args.get("time").split("GMT")[1][0] == "-" else 1
    ))
    return resp


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)
