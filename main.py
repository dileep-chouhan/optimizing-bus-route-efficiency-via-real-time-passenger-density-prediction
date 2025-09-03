import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import norm
# --- 1. Synthetic Data Generation ---
# Generate synthetic data for bus passenger density at different times and locations
np.random.seed(42)  # for reproducibility
num_routes = 5
num_days = 30
num_timeslots = 24 #24 hours in a day
dates = pd.date_range(start='2024-03-01', periods=num_days)
times = np.arange(num_timeslots)
route_data = []
for route in range(1, num_routes + 1):
    for day in dates:
        for time in times:
            # Simulate passenger density with some noise
            base_density = 100 + 50 * np.sin(2 * np.pi * time / 24) + 20 * np.random.randn() # diurnal pattern
            passenger_density = max(0, int(base_density + 20 * np.random.randn())) #add noise and ensure non-negative values
            route_data.append({'Route': route, 'Date': day, 'Time': time, 'PassengerDensity': passenger_density})
df = pd.DataFrame(route_data)
# --- 2. Data Analysis ---
#Calculate average passenger density per route and time slot
average_density = df.groupby(['Route', 'Time'])['PassengerDensity'].mean().unstack()
#Fit a Gaussian curve to the average density for each route to predict future density
def gaussian(x, amp, mu, sig):
    return amp * np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))
predictions = {}
for route in average_density.index:
    ydata = average_density.loc[route].values
    xdata = np.arange(len(ydata))
    popt, pcov = curve_fit(gaussian, xdata, ydata, p0=[100,12,5]) #initial guesses for amplitude, mean, and standard deviation
    predictions[route] = gaussian(xdata, *popt)
# --- 3. Visualization ---
#Plot average passenger density and Gaussian fit for each route
plt.figure(figsize=(15, 10))
for i, route in enumerate(average_density.index):
    plt.subplot(len(average_density.index), 1, i + 1)
    plt.plot(average_density.loc[route], label='Average Density')
    plt.plot(predictions[route], label='Gaussian Fit')
    plt.title(f'Route {route} Passenger Density')
    plt.xlabel('Time of Day')
    plt.ylabel('Passenger Density')
    plt.legend()
plt.tight_layout()
output_filename = 'passenger_density_prediction.png'
plt.savefig(output_filename)
print(f"Plot saved to {output_filename}")