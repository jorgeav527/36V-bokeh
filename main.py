from bokeh.embed import components
from bokeh.plotting import figure
from flask import Flask, render_template
import seaborn as sns
from bokeh.models import ColumnDataSource, HoverTool

app = Flask(__name__)

df = sns.load_dataset("mpg")


@app.route("/first")
def first():
    p = figure(title="Very Simple Bokeh Plot", height=300, width=500)
    p.line([1, 2, 3, 4], [4, 7, 2, 6], line_width=3)

    script_py, div_py = components(p)

    return render_template("index.html", script=script_py, div=div_py)


@app.route("/second")
def second():
    p = figure(
        title="Haz clic en la leyenda para filtrar",
        width=700,
        height=450,
        tools="pan,wheel_zoom,reset,hover",
    )
    hover = HoverTool()
    hover.tooltips = [
        ("Modelo", "@name"),
        ("Consumo (MPG)", "@mpg"),
        ("Caballos", "@horsepower"),
        ("Peso", "@weight"),
    ]

    for origen, color in zip(
        ["usa", "japan", "europe"], ["navy", "firebrick", "forestgreen"]
    ):
        source = ColumnDataSource(df[df["origin"] == origen])
        p.scatter(
            "weight",
            "mpg",
            source=source,
            size=10,
            color=color,
            alpha=0.6,
            legend_label=origen,
        )
        p.add_tools(hover)

    p.legend.click_policy = "hide"

    script_py, div_py = components(p)

    return render_template("index.html", script=script_py, div=div_py)
