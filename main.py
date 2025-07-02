from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const
from datetime import datetime, timedelta

def degree_to_sign(deg):
    signs = [
        'Aries', 'Taurus', 'Gemini', 'Cancer',
        'Leo', 'Virgo', 'Libra', 'Scorpio',
        'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    index = int(deg / 30) % 12
    return signs[index]

def generate_html():
    now_jst = datetime.utcnow() + timedelta(hours=9)
    date_str = now_jst.strftime("%Y/%m/%d")

    dt = Datetime(date_str, "00:00", "+09:00")
    pos = GeoPos("35:41:22", "139:41:30")  # 東京

    chart = Chart(dt, pos, hsys=const.PLACIDUS)
    moon = chart.get(const.MOON)
    moon_deg = round(moon.normlon, 2)
    moon_sign = moon.sign
    moon_house = moon.house

    plus60 = (moon_deg + 60) % 360
    minus120 = (moon_deg - 120) % 360

    sign_p60 = degree_to_sign(plus60)
    sign_m120 = degree_to_sign(minus120)

    html = f"""
    <html>
    <head><meta charset="utf-8"><title>今日の月の位置</title></head>
    <body>
    <h1>今日の月の±60°/−120°</h1>
    <p><strong>日時:</strong> {date_str} 00:00 JST</p>
    <h2>月の位置</h2>
    <ul>
      <li>黄経: {moon_deg}°</li>
      <li>星座: {moon_sign}</li>
      <li>Placidusハウス: {moon_house}</li>
    </ul>
    <h2>月+60°の星座</h2>
    <p>{sign_p60}</p>
    <h2>月−120°の星座</h2>
    <p>{sign_m120}</p>
    </body>
    </html>
    """
    with open("output.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    generate_html()
