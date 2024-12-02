import numpy as np
from sklearn.linear_model import LinearRegression

# Dummy Traffic Model
model = LinearRegression()
model.fit([[0], [12], [24]], [[5], [50], [10]])  # Traffic peaks at midday

def predict_traffic(time_of_day):
    time_of_day = np.array([[time_of_day]])
    return float(model.predict(time_of_day)[0])
