This is the module for the Numerical Methods such as approximations, equation solving, solving sets of linear equations, interpolations, numerical integration, numerical differentiation, and ODE solving.

Corrections:

Replace pynm by py_num_methods

# Approximations:

Euler's Method

import pynm.approximations as pynma
x, y = pynma.euler_method(f, x0, y0, h, n)
        
    Parameters:
        - f: The derivative function of the ODE.
        - x0: The initial x value.
        - y0: The initial y value.
        - h: The step size.
        - n: The number of iterations.
        
    Returns:
        - x: The array of x values.
        - y: The array of y values.

# Equation Solving:

import pynm.eqn_solver as pynm_es

Graphical Solver:

    pynm_es.solve_equation_graphically(equation, x_range, y_range)
    
    Parameters:
	- equation: function
	- x_range: Tuple
	- y_range: Tuple

    Returns:
	- None
	- Plots the graph

Bisection Method:
    ret = pynm_es.bisection_method(f, a, b, tol)
        
    Parameters:
        - f: The function for which we want to find the root.
        - a: The lower bound of the interval.
        - b: The upper bound of the interval.
        - tol: The tolerance level for the root.
        
    Returns:
        - The approximate root of the function within the specified tolerance level.

False Position Method:
   ret = pynm_es.false_position_method(f, a, b, tol, max_iter)

   Parameters:
    	- f: The function for which we want to find the root.
    	- a and b: The initial interval endpoints.
        - tol: The tolerance level for convergence.
        - max_iter: The maximum number of iterations allowed.
    Returns:
        - The approximate root of the function.

Fixed Point Iterations:
   ret = pynm_es.fixed_point_iteration(f, initial_guess, tolerance, max_iterations)

   Parameters:
    	- f: The function for which we want to find the root.
    	- initial_guess: The initial guess value.
        - tolerance: The tolerance level for convergence.
        - max_iterations: The maximum number of iterations allowed.

    Returns:
        - The approximate root of the function.

# Simultaneous Linear Equation Solver:

import pynm.sim_lin_eqn_solve as pynmsles

Gaussian Elimination:
    x = pynmsles.gaussian_elimination(A, b)

   Parameters:
    	- A: The A (coefficient) matrix in Ax=b
    	- b: The b (constant) matrix in Ax=b

    Returns:
        - x: Solution

LU Decomposition:
    x = pynmsles.lu_decomposition(A, b)

   Parameters:
    	- A: The A (coefficient) matrix in Ax=b
    	- b: The b (constant) matrix in Ax=b

    Returns:
        - x: Solution

Tri Diagonal Matrix Algorithm:
    x = pynmsles.solve_tdma(A, b)

   Parameters:
    	- A: The A (coefficient) matrix in Ax=b
    	- b: The b (constant) matrix in Ax=b

    Returns:
        - x: Solution

Gauss Seidel:
    x = pynmsles.gauss_seidel(A, b, x0, max_iterations=100, tolerance=1e-6)

   Parameters:
    	- A: The A (coefficient) matrix in Ax=b
    	- b: The b (constant) matrix in Ax=b
	- x0: Initial guess array
	- max_iterations: Max number of iterations
	- tolerance: Permissible tolerance in relative error

    Returns:
        - x: Solution

# Interpolations:

import pynm.interpolations as pynmi

Quadratic Interpolations:

    y = pynmi.quadratic_interpolation(x, x0, x1, x2, y0, y1, y2)
    
    Parameters:
        - x : The point at which to estimate the value.
        - x0, x1, x2 : The x-coordinates of the three data points.
        - y0, y1, y2 : The y-coordinates of the three data points.

    Returns:
	- y = estimated value at point x.

Lagrange Interpolations:

    x = pynmi.lagrange_interpolation(x, y, xi)
    
    Parameters:
        - x, y : Arrays of data points
	- xi : Value at which we want to approximate the function

    Returns:
	- yi = interpolated value at point xi

# Numerical Integration:

import pynm.numerical_integration as pynmni

Trapezoidal Integration:

    val = pynmni.trapezoidal_integration(f, a, b, n)

    Parameters:
        - f: The function to be integrated.
        - a: The lower limit of integration.
        - b: The upper limit of integration.
        - n: The number of subintervals to divide the integration interval into.
        
    Returns:
        - val = The approximate value of the integral.

Simpsons 1/3 method:

    val = pynmni.simpsons_13(f, a, b, n)

    Parameters:
        - f: The function to be integrated.
        - a: The lower limit of integration.
        - b: The upper limit of integration.
        - n: The number of subintervals.
        
    Returns:
        - val = The approximate value of the definite integral.

Simpsons 3/8 method:

    val = pynmni.simpsons_38(f, a, b, n)

    Parameters:
        - f: The function to be integrated.
        - a: The lower limit of integration.
        - b: The upper limit of integration.
        - n: The number of subintervals.
        
    Returns:
        - val = The approximate value of the definite integral.

# Numerical Differentiation

import pynm.numerical_differentiation as pynmnd

    val = pynmnd.numerical_differentiation(f, x, h, method)
	
    Parameters:
	- f: Function
	- x: x values for finding slope at
	- h: The value of interval size
	- method: "central", "backward" and "forward" based on type of differentiation

    Returns:
	val = The approximate value of differentiated function at x

# ODE Solver

import pynm.ODE_solver as pynmode

Predictor Corrector Method:

    t, y = pynmode.predictor_corrector(f, y0, t0, tn, h)

    Parameters:
        - f: The function defining the ODE dy/dt = f(t, y).
        - y0: The initial condition y(t0) = y0.
        - t0: The initial time.
        - tn: The final time.
        - h: The time step size.

    Returns:
        - t: An array of time values.
        - y: An array of corresponding solution values.

Second Order Runge Kutta:

    t, y = pynmode.runge_kutta_2(f, t0, y0, h, n)

        Parameters:
        - f: The function defining the ODE dy/dt = f(t, y).
        - t0: The initial value of the independent variable.
        - y0: The initial value of the dependent variable.
        - h: The step size.
        - n: The number of steps.

        Returns:
        - t: The array of time values.
        - y: The array of solution values.


Fourth Order Runge Kutta:

    t, y = pynmode.runge_kutta_4(f, t0, y0, h, n)

        Parameters:
        - f: The function defining the ODE dy/dt = f(t, y).
        - t0: The initial value of the independent variable.
        - y0: The initial value of the dependent variable.
        - h: The step size.
        - n: The number of steps.

        Returns:
        - t: The array of time values.
        - y: The array of solution values.

           
