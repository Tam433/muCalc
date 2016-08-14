#####################################################################
#  WARNING: Don't foolishly fiddle with this file                   #
#####################################################################
pi = PI = 3.141592653589793 # constant pi
e = E = 2.718281828459045 # constant e
#--------------------------------------------- Physical Constants (SI units)
Na = 6.022e23 # Avogadro's constant
c = 3e8  # Approx. speed of light
h = 6.626068e-34 # Planck's constant
G = 6.67428e-11  # Universal gravitational constant
epsi0 = 8.85418e-12 # permittivity of free space
a0 = 5.3e-11 # Bohr radius
R = 8.314472 # Gas constant
#------------------------------------------------------------------
#----------------------------Standard Function defs----------------
#------------------------------------------------------------------
#--------------------------------------------------------------------------
def fact(n):     # Factorial Function.. 'fact'... cute huh ;-) ?
   memo = {}
   if n == 0: 
       return 1
   elif n < 0 or not type(n) is int:
   	    raise ValueError("factroial ain't defined for -ve or non-integers")
   elif n in memo:
   	  return memo[n]
   else:
        res =  n * fact(n-1)
        memo[n] = res
        return res
#-------------------------------------------------------------------
def fib(n): # Fibonacci sequence function
        known = {0:0,1:1}
	if n in known:
		return known[n]
	res = fib(n - 1) + fib(n - 2)
	known[n] = res
	return res 
#-------------------------------------------------------------------
def sgn(n):      # Signum Function
    if n == 0:  
       return 0
    elif n > 0:
       return 1
    elif n < 0:
       return -1 
#-------------------------------------------------------------------       
def floor(n):      # Floor Function
   if n < 0:
      if type(n) is int:
           return n
      else:
          return (int(n)-1)
   if n > 0:
      return int(n)
#--------------------------------------------------------------------
def ceil(n):   # Ceiling Function
    if n < 0 : 
      return int(n)
    else:
      if type(n) is int:
           return (n)
      else:
          return (int(n)+1)
    
def fpart(n):  # Fractional part
    return float(n-floor(n))
#--------------------------------------------------------------------
def rad(n):   # Degree to Radians
   return  (PI/180)*n
#--------------------------------------------------------------------
def deg(n):  # Radians to Degree
   return (180/PI)*n
import math
#--------------------------------------------------------------------
sin = math.sin  # Circular and inverse circular functions
cos = math.cos
tan = math.tan
asin = math.asin
acos = math.acos
atan = math.atan
#--------------------------------------------------------------------
sinh = math.sinh # Hyperbolic and inverse hyperbolic funcs
cosh = math.cosh
tanh = math.tanh
acosh = math.acosh
atanh = math.atanh
asinh = math.asinh
#--------------------------------------------------------------------
ln = math.log  # Logarithimic funcs
log10 = math.log10
#--------------------------------------------------------------------
sqrt = math.sqrt
abs = abs
def f(x):  return "Greetings to the usr from (N.W.A (Nerds With Attitude) : Alwayz into Somethin!') "
