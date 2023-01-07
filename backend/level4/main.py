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

    # Calculation of the commission
    commission = price * 0.3
    insurance_fee = commission / 2
    assistance_fee = nb_days * 100
    drivy_fee = commission - insurance_fee - assistance_fee


    return {
        "price": round(price),
        "commission": {
            "insurance_fee": round(insurance_fee),
            "assistance_fee": round(assistance_fee),
            "drivy_fee": round(drivy_fee)
        }
    }

# Calculate the actions (credits and debits) for each actor for the given rental and price.
# Returns a list of dictionaries with keys 'who', 'type', and 'amount'.
def get_rental_actions(rental, price):
    actions = []
    actors = [
        {"who": "driver", "type": "debit", "amount": round(price['price'])},
        {"who": "owner", "type": "credit", "amount": round(price['price'] * 0.7)},
        {"who": "insurance", "type": "credit", "amount": round(price['commission']['insurance_fee'])},
        {"who": "assistance", "type": "credit", "amount": round(price['commission']['assistance_fee'])},
        {"who": "drivy", "type": "credit", "amount": round(price['commission']['drivy_fee'])}
    ]

    for actor in actors:
        actions.append({
            "who": actor['who'],
            "type": actor['type'],
            "amount": actor['amount']
        })

    return actions

    
# Load of the data from the file input.json
with open('data/input.json') as f:
    data = json.load(f)

# Initialisation of the dictionnary written in the file output.json
    output_data = {
        "rentals": []
    }

#Loop for each rent
for rental in data['rentals']:
    # Matching the car with the rent
    car = [c for c in data['cars'] if c['id'] == rental['car_id']][0]
    #Calculation of the price
    price = get_rental_price(rental, car)
    actions = get_rental_actions(rental,price)
    #Update of the dictionnary
    output_data['rentals'].append({
            "id": rental['id'],
            "actions":actions
        })

# Save of the results in the file output.json
with open('data/output.json', 'w') as f:
    json.dump(output_data, f, indent=2)

