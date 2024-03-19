from flask import Flask, render_template
import plotly.graph_objs as go

app = Flask(__name__)

@app.route('/')
def index():
    # Данные для графика (здесь предполагается что-то типа продаж и прибыли по времени)
    x_data = ['Янв', 'Фев', 'Март', 'Апр', 'Май']
    y_sales_data = [100, 120, 150, 110, 130]
    y_profit_data = [50, 60, 70, 55, 65]

    # Создание линейного графика с точками
    trace1 = go.Scatter(x=x_data, y=y_sales_data, mode='lines+markers', name='Продажи')
    trace2 = go.Scatter(x=x_data, y=y_profit_data, mode='lines+markers', name='Прибыль')

    layout = go.Layout(title='Динамика продаж и прибыли',
                       xaxis=dict(title='Месяц'),
                       yaxis=dict(title='Сумма'),
                       margin=dict(l=20, r=20, t=40, b=20))

    fig = go.Figure(data=[trace1, trace2], layout=layout)

    # Преобразование графика в HTML
    graph_html = fig.to_html(full_html=False)

    return render_template('index.html', graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)