import numpy as np
import matplotlib.pyplot as plt

class approximations:
    def euler_method(f, x0, y0, h, n):
        x = [x0]
        y = [y0]
        
        for i in range(n):
            x.append(x[i] + h)
            y.append(y[i] + h * f(x[i], y[i]))
        
        return x, y

class eqn_solver:
    def solve_equation_graphically(equation, x_range, y_range):
        x = np.linspace(x_range[0], x_range[1], 1000)
        y = eval(equation)
        plt.plot(x, y)
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.grid(True, linestyle='--', linewidth=0.5)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Graphical Solution')
        plt.show()

    def bisection_method(f, a, b, tol):
        while abs(b - a) > tol:
            c = (a + b) / 2
            if f(c) == 0:
                return c
            elif f(a) * f(c) < 0:
                b = c
            else:
                a = c
        return (a + b) / 2


    def false_position_method(f, a, b, tol, max_iter):
        if f(a) * f(b) >= 0:
            raise ValueError("The function values at the endpoints must have opposite signs.")
        
        for i in range(max_iter):
            c = (a * f(b) - b * f(a)) / (f(b) - f(a))
            
            if abs(f(c)) < tol:
                return c
            
            if f(a) * f(c) < 0:
                b = c
            else:
                a = c
        
        raise ValueError("The method did not converge within the maximum number of iterations.")



    def fixed_point_iteration(f, initial_guess, tolerance, max_iterations):
        x = initial_guess
        for i in range(max_iterations):
            x_next = f(x)
            if abs(x_next - x) < tolerance:
                return x_next
            x = x_next
        return None

class sim_lin_eqn_solve:
    def gaussian_elimination(A, b):
        n = len(A)
        for i in range(n):
            # Find the pivot row
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            
            # Perform row operations to eliminate variables
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                A[j] -= factor * A[i]
                b[j] -= factor * b[i]
        
        # Back substitution to find the solution
        x = np.zeros(n)
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - np.dot(A[i][i+1:], x[i+1:])) / A[i][i]
        
        return x

    def lu_decomposition(A, B):
        n = len(A)
        L = [[0.0] * n for _ in range(n)]
        U = [[0.0] * n for _ in range(n)]
        P = [[float(i == j) for j in range(n)] for i in range(n)]
        for j in range(n):
            max_row = max(range(j, n), key=lambda i: abs(A[i][j]))
            if j != max_row:
                P[j], P[max_row] = P[max_row], P[j]
                A[j], A[max_row] = A[max_row], A[j]
            L[j][j] = 1.0
            for i in range(j + 1, n):
                L[i][j] = A[i][j] / A[j][j]
                for k in range(j + 1, n):
                    A[i][k] -= L[i][j] * A[j][k]
            for i in range(j, n):
                U[i][j] = A[i][j]
        # Solve Ly = B using forward substitution
        y = [0.0] * n
        for i in range(n):
            y[i] = B[P[i]]
            for j in range(i):
                y[i] -= L[i][j] * y[j]
        # Solve Ux = y using backward substitution
        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            x[i] = y[i]
            for j in range(i + 1, n):
                x[i] -= U[i][j] * x[j]
            x[i] /= U[i][i]
        return x


    def gauss_seidel(A, b, x0, max_iterations=100, tolerance=1e-6):
        n = len(A)
        x = x0.copy()
        for _ in range(max_iterations):
            for i in range(n):
                sum_ax = sum(A[i][j] * x[j] for j in range(n) if j != i)
                x[i] = (b[i] - sum_ax) / A[i][i]
            if all(abs(A @ x - b) < tolerance):
                return x
        return x

    def solve_tdma(A, B):
        n = len(B)
        alpha = np.zeros(n)
        beta = np.zeros(n)
        x = np.zeros(n)

        # Forward elimination
        alpha[1] = A[0][1] / A[0][0]
        beta[1] = B[0] / A[0][0]
        for i in range(1, n-1):
            alpha[i+1] = A[i][i+1] / (A[i][i] - A[i][i-1] * alpha[i])
            beta[i+1] = (B[i] - A[i][i-1] * beta[i]) / (A[i][i] - A[i][i-1] * alpha[i])

        # Back substitution
        x[n-1] = (B[n-1] - A[n-1][n-2] * beta[n-1]) / (A[n-1][n-1] - A[n-1][n-2] * alpha[n-1])
        for i in range(n-2, -1, -1):
            x[i] = beta[i+1] - alpha[i+1] * x[i+1]

        return x

class interpolations:
    def quadratic_interpolation(x, x0, x1, x2, y0, y1, y2):
        # Calculate the coefficients of the quadratic equation
        a = ((y2 - y0) / ((x2 - x0) * (x2 - x1))) - ((y1 - y0) / ((x1 - x0) * (x2 - x1)))
        b = (y1 - y0) / (x1 - x0) - a * (x1 + x0)
        c = y0 - a * x0**2 - b * x0
        
        # Evaluate the quadratic equation at point x
        y = a * x**2 + b * x + c
        
        return y

    def lagrange_interpolation(x, y, xi):
        n = len(x)
        yi = 0.0

        for i in range(n):
            L = 1.0
            for j in range(n):
                if i != j:
                    L *= (xi - x[j]) / (x[i] - x[j])
            yi += y[i] * L

        return yi

class numerical_integration:
    def trapezoidal_integration(f, a, b, n):

        h = (b - a) / n  # Calculate the width of each subinterval
        x = a  # Initialize the starting point
        integral = 0  # Initialize the integral value
        
        for i in range(n):
            integral += (f(x) + f(x + h)) * h / 2  # Calculate the area of each trapezoid
            x += h  # Move to the next subinterval
        
        return integral

    def simpsons_13(f, a, b, n):

        h = (b - a) / n
        x = [a + i * h for i in range(n+1)]
        y = [f(xi) for xi in x]
        
        integral = y[0] + y[-1]
        for i in range(1, n):
            if i % 2 == 0:
                integral += 2 * y[i]
            else:
                integral += 4 * y[i]
        
        integral *= h / 3
        return integral

    def simpsons_38(f, a, b, n):
        h = (b - a) / n
        x = a
        integral = f(a) + f(b)

        for i in range(1, n):
            x += h
            if i % 3 == 0:
                integral += 2 * f(x)
            else:
                integral += 3 * f(x)

        integral *= 3 * h / 8

        return integral

class numerical_differentiation:
    def numerical_differentiation(f, x, h, method):
        if method == 'central':
            return (f(x + h) - f(x - h)) / (2 * h)
        elif method == 'backward':
            return (f(x) - f(x - h)) / h
        elif method == 'forward':
            return (f(x + h) - f(x)) / h
        else:
            raise ValueError("Invalid differentiation method. Please choose 'central', 'backward', or 'forward'.")

class ODE_solver:
    def predictor_corrector(f, y0, t0, tn, h):
        t = [t0]
        y = [y0]

        while t[-1] < tn:
            t_next = t[-1] + h
            y_predictor = y[-1] + h * f(t[-1], y[-1])
            y_corrector = y[-1] + h * f(t_next, y_predictor)
            y.append(y_corrector)
            t.append(t_next)

        return t, y

    def runge_kutta_2(ode_func, t0, y0, h, n):
        t_values = [t0]
        y_values = [y0]

        for _ in range(n):
            t = t_values[-1]
            y = y_values[-1]

            k1 = ode_func(t, y)
            k2 = ode_func(t + h, y + h * k1)

            y_next = y + h * (k1 + k2) / 2
            t_next = t + h

            t_values.append(t_next)
            y_values.append(y_next)

        return t_values, y_values

    def runge_kutta_4(f, t0, y0, h, n):
        t = [t0]
        y = [y0]

        for i in range(n):
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + h/2, y[i] + k1/2)
            k3 = h * f(t[i] + h/2, y[i] + k2/2)
            k4 = h * f(t[i] + h, y[i] + k3)

            t.append(t[i] + h)
            y.append(y[i] + (k1 + 2*k2 + 2*k3 + k4)/6)

        return t, y
