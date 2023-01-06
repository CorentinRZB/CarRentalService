import json
import datetime

def get_rental_price(rental, car):
    # Calculation of the location days
    start_date = datetime.datetime.strptime(rental['start_date'], '%Y-%m-%d')
    end_date = datetime.datetime.strptime(rental['end_date'], '%Y-%m-%d')
    nb_days = (end_date - start_date).days + 1

    # Initialisation of the price
    price = 0

    # Dictionnary of the reduction rates matching the rental days
    reductions = {
        1: 0.1,
        4: 0.3,
        10: 0.5
    }

    # Loop for each rental day
    for i in range(1, nb_days + 1):
        reduction = 0
        for threshold, rate in reductions.items():
            if i > threshold:
                reduction = rate

        # Calculation of the daily price with the good reduction rate
        daily_price = (1 - reduction) * car['price_per_day']
        # Adding the daily price to the total price
        price += daily_price

    # Adding the distance price to the total price
    price += rental['distance'] * car['price_per_km']
    return price

# Load of the data from the file input.json
with open('data/input.json') as f:
    data = json.load(f)

# Calculatation of the price for each location
result = []
for rental in data['rentals']:
    car = next(c for c in data['cars'] if c['id'] == rental['car_id'])
    price = get_rental_price(rental, car)
    result.append({'id': rental['id'], 'price': price})

# Save of the results in the file output.json
with open('data/output.json', 'w') as f:
    json.dump({'rentals': result}, f, indent=2)

