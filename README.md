# COVID19_Cases_Estimation

Numerical fitting is an invaluable tool for data analysis and potential prediction of events by obtaining functions that can correspond to a data cloud or a given function with low error. 
In this study, we propose to predict the progression of COVID-19 cases in different countries and worldwide using an updated database from 2020.

We will work using a function from the scipy.optimize package, specifically the curve_fit function. 
This function from scipy allows for convenient non-linear least squares curve fitting. 
It requires a fitting function and a data cloud as necessary arguments, and initial parameters can be provided for the function to start fitting (which will be the future coefficients of the fitting function). 
If these initial parameters are not provided, curve_fit looks for the number of parameters using an inspection method.

In the case where the system has no constraints, curve_fit works using the Levenberg-Marquardt method. 
This method interpolates between the Newton-Gauss algorithm and the gradient descent method and is usually optimal in most cases, although it may be slow at times. 
Alternatively, it operates by the Trust Region Reflective method, which allows for working in situations where there are more constraints than variables but is slightly more cumbersome.

The function returns a tuple where the first position is a vector with n values, which are the coefficients of the optimal fitting function. 
The second position is an nxn matrix where the diagonal represents the variance of the parameter estimation, 
and the standard deviation error can be obtained using the following line of code:      np.sqrt(np.diag(pcov))

We work with a database in .xlsx format downloaded from the "Our World in Data" website. 
The import is done using the pandas library and its read_excel function, which prompts the user with an input to choose from a list of countries for which they want to perform the approximation.

No major pre-conditioning was done except for adding a column with the number of days elapsed (in the same Excel file prior to import). 
Additionally, a column with the logarithmic values of the total cases for each country was added for easier plotting.

Subsequently, three functions are defined with which we will attempt to fit our data cloud:
- A logistic function.
- An exponential function.
- A 3rd-degree polynomial function.
Note: We do not work with a higher-degree polynomial as the fitting to the data cloud is good, but the error becomes excessive outside of it.

Then, the curve_fit function is applied to fit the curves to our data cloud, which returns coefficients corresponding to that situation, 
and with those coefficients, we calculate the forecasts for 30 and 60 days. 
The same is done by running the X (days elapsed) values through the fitted functions using an extended vector for the required number of days.

The total quadratic error is calculated by summing the squares of the differences between the points obtained by each approximation and our data cloud.

In most cases, the best fit is achieved by the polynomial function, but as mentioned previously, 
it has a problem of deviating from the boundaries marked by our data points: it increases or decreases at an disproportional rate.

As in many other cases, it can be seen that while it works within the x-axis values covered by the data points given as a starting point, the approximation is good. 
However, it deviates when predicting values in a future (or past) time span.

Therefore, I decide to use another tool to make the prediction as realistically as possible, the logistic function. 
This function models such phenomena as pandemics, microbial growth, kinetic developments, etc. very accurately.
Moreover, it is the function that best fits the data points for China, and it is very close to being the best for New Zealand as well.

The function consists of an exponential growth phase that becomes asymptotic at a maximum, 
which in this case is the most logical since exponential growth cannot continue indefinitely as the world population is a finite value. 
Once I have the fitted function, I calculate the predicted values of cases for the next 30 and 60 days by adding the increment in the logistic function for that number of days to the current number of existing cases.
