from flask import Flask, render_template, request

app = Flask(__name__)

# Home Page
@app.route('/')
def home():
    return render_template('index.html')


# EMI Calculator
@app.route('/EMI_Calculator', methods=['GET', 'POST'])
def emi():

    emi_result = None
    total_payment = None
    total_interest = None

    if request.method == 'POST':
        try:
            principal = float(request.form['principal'])
            rate = float(request.form['rate'])
            tenure = int(request.form['tenure'])

            monthly_rate = rate / (12 * 100)
            months = tenure * 12

            emi_result = (
                principal *
                monthly_rate *
                ((1 + monthly_rate) ** months)
            ) / (
                ((1 + monthly_rate) ** months) - 1
            )

            total_payment = emi_result * months
            total_interest = total_payment - principal

            emi_result = round(emi_result, 2)
            total_payment = round(total_payment)
            total_interest = round(total_interest)

        except Exception as e:
            return f"Error: {e}"

    return render_template(
        'EMI_Calculator.html',
        emi=emi_result,
        total_payment=total_payment,
        total_interest=total_interest
    )

@app.route('/FD_Calculator', methods=['GET', 'POST'])
def fd():
     maturity_amount = None
     interest_earned = None

     if request.method == 'POST':
         principal = float(request.form['principal'])
         rate = float(request.form['rate'])
         tenure = float(request.form['tenure'])
         maturity_amount = principal * ((1 + rate / 100) ** tenure)
         interest_earned = maturity_amount - principal
         maturity_amount = round(maturity_amount)
         interest_earned = round(interest_earned)
     
     return render_template(
         'FD_Calculator.html',
        maturity_amount=maturity_amount,
        interest_earned=interest_earned
        )

@app.route('/RD_Calculator', methods=['GET', 'POST'])
def rd():
    maturity_amount = None
    total_investment = None
    interest_earned = None

    if request.method == 'POST':

        monthly_deposit = float(request.form['monthly_deposit'])
        annual_rate = float(request.form['rate'])
        tenure_months = int(request.form['tenure'])
        quarterly_rate = annual_rate / 400
        maturity_amount = 0

        for month in range(tenure_months):
            remaining_months = tenure_months - month

            maturity_amount += monthly_deposit * (
                (1 + quarterly_rate) **
                (remaining_months / 3)
            )

        total_investment = monthly_deposit * tenure_months
        interest_earned = maturity_amount - total_investment

        maturity_amount = round(maturity_amount)
        total_investment = round(total_investment)
        interest_earned = round(interest_earned)

    return render_template(
        'RD_Calculator.html',
        maturity_amount=maturity_amount,
        total_investment=total_investment,
        interest_earned=interest_earned
    )

@app.route('/SIP_Calculator', methods=['GET', 'POST'])
def sip():

    invested_amount = None
    estimated_returns = None
    maturity_amount = None

    if request.method == 'POST':

        monthly_investment = float(request.form['monthly_investment'])
        annual_return = float(request.form['annual_return'])
        years = int(request.form['years'])

        months = years * 12
        monthly_rate = annual_return / (12 * 100)

        maturity_amount = (
            monthly_investment *
            (((1 + monthly_rate) ** months - 1) / monthly_rate) *
            (1 + monthly_rate)
        )

        invested_amount = monthly_investment * months
        estimated_returns = maturity_amount - invested_amount

        maturity_amount = round(maturity_amount)
        invested_amount = round(invested_amount)
        estimated_returns = round(estimated_returns)

    return render_template(
        'SIP_Calculator.html',
        invested_amount=invested_amount,
        estimated_returns=estimated_returns,
        maturity_amount=maturity_amount
    )

@app.route('/PPF_Calculator', methods=['GET', 'POST'])
def ppf():

    total_investment = None
    interest_earned = None
    maturity_amount = None

    if request.method == 'POST':
        yearly_investment = float(request.form['Investment'])
        years = int(request.form['Time'])
        annual_rate = 7.1
        maturity_amount = 0
        for year in range(years):
            maturity_amount = (
                maturity_amount + yearly_investment
            ) * (1 + annual_rate / 100)
        total_investment = yearly_investment * years
        interest_earned = maturity_amount - total_investment
        total_investment = round(total_investment)
        interest_earned = round(interest_earned)
        maturity_amount = round(maturity_amount)
        
    return render_template(
        'PPF_Calculator.html',
        total_investment=total_investment,
        interest_earned=interest_earned,
        maturity_amount=maturity_amount
    )

@app.route("/SWP_Calculator", methods=["GET", "POST"])
def swp():

    invested_amount = None
    total_withdrawal = None
    estimated_returns = None
    remaining_balance = None

    if request.method == "POST":

        total_investment = float(request.form["total_investment"])
        monthly_withdrawal = float(request.form["monthly_withdrawal"])
        annual_return = float(request.form["annual_return"])
        years = int(request.form["years"])

        monthly_rate = annual_return / 12 / 100
        total_months = years * 12

        balance = total_investment
        total_withdrawal = 0

        for _ in range(total_months):

            # Add monthly return
            balance += balance * monthly_rate

            # Withdraw monthly amount
            balance -= monthly_withdrawal

            total_withdrawal += monthly_withdrawal

            # Stop if balance is exhausted
            if balance <= 0:
                balance = 0
                break

        invested_amount = round(total_investment, 2)
        remaining_balance = round(balance, 2)

        estimated_returns = round(
            remaining_balance + total_withdrawal - invested_amount,
            2
        )

        total_withdrawal = round(total_withdrawal, 2)

    return render_template(
        "SWP_Calculator.html",
        invested_amount=invested_amount,
        total_withdrawal=total_withdrawal,
        estimated_returns=estimated_returns,
        remaining_balance=remaining_balance
    )


if __name__ == "__main__":
    app.run(debug=True)
