import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
import matplotlib.pyplot as plt
from keras.losses import MeanSquaredError
from keras.models import load_model

# Load the dataset
file_path = 'model\data.csv' 
data = pd.read_csv(file_path)

# Select relevant columns
traffic_data = data[['year', 'cars_and_taxis', 'all_motor_vehicles']].dropna()

# Scale the features
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(traffic_data[['cars_and_taxis', 'all_motor_vehicles']])
traffic_data['scaled_cars_and_taxis'] = scaled_data[:, 0]
traffic_data['scaled_all_motor_vehicles'] = scaled_data[:, 1]

# Function to create sequences
def create_sequences(data, time_steps=12):
    X, y = [], []
    for i in range(len(data) - time_steps):
        X.append(data[i:i + time_steps, :])  # Input sequence (past data)
        y.append(data[i + time_steps, 0])  # Target ('cars_and_taxis')
    return np.array(X), np.array(y)

# Prepare sequences
time_steps = 12
sequence_data = traffic_data[['scaled_cars_and_taxis', 'scaled_all_motor_vehicles']].values
X, y = create_sequences(sequence_data, time_steps)

# Split data into training and testing sets
train_size = int(0.8 * len(X))
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Build the LSTM model
model = Sequential([
    LSTM(64, input_shape=(time_steps, 2), return_sequences=True),  # First LSTM layer
    Dropout(0.2),
    LSTM(32, return_sequences=False),  # Second LSTM layer
    Dropout(0.2),
    Dense(1)  # Output layer
])

# Compile the model
model.compile(optimizer='adam', loss='mse')

# Train the model
history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_split=0.2, verbose=1)

# Evaluate the model
loss = model.evaluate(X_test, y_test)
print(f"Test Loss: {loss}")

# Plot training history
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend()
plt.title('Model Loss')
plt.show()



#Custom objects mapping
custom_objects = {'mse': MeanSquaredError()}
model = load_model('model/traffic_forecasting_model.h5', custom_objects=custom_objects)

# Save the model for future use
model.save('model/traffic_forecasting_model.h5')

