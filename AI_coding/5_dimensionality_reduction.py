import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split

# === STEP 1: Create or Load Dataset ===
try:
    dataset = list(np.load("5_drawings.npy", allow_pickle=True))
except FileNotFoundError:
    dataset = []

# === STEP 2: Add a New Drawing ===
# Simulate a new 20x20 drawing (replace this with real input)
new_drawing = np.random.rand(20, 20)
dataset.append(new_drawing)

# Save dataset
np.save("5_drawings.npy", np.array(dataset))

# === STEP 3: Prepare Data ===
X = np.array(dataset).astype("float32")
X = np.reshape(X, (len(X), 20, 20, 1))

# If dataset has only 1 sample, skip split
if len(X) > 1:
    X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)
else:
    X_train = X_test = X

# === STEP 4: Build Conv Autoencoder ===
input_img = Input(shape=(20, 20, 1))

# Encoder
x = Conv2D(16, (3, 3), activation='relu', padding='same')(input_img)
x = MaxPooling2D((2, 2), padding='same')(x)
x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
encoded = MaxPooling2D((2, 2), padding='same')(x)

# Decoder
x = Conv2D(8, (3, 3), activation='relu', padding='same')(encoded)
x = UpSampling2D((2, 2))(x)
x = Conv2D(16, (3, 3), activation='relu', padding='same')(x)
x = UpSampling2D((2, 2))(x)
decoded = Conv2D(1, (3, 3), activation='sigmoid', padding='same')(x)

autoencoder = Model(input_img, decoded)
autoencoder.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy')

# === STEP 5: Train ===
autoencoder.fit(
    X_train, X_train,
    epochs=150,
    batch_size=16,
    shuffle=True,
    validation_data=(X_test, X_test)
)


# === STEP 6: Visualization helper functions ===
def rescale_and_gamma(img, gamma=0.5):
    # img in [0,1]
    min_val, max_val = img.min(), img.max()
    if max_val - min_val < 1e-8:
        return np.zeros_like(img)
    img_rescaled = (img - min_val) / (max_val - min_val)
    return np.power(img_rescaled, gamma)


# === STEP 7: Visualize ===
decoded_imgs = autoencoder.predict(X_test)

n = min(10, len(decoded_imgs))
plt.figure(figsize=(20, 4))
for i in range(n):
    ax = plt.subplot(2, n, i + 1)
    plt.imshow(X_test[i].reshape(20, 20), cmap='gray', vmin=0, vmax=1)
    plt.title("Original")
    plt.axis('off')

    ax = plt.subplot(2, n, i + 1 + n)
    corrected_img = rescale_and_gamma(decoded_imgs[i].reshape(20, 20))
    plt.imshow(corrected_img, cmap='gray', vmin=0, vmax=1)
    plt.title("Rebuilt")
    plt.axis('off')

plt.show()


