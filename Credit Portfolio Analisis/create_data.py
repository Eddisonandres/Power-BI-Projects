import random
from datetime import datetime, timedelta
# variables
num_credits = 50
credit_data = []
payer_good = False
loan_amount = 0
loan_term = 0
installment = 0
product_selection = 0
interest_rate = 0
int_rate_year = 0
principal_payment = 0
interest_payment = 0
random_days = 0
customer_paid = 0

# create the ids for the credits
products_id = [f'{1000 + i}' for i in range(num_credits)]

# constants
PRODUCTS = [1, 2, 3, 4] # 1: Education, 2: General, 3: Taxes loan, 4: Travel
RATE_PRODUCTS = [0.05, 0.08, 0.09, 0.1]
LOAN_TERMS = [12, 24, 36, 48, 60]
START_DATE_LOAN = datetime(2022, 1, 1)
END_DATE_LOAN = datetime(2024, 12, 31)
DELTA = END_DATE_LOAN - START_DATE_LOAN

random_date = START_DATE_LOAN
# simulation for each credit
for pid in products_id:
    # give the kind of payer, probability of 8% to bad payer
    payer_good = random.choices([False, True], weights = [0.08, 0.92], k=1) [0]
    # give a random loan amount
    loan_amount = random.randrange(50, 1000) * 10
    # select the position to the product code
    product_selection = random.randrange(0, len(PRODUCTS))
    # give a product code and interest rate
    products_code = PRODUCTS[product_selection]
    interest_rate = RATE_PRODUCTS[product_selection]
    int_rate_year = interest_rate / 12 # it takes 12 as months in the year
    # give a loan term
    loan_term = random.choice(LOAN_TERMS)
    # installment = [P * r * (1 + r)^n] / [(1 + r)^n - 1] 
    # calculate installment
    installment = loan_amount * ((int_rate_year) * (1 + int_rate_year)** loan_term) / (((1 + int_rate_year)** loan_term) -1)
    interest_payment = loan_amount * int_rate_year
    principal_payment = installment - interest_payment
    # create the disbursement date
    random_days = random.randint(0, DELTA.days)
    random_date = START_DATE_LOAN + timedelta(days=random_days)
    disbursement_date = random_date # variable to save the disbursement date
    # create historical month
    for mon in range(1, loan_term + 1):
        # create random payment with 70% of probability no payment when is not good payer
        if not payer_good:
            customer_paid = random.choices([False, True], weights= [0.2, 0.8], k=1) [0]
            