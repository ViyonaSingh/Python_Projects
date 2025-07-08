import numpy as np
from sklearn.ensemble import IsolationForest


# Step 1: Generate synthetic "normal" biometric data
def generate_normal_data(n_samples=500):
    weight = np.random.normal(70, 10, n_samples)  # average 70kg ±10
    height = np.random.normal(170, 10, n_samples)  # average 170cm ±10
    age = np.random.normal(40, 15, n_samples)  # average 40 years ±15
    gender = np.random.choice([0, 1], n_samples)  # 0 = male, 1 = female
    smoking = np.random.choice([0, 1], n_samples, p=[0.8, 0.2])
    exercise_days = np.random.randint(0, 8, n_samples)

    X = np.vstack((weight, height, age, gender, smoking, exercise_days)).T
    return X


# Step 2: Train model
X_train = generate_normal_data()
model = IsolationForest(contamination=0.05, random_state=42)
model.fit(X_train)

# Step 3: Predefined test samples
test_samples = np.array([
    [68, 172, 38, 0, 0, 5],
    [80, 165, 45, 1, 0, 2],
    [120, 190, 70, 0, 1, 0],
    [40, 150, 25, 1, 1, 7],
    [200, 180, 50, 0, 1, 0],
])

print("📊 Predefined Test Results:")
predictions = model.predict(test_samples)
for i, sample in enumerate(test_samples):
    status = "Anomaly ❌" if predictions[i] == -1 else "Normal ✅"
    print(f"Sample {i + 1}: {sample} -> {status}")

# Step 4: User Input
print("\n🧪 Enter your own biometric values to test (type 'q' to quit):")

while True:
    try:
        user_input = input("\nEnter: weight, height, age, gender(0=male,1=female), smoking(0/1), exercise_days (0-7): ")
        if user_input.lower() == 'q':
            print("Exiting.")
            break

        # Parse and convert input
        parts = list(map(float, user_input.strip().split(',')))
        if len(parts) != 6:
            print("⚠️ Please enter exactly 6 comma-separated values.")
            continue

        sample = np.array([parts])
        prediction = model.predict(sample)[0]
        status = "Anomaly ❌" if prediction == -1 else "Normal ✅"
        print(f"Result: {status}")

    except Exception as e:
        print(f"Error: {e}")
