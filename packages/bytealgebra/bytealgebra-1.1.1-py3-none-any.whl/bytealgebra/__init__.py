import math

# Linear Function
'''
This function represents a linear equation in the form y = mx + b, 
where m is the slope and b is the y-intercept. Given the values of x, m, and b, 
the function calculates and returns the corresponding y value.
'''
def linear_function(x, m, b):
    return m * x + b


# Quadratic Function
'''
This function represents a quadratic equation in the form y = ax^2 + bx + c. 
Given the values of x, a, b, and c, the function calculates and returns 
the corresponding y value.
'''
def quadratic_function(x, a, b, c):
    return a * x**2 + b * x + c


# Absolute Value Function
'''
This function calculates the absolute value of a number x. 
The absolute value of a number is its distance from zero on the number line, 
always resulting in a non-negative value.
'''
def absolute_value_function(x):
    return abs(x)


# Square Root Function
'''
This function uses the sqrt function from the math module to calculate 
the square root of a given number x. The result is the positive square root of x.
'''
def square_root_function(x):
    return math.sqrt(x)


# Exponential Function
'''
This function calculates the result of an exponential expression where x is 
the exponent and base is the base of the exponentiation. 
It uses the exp function to raise base to the power of x.
'''
def exponential_function(x, base):
    return math.exp(x * math.log(base))
