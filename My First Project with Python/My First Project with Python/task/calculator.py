# Write your code here
total_earned = {'Bubblegum': 202, 'Toffee': 118, 'Ice cream': 2250, 'Milk chocolate': 1680, 'Doughnut': 1075, 'Pancake': 80}
earned = 0.0
print('Earned amount:')
for key, value in total_earned.items():
    print(f'{key}: ${value}')
    earned += value

print()
print(f'Income: ${earned}')
staff = int(input('Staff expenses: '))
other = int(input('Other expenses: '))

net_income = earned - staff - other
print(f'Net income: ${net_income}')