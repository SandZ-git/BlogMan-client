from flask import Flask, render_template, url_for, request, redirect, jsonify
from datetime import date
import requests
from post import Post


app = Flask(__name__)


today_date = date.today()
current_year = date.today().year


def get_all_posts(posts_request):
    post_objects = []
    for post in posts_request["posts"]:
        post_obj = Post(
            post["id"],
            post["title"],
            post["subtitle"],
            post["body"],
            post["author_id"],
            post["country_id"],
            post["date"],
            post["image"],
        )
        post_objects.append(post_obj)
    return post_objects


@app.route('/', methods=["GET", "POST"])
def home():
    is_homepage = True
    if request.method == "POST":
        post_id = request.form.get("post_id", 0)
        post_id_delete = request.form.get("post_id_delete", 0)
        if post_id == '':
            post_id = 0
            return redirect(url_for('show_post', post_id=post_id))
        elif post_id != 0:
            return redirect(url_for('show_post', post_id=post_id))
        if post_id_delete == '':
            post_id_delete = 0
            return redirect(url_for('delete_post', post_id_delete=post_id_delete))
        elif post_id_delete != 0:
            return redirect(url_for('delete_post', post_id_delete=post_id_delete))

    return render_template("index.html", current_year=current_year, is_homepage=is_homepage)


@app.route('/posts')
def posts():
    posts_result = requests.get("http://127.0.0.1:5000/api/post").json()
    return render_template("posts.html", current_year=current_year, all_posts=get_all_posts(posts_result))


@app.route("/posts/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    requested_post = requests.get(f"http://127.0.0.1:5000/api/post/{post_id}").json()
    is_error = False
    if list(requested_post.keys())[0] == 'error':
        is_error = True
        post_obj = requested_post["error"]["Not Found"]
    else:
        post_obj = Post(
            requested_post["post"]["id"],
            requested_post["post"]["title"],
            requested_post["post"]["subtitle"],
            requested_post["post"]["body"],
            requested_post["post"]["author_id"],
            requested_post["post"]["country_id"],
            requested_post["post"]["date"],
            requested_post["post"]["image"],
        )
    return render_template("post.html", requested_post=post_obj, is_error=is_error)


@app.route("/delete/<int:post_id_delete>", methods=["GET", "POST"])
def delete_post(post_id_delete):
    post_id = post_id_delete
    requested_post = requests.delete(f"http://127.0.0.1:5000/api/post/{post_id}").json()
    is_response = False

    message = ''
    if requested_post == '':
        message = ""
        return redirect(url_for('home'))
    is_error = False
    if list(requested_post.keys())[0] == 'error':
        is_error = True
        post_obj = requested_post["error"]["Not Found"]
    elif list(requested_post.keys())[0] == 'response':
        is_response = True
        post_obj = requested_post["response"]["success"]

    return render_template('post-deleted.html', post_id=post_id, requested_post=post_obj, is_error=is_error, is_response=is_response)


@app.route("/new-post", methods=["GET", "POST"])
def create_post():
    api_url = 'http://127.0.0.1:5000/api/post'
    if request.method == "POST":
        data = dict(request.form)

        headers = {"Content-Type": "application/json"}
        response = requests.post(api_url, json=data, headers=headers)

        is_error = False

        if response.status_code == 200:
            r_text = response.text
        else:
            is_error = True
            r_text = "There was issue processing the request"
        return render_template('response.html', response=r_text, is_error=is_error)

    return render_template('new-post.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8181, debug=True)