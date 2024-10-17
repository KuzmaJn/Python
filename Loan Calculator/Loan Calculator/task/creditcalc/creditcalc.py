import math, argparse


#ap - annuity payment, lp - loan principal, nop - number of payments, ir - interest rate
def annuity_payment(lp, nop, ir):
    ap = lp * ((ir * math.pow(1 + ir, nop)) / (math.pow(1 + ir, nop) - 1))
    return math.ceil(ap)


def loan_principal(ap, nop, ir):
    lp = ap / ((ir * math.pow(1 + ir, nop)) / (math.pow(1 + ir, nop) - 1))
    return lp


def number_of_payments(ap, lp, ir):
    nof = math.log((ap / (ap - ir * lp)), (1 + ir))
    nof = math.ceil(nof)
    return f'{nof // 12} years and {nof % 12} months'


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--payment', type=float, help='Monthly payment amount', default=None)
    parser.add_argument('--principal', type=int, help='Loan principal', default=None)
    parser.add_argument('--periods', type=int, help='Number of periods (months)', default=None)
    parser.add_argument('--interest', type=float, help='Interest rate', required=True)

    args = parser.parse_args()
    #args = [None, 1000000, 60, 10]
    monthly_interest = args.interest / (12 * 100)
    if args.payment is None:
        print(f'Your monthly payment = {annuity_payment(args.principal, args.periods, monthly_interest)}')
    elif args.principal is None:
        print(f'Your loan principal = {loan_principal(args.payment, args.periods, monthly_interest)}')
    elif args.periods is None:
        print(f'It will take {number_of_payments(args.payment, args.principal, monthly_interest)} to repay this loan!')

    else:
        print("Error occurred!")


if __name__ == '__main__':
    main()
