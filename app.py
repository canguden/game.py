from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

bankroll = 500

def print_bankroll():
    return "Your current bankroll: $" + str(bankroll)

def take_bet():
    while True:
        try:
            bet = int(request.form.get("bet"))
            if bet <= bankroll and bet > 0:
                return bet
            else:
                return "Enter validd amount"
        except ValueError:
            return "Dont exceed bankroll"

def play_roulette():
    global bankroll
    numbers = list(range(37))
    even = list(range(0, 37, 2))
    odd = list(range(1, 37, 2))
    zero = [0]


    bet = take_bet()

    random_number = random.choice(numbers)

    if random_number in even:
        result_color = 'black'
    elif random_number in odd:
        result_color = 'red'
    else:
        result_color = 'green'

    if (bet == 1 and result_color == 'black') or \
       (bet == 2 and result_color == 'red') or \
       (bet == 3 and random_number == 0):
        if bet == 3:
            winnings = bet * 36
        else:
            winnings = bet * 2
        bankroll += winnings
        return {"result": "Winner Winner Chicken Dinner! You won $" + str(winnings), "number": random_number, "color": result_color}
    else:
        bankroll -= bet
        return {"result": "Uhhhh Unlucky Mate, you lost $" + str(bet), "number": random_number, "color": result_color}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        result_data = play_roulette()
        bankroll_status = print_bankroll()
        return render_template('index.html', result=result_data["result"], bankroll_status=bankroll_status, number=result_data["number"], color=result_data["color"])
    else:
        return render_template('index.html', result='', bankroll_status=print_bankroll(), number='', color='')

if __name__ == '__main__':
    app.run(debug=True)
