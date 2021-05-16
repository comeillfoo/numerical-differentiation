from math import exp, sin, cos
import matplotlib as mat
import matplotlib.pyplot as plt
import numpy as np
from shell import *
from differentiation import euler, adams


def draw_array( X, Y, fmt, lbl ):
  plt.plot( X, [ y for y in Y.values() ], fmt, label=lbl )


def draw_inter( a, b, Xi, Yi, F_n ):
  X = np.arange( a - 2, b + 2, 1e-3 )
  y = []
  for x in X:
    try:
      y.append( F_n( Xi, Yi, x ) )
    except ValueError:
      y.append( 0 )
  plt.plot( X, y, 'b-', label='y = F_n( x )' )


polinom =  { 'math': "y' = y + ( 1 + x )y^2", 'function': lambda x, y: y + ( 1 + x ) * y * y, 'constant': lambda x, y: -exp(x) * ( 1/y + x ),                          'exact': lambda x, c: -exp( x ) / ( c + x * exp( x ) )       }
trigonom = { 'math': "y' = sin x + y",        'function': lambda x, y: sin(x) + y,            'constant': lambda x, y: ( y + ( sin( x ) + cos( x ) ) / 2 ) / exp( x ), 'exact': lambda x, c: c * exp( x ) - sin(x) / 2 - cos(x) / 2 }

# equations kit
equations = [ polinom, trigonom ]


# define the number of steps needed to do to get from left to right using step - hstep
def steps( left, right, hstep ):
  return ( right - left ) / hstep + 1


# generator of exact equation solution - y(x)
def get_exact_solution( constant, exact_solution ):
  def exact_y( x ):
    return exact_solution( x, constant )
  return exact_y


# common solve method
def solve( left, right, hstep, function, precise, y0, resolver ):
  n = steps( left, right, hstep )
  return resolver( left, y0, hstep, n, function, precise )


def main():
  try:
    # get the equation for differentiation
    equation_id = std_read_item_from_items( 'Выберите ОДУ:', list( map( lambda equation: equation[ 'math' ], equations ) ) )
    print(  )

    # get the f(x, y) in y' = f(x, y)
    function = equations[ equation_id ][ 'function' ]
    

    # get the derivation borders
    left, right = std_read_pair( '[ + ]: Введите интервал дифференцирования [ a, b ]: ' )
    print(  )
    # validate borders
    if right < left:
      left, right = ( right, left )
      print( 'Устранено неправильное указание границ' )

    # get start conditions
    x0 = left
    y0 = std_read_single( f'[ + ]: Введите начальные условия ( {x0}, y0 ): ' )
    print(  )

    # calculate the function of the exact solution
    constant = equations[ equation_id ][ 'constant' ]( x0, y0 )
    exact_function = equations[ equation_id ][ 'exact' ]
    precise = get_exact_solution( constant, exact_function )

    # get the step of differentiation
    hstep = std_read_positive( '[ + ]: Введите шаг дифференцирования ( h ): ', 'Шаг дифференцирования не может быть неположительным числом. Попробуйте снова...\n' )
    print(  )

    # eps = std_read_positive( '[ + ]: Введите точность дифференцирования: ', 'Погрешность не может быть неположительным числом. Попробуйте снова...\n' )
    # print(  )

    # detect the solution method
    methods = [ 'Методом Эйлера', 'Методом Адамса' ]
    method_id = std_read_item_from_items( 'Выберите метод дифференцирования:', methods )
    print(  )

    method = None
    if method_id == 0:
      method = euler
    elif method_id == 1:
      method = adams
    else:
      print( 'Завершение работы...' )
      eixt()

    # resolve according to method
    X1h, Y1h = solve( left, right, hstep, function, precise, y0, method )
    y1h = Y1h[ X1h[ 2 ] ]
    print()

    # define the error of calculations
    eps = max( [ abs( Y1h[ x ] - precise( x ) ) for x in X1h ] )
    print( f'Погрешность: [ eps = {eps} ]\n' )

    # resolve using hstep * 2
    X2h, Y2h = solve( left, right, 2 * hstep, function, precise, y0, method )
    y2h = Y2h[ X2h[ 2 ] ]
    print()

    # define the accuracy by Runge
    R = y1h - y2h
    print( f'Оценка точности по правилу Рунге: R = {R}' )

    # draw the results
    draw_array( X1h, Y1h, 'bo-', 'y ~ phi( x )' )

    precise_X = X1h
    precise_Y = { x: precise( x ) for x in precise_X }

    draw_array( precise_X, precise_Y, 'r-', 'y = phi( x )' )
    plt.grid( True, 'both', 'both' )
    plt.ylabel( 'y', horizontalalignment='right', y=1.05, rotation=0 )
    plt.xlabel( 'x', horizontalalignment='right', x=1.05 )
    plt.legend()
    plt.show()

  except KeyboardInterrupt:
    print( '\nЗавершение программы' )
  except EOFError:
    print( '\nЗавершение программы...' )

if __name__ == '__main__':
  main()