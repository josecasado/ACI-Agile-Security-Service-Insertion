from flask import Flask, render_template, url_for, request, redirect, flash, session
from datetime import datetime
from logging import DEBUG
from fw import asavg, asavi, asaphyg, asaphyi, ftdv3g, ftdv3i, ftdv4g, ftdv4i

# var
my_title = "Perimeter"
my_title1 = "Data Base"
my_text = "ASA: virtual or physical"


app = Flask(__name__)
# app.logger.setLevel(DEBUG)

bookmarks = []

app.secret_key = '\x17N\x1e\x14+h\x1fV\xd6\x83\x80+\x9fNZ1\x9d\x92\xc3\x04\xcf\x1c\xc5\xa3'


def store_bookmark(url):
    bookmarks.append(dict(url=url, user="jcasado", date=datetime.utcnow()))


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title=my_title, title1=my_title1, text=my_text)


@app.route("/despliegagextv", methods=["GET", "POST"])
def despliegagextv():
    if request.method == "POST":
        if 'despliega asa virtual' in request.form:
            # print "Deployed Graph virtual asa "
            result = asavi()
            if result:
                print "result = True"
                mensaje = "ASAv"
                flash("Service Graph deployed: {}".format(mensaje))
                return redirect(url_for("index"))
            else:
                return redirect(url_for("index"))
        else:
            pass
    return render_template("despliegagextv.html")


@app.route("/despliegagextphy", methods=["GET", "POST"])
def despliegagextphy():
    if request.method == "POST":
        if 'despliega asa fisico' in request.form:
            # print "Desplegado Graph asa virtual"
            result = asaphyi()
            if result:
                print "result True"
                mensaje = "ASA-5515"
                flash("Service Graph deployed: {}".format(mensaje))
                return redirect(url_for("index"))
            else:
                return redirect(url_for("index"))
        else:
            pass
    return render_template("despliegagextphy.html")

@app.route("/despliegagftdv3", methods=["GET", "POST"])
def despliegagftdv3():
    if request.method == "POST":
        if 'despliega ftdv3' in request.form:
            # print "Desplegado Graph asa virtual"
            result = ftdv3i()
            if result:
                mensaje = "FTDv Unmanaged"
                flash("Service Graph deployed: {}".format(mensaje))
                return redirect(url_for("index"))
            else:
                return redirect(url_for("index"))
        else:
            pass
    return render_template("despliegagftdv3.html")

@app.route("/despliegagftdv4", methods=["GET", "POST"])
def despliegagftdv4():
    if request.method == "POST":
        if 'despliega ftdv4' in request.form:
            # print "Desplegado Graph asa virtual"
            result = ftdv4i()
            if result:
                print "result True"
                mensaje = "FTDv Managed"
                flash("Service Graph deployed: {}".format(mensaje))
                return redirect(url_for("index"))
            else:
                return redirect(url_for("index"))
        else:
            pass
    return render_template("despliegagftdv4.html")


@app.route("/insertagext", methods=["GET", "POST"])
def insertagext():
    if request.method == "POST":
        if 'asa virtual' in request.form:
            # print "asa virtual"
            result = asavg()
            if result:
                mensaje = "Asa Virtual"
                flash("Service Graph ready: {}".format(mensaje))
                return redirect(url_for("despliegagextv"))
            else:
                return redirect(url_for("despliegagextv"))
        elif 'asa fisico' in request.form:
            # print "ASA Fisico"
            result = asaphyg()
            if result:
                mensaje = "Physical ASA"
                flash("Service Graph ready: {}".format(mensaje))
                return redirect(url_for("despliegagextphy"))
            else:
                return redirect(url_for("despliegagextphy"))
        else:
            pass
    return render_template("insertagext.html")


@app.route("/insertagint", methods=["GET", "POST"])
def insertagint():
    if request.method == "POST":
        if 'ftdvu' in request.form:
            result = ftdv3g()
            if result:
                mensaje = "FTD Unmanaged"
                flash("Service Graph ready: {}".format(mensaje))
                return redirect(url_for("despliegagftdv3"))
            else:
                return redirect(url_for("despliegagftdv3"))
        elif 'ftdvm' in request.form:
            result = ftdv4g()
            if result:
                print result
                mensaje = "FTD Managed"
                flash("Service Graph ready: {}".format(mensaje))
                return redirect(url_for("despliegagftdv4"))
            else:
                return redirect(url_for("despliegagftdv4"))
        else:
            pass
    return render_template("insertagint.html")



app.errorhandler(404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
