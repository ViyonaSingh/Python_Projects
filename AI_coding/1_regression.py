import numpy as np
from sklearn.ensemble import GradientBoostingRegressor as Model
import matplotlib.pyplot as plt


def load_data(filename):
    X = []
    y = []
    with open(filename, "r") as f:
        next(f)  # Skip header line
        for line in f:
            parts = line.strip().split(' ; ')
            if len(parts) != 6:
                continue
            features = list(map(float, parts[:5]))
            target = float(parts[5])
            X.append(features)
            y.append(target)
    return np.array(X), np.array(y)


def train_model(X, y):
    model = Model()
    model.fit(X, y)
    score = model.score(X, y)
    print(f"Model training R^2 score: {score:.6f}")
    return model, score


def plot_true_vs_pred(X, y, model):
    y_pred = model.predict(X)
    plt.figure(figsize=(8, 5))
    plt.scatter(list(range(len(y))), y, color='blue', s=10, label='True CO2 Emission')
    plt.scatter(list(range(len(y_pred))), y_pred, color='red', s=10, label='Predicted CO2 Emission', alpha=0.7)
    plt.xlabel('Sample Index')
    plt.ylabel('CO2 Emission (tons/year)')
    plt.title('True vs Predicted CO2 Emissions')
    plt.legend()
    plt.show()



def print_co2_emission_table():
    data = [
        ["🌍 Target", "🎯 Tons CO₂/person/year", "🟢 Climate Impact"],
        ["1.5°C Goal (Paris)", "2.0", "Very Sustainable ✅"],
        ["World Average", "4.7", "Too High ⚠️"],
        ["EU Average", "6–8", "Needs Improvement ⚠️"],
        ["US Average", "15–16", "Very High 🔥"],
        ["Climate Stability Ideal", "<2.0", "Perfect 🌿"],
    ]

    # Print table header
    print("=" * 52)
    for row in data:
        print(f"{row[0]:<25} | {row[1]:<15} | {row[2]:<10}")
        if row[0] == "🌍 Target":
            print("-" * 52)
    print("=" * 52)


def predict_new(model):
    print_co2_emission_table()
    print("\nEnter a new data point's 5 features separated by commas:")
    print("(flights_per_year, car_km_per_week, meat_kg_per_week, electricity_kwh_month, waste_kg_week)")
    input_str = input("Your input: ")
    try:
        features = list(map(float, input_str.split(',')))
        if len(features) != 5:
            print("Error: Please enter exactly 5 numeric values separated by commas.")
            return
        features_np = np.array(features).reshape(1, -1)
        prediction = model.predict(features_np)
        print(f"Predicted CO2 emission: {prediction[0]:.3f} tons per year")
    except ValueError:
        print("Error: Invalid input. Please enter numeric values only.")


def main():
    filename = "1_climate_impact.txt"
    X, y = load_data(filename)
    print(f"Loaded {X.shape[0]} samples with {X.shape[1]} features each.")

    model, score = train_model(X, y)
    plot_true_vs_pred(X, y, model)
    predict_new(model)


if __name__ == "__main__":
    main()
