from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
       
        return render_template("Form.html")
    return render_template("Home.html")


def prediction(features):
    filename = '../notebooks/PricePredictor.pickle' 
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    predict = model.predict([features])
    return predict


@app.route('/Form.html', methods=['POST', 'GET'])
def form():
    pred = 0
    car_name = ""
    if request.method == 'POST':
        name = request.form['car-name']
        car_name = name  # Store the car name to pass to the template
        year = request.form['year']
        km_driven = request.form['km-driven']
        fuel_type = request.form['fuel-type']
        seller_type = request.form['seller-type']
        transmission = request.form['transmission']
        owner = request.form['owner']
        seats = request.form['seats']
        max_power = request.form['max-power']
        mileage = request.form['mileage']
        engine = request.form['engine']

        featureList = []
        name_list = ['Chevrolet', 'Ford', 'Honda', 'Hyundai', 'Mahindra', 'Maruti', 'Renault', 'Tata', 'Toyota', 'Volkswagen']
        featureList.append(int(year))
        featureList.append(float(km_driven))
        featureList.append(int(seats))
        featureList.append(float(max_power))
        featureList.append(float(mileage))
        featureList.append(int(engine))
        fuel_list = ['CNG', 'Diesel', 'LPG', 'Petrol']
        seller_list = ['Dealer', 'Individual', 'Trustmark Dealer']
        transmission_list = ['Manual', 'Automatic']
        owner_list = ['First Owner', 'Fourth & Above Owner', 'Second Owner', 'Test Drive Car', 'Third Owner']

        def traverse(lst, value):
            for item in lst:
                featureList.append(1 if item == value else 0)

        traverse(name_list, name)
        traverse(fuel_list, fuel_type)
        traverse(seller_list, seller_type)
        traverse(transmission_list, transmission)
        traverse(owner_list, owner)

        pred = prediction(featureList)
        pred = np.round(pred[0], 2) * 3.46
        
        pred = f"{pred:,.2f}"

       

    return render_template("Form.html", pred=pred, car_name=car_name)


if __name__ == '__main__':
    app.run(debug=True)
