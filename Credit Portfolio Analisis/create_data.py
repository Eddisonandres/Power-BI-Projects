import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
# variables
credit_data = []
payer_good = False
loan_amount = 0
loan_term = 0
installment = 0
product_selection = 0
product_code = 0
interest_rate = 0
int_rate_year = 0
principal_payment = 0
interest_payment = 0
random_days = 0
customer_paid = 0
agency_code = 0
credit_data_all = []


# constants
NUM_CREDITS = 10
PRODUCTS = [1, 2, 3, 4] # 1: Education, 2: General, 3: Taxes loan, 4: Travel
RATE_PRODUCTS = [0.05, 0.08, 0.09, 0.1]
LOAN_TERMS = [12, 24, 36, 48, 60]
START_DATE_LOAN = datetime(2022, 1, 1)
END_DATE_LOAN = datetime(2024, 12, 31)
DELTA = END_DATE_LOAN - START_DATE_LOAN
AGENCIES = [10, 20, 30, 40, 50]
AMORTIZATION = 30

# function to add the record of each loan
def add_record(
    p_cut_month, 
    p_pid,
    p_disbursement_date,
    p_end_date,
    p_days_past_due,
    p_loan_term,
    p_amortization,
    p_loan_amount,
    p_interest_rate,
    p_installment_amount,
    p_outstanding_balance,
    p_agency_code,
    p_product_code
    ):
    record = {
        'cut_month': p_cut_month,
        'num_product': p_pid,
        'disbursement_date': p_disbursement_date,
        'end_date': p_end_date,
        'days_past_due': p_days_past_due,
        'loan_term': p_loan_term,
        'amortization': p_amortization,
        'loan_amount': p_loan_amount,
        'interest_rate': p_interest_rate,
        'installment_amount': p_installment_amount,
        'outstanding_balance': int(p_outstanding_balance),
        'agency_code': p_agency_code,
        'product_code': p_product_code
    }
    print(record)
    credit_data_all.append(record)

# create the ids for the credits
products_id = [f'{1000 + i}' for i in range(NUM_CREDITS)]
random_date = START_DATE_LOAN
# simulation for each credit
for pid in products_id:
    # give the kind of payer, probability of 8% to bad payer
    payer_good = random.choices([False, True], weights = [0.04, 0.6], k=1) [0]
    # give an agency code
    agency_code = random.choice(AGENCIES)
    # give a random loan amount
    loan_amount = random.randrange(50, 1000) * 10
    # select the position to the product code
    product_selection = random.randrange(0, len(PRODUCTS))
    # give a product code and interest rate
    product_code = PRODUCTS[product_selection]
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
    disbursement_date = START_DATE_LOAN + timedelta(days=random_days)
    #print(random_date)
    #disbursement_date = random_date.strftime('%d/%m/%Y') # variable to save the disbursement date
    # add the record for the disbursement to the dictionary
    add_record(disbursement_date.strftime('%y%m'),
        pid,
        disbursement_date.strftime('%d/%m/%y'),
        disbursement_date.strftime('%d/%m/%y'),
        0,
        loan_term,
        AMORTIZATION,
        loan_amount,
        interest_rate,
        installment,
        loan_amount,
        agency_code,
        product_code
        )
    # create historical month
    date_next_add = disbursement_date
    day_past_due = 0
    for mon in range(1, loan_term + 1):
        # create random payment with 80% of probability no payment when is not good payer
        if not payer_good:
            customer_paid = random.choices([False, True], weights= [0.8, 0.2], k=1) [0]
            print(customer_paid)
            # validate if customer paid
            if not customer_paid:
                if day_past_due == 0:
                    dayn = datetime.strptime(disbursement_date.strftime('%d/%m/%y'), '%d/%m/%y')
                    day_past_due = 30 - dayn.day
                else:
                    day_past_due = day_past_due + 30
                print(day_past_due)
            else:
                day_past_due = 0
        date_next_add = date_next_add + relativedelta(months=1)
        cut_date_next = date_next_add.strftime('%d/%m/%y')
        