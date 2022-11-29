from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

def get_complementary(color):
    color = color[1:]
    color = int(color, 16)
    comp_color = 0xFFFFFF ^ color
    comp_color = "#%06X" % comp_color
    return comp_color

def change_bg_color(color):
    # Change background color
    return

def change_fg_color(color):
    comp_color = get_complementary(color)
    # Change text color
    return


if __name__ == '__main__':
   app.run()