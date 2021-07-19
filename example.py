"""
from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px
app = Flask(__name__)
@app.route(‘/’)
def notdash():
   df = pd.DataFrame({
      “Fruit”: [“Apples”, “Oranges”, “Bananas”, “Apples”, “Oranges”, “Bananas”],
      “Amount”: [4, 1, 2, 2, 4, 5],
      “City”: [“SF”, “SF”, “SF”, “Montreal”, “Montreal”, “Montreal”]
   })
fig = px.bar(df, x=”Fruit”, y=”Amount”, color=”City”,    barmode=”group”)
graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
return render_template(‘notdash.html’, graphJSON=graphJSON)



<!doctype html>
<html>
 <body>
  <h1>Hello Plotly (but not Dash)</h1>
  <div id=”chart” class=”chart”></div>
</body>
<script src=”https://cdn.plot.ly/plotly-latest.min.js"></script>
<script type=”text/javascript”>
  var graphs = {{graphJSON | safe}};
  Plotly.plot(‘chart’,graphs,{});
</script>
</html>






"""