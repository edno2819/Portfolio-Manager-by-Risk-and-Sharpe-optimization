import scipy.optimize as optimize

def f(params):
    a, b, c = params 
    if a<0.5:
        return 5
    return a**2 + b**2 + c**2 + (1/(a+b+c))

initial_guess = [1, 1, 1]
result = optimize.minimize(f, initial_guess)

if result.success:
    fitted_params = result.x
    print(fitted_params)
else:
    raise ValueError(result.message)

result