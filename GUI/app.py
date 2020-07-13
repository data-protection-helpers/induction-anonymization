"""

"""


from flask import Flask, render_template, request
import sys
from smote import treatment
import pandas as pd

df = pd.read_csv("database.csv")
df = df[["DISTANCE", "ORIGIN_AIRPORT_ID", "DEST_AIRPORT_ID"]][:50]

GUI = Flask(__name__)


@GUI.route('/home', methods=['GET', 'POST'])
def home():
    """

    """
    if request.method == 'POST':

        return render_template('dataframe.html', tables=[df.to_html(classes='data')], titles=df.columns.values,
                               dataset_name="Initial dataset")

    return render_template('main_page.html')


@GUI.route('/selection', methods=['GET', 'POST'])
def select():
    """

    """
    if request.method == 'POST':

        multiselect = request.form.getlist('multi')
        global df_sample
        df_sample = df[multiselect]
        return render_template('dataframe.html', tables=[df_sample.to_html(classes='data')], titles=df_sample.columns.
                               values, dataset_name="Selected dataset")

    return render_template("selection.html",  tables=[df.to_html(classes='data')], titles=df.columns.values)


@GUI.route('/synthesization',  methods=['GET', 'POST'])
def synthesization():
    """

    """
    if request.method == 'POST':
        treatment(df_sample)
        return render_template('image.html')

    return render_template('synthesization.html')

@GUI.route('/anonymisation')
def anonymisation():
    """
    """
    return render_template('anonymisation.html')


if __name__ == '__main__':
    GUI.run(debug=True)