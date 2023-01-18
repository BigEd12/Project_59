from flask import Flask, render_template, request
import requests
import datetime
import smtplib

MY_EMAIL = "olmos.edward@gmail.com"
MY_PASSWORD = "lshgrctaaymugbhv"

response = requests.get(url="https://api.npoint.io/e35454a27b2b7398e8e7")
all_posts = response.json()

day = datetime.date.today().day
month = datetime.date.today().strftime("%B")
year = datetime.date.today().year


today = f"{day} of {month}, {year}"

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", blogs=all_posts, date=today)

@app.route('/about')
def get_about_section():
    return render_template("about.html")


@app.route('/contact', methods=["GET", "POST"])
def get_contact_section():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone_num']
        message = request.form['message']
        all_details = (f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}")
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=email,
                msg=f"Subject:New contact from site\n\n{all_details}"
            )
        return render_template("contact.html", message="Successfully sent message")
    return render_template("contact.html", message="Contact Me")


@app.route('/post/<int:blog_id>')
def get_blog_post(blog_id):
    blog_post = all_posts[blog_id - 1]
    return render_template("post.html", post=blog_post, date=today)


if __name__ == "__main__":
    app.run(debug=True)