import io
import random
from flask import Flask, Response, request, render_template, send_file
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG
import plots

from matplotlib.figure import Figure

app = Flask(__name__, template_folder='templates')


@app.route("/")
def show_plot():
    figure = plots.plot_city(city)
    figure.savefig('img/plot.png')
    return render_template("simple.html")

    # output = io.BytesIO()
    # FigureCanvasSVG(fig).print_svg(output)
    # return Response(output.getvalue(), mimetype="image/svg+xml")

if __name__ == '__main__':
    app.run()