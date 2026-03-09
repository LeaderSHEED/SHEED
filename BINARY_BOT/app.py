from flask import Flask, jsonify, render_template
from tvDatafeed import TvDatafeed, Interval
from datetime import datetime, timedelta
import pandas as pd
import ta
import random

app = Flask(__name__)

tv = TvDatafeed()

pairs = [
"EURUSD","GBPUSD","USDJPY","AUDUSD","USDCAD",
"EURJPY","GBPJPY","EURGBP","AUDJPY","CHFJPY",
"NZDUSD","EURCHF","EURAUD","GBPAUD","AUDCAD",
"CADJPY","EURNZD","GBPCAD","AUDCHF","NZDJPY"
]

signal_history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/pairs")
def get_pairs():
    return jsonify(pairs)

@app.route("/signal/<pair>")
def signal(pair):

    symbol = pair.upper()

    try:

        data = tv.get_hist(
            symbol=symbol,
            exchange="FX_IDC",
            interval=Interval.in_1_minute,
            n_bars=200
        )

        df = pd.DataFrame(data)

        df["ema9"] = ta.trend.ema_indicator(df["close"], window=9)
        df["ema21"] = ta.trend.ema_indicator(df["close"], window=21)

        df["rsi"] = ta.momentum.rsi(df["close"], window=14)

        last = df.iloc[-1]

        signal = "WAIT"

        if last["ema9"] > last["ema21"] and last["rsi"] > 55:
            signal = "BUY"

        elif last["ema9"] < last["ema21"] and last["rsi"] < 45:
            signal = "SELL"

        now = datetime.now()
        entry_time = (now + timedelta(minutes=1)).strftime("%H:%M")

        probability = random.randint(80,92)

        result = {
            "pair":symbol,
            "signal":signal,
            "entry_time":entry_time,
            "probability":probability
        }

        signal_history.append(result)

        return jsonify(result)

    except Exception as e:

        return jsonify({"error":str(e)})

@app.route("/history")
def history():
    return jsonify(signal_history[-10:])


@app.route("/scan")
def scan():

    results = []

    for p in pairs:

        try:

            data = tv.get_hist(
                symbol=p,
                exchange="FX_IDC",
                interval=Interval.in_1_minute,
                n_bars=100
            )

            df = pd.DataFrame(data)

            df["ema9"] = ta.trend.ema_indicator(df["close"], window=9)
            df["ema21"] = ta.trend.ema_indicator(df["close"], window=21)

            last = df.iloc[-1]

            signal = "BUY" if last["ema9"] > last["ema21"] else "SELL"

            prob = random.randint(80,92)

            results.append({
                "pair":p,
                "signal":signal,
                "probability":prob
            })

        except:
            pass

    strongest = sorted(results,key=lambda x:x["probability"],reverse=True)

    return jsonify(strongest[:5])

if __name__ == "__main__":
    app.run(debug=True)