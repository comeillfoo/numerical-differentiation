def float_format( number ):
  return "{: > .4e}".format( number )

def logiter( func ):
  def wrapper( *args, **kwargs ):
    i = "{: > d}".format( round( args[ 0 ], 0 ) )
    xi = args[ 1 ]
    yi = args[ 2 ]
    hstep = args[ 3 ]
    function = args[ 4 ]
    precise = args[ 5 ]
    print( f' {i}\t{ float_format( xi ) } { float_format( yi ) } { float_format( function( xi, yi ) ) } { float_format( precise( xi ) ) }' )
    return func( *args, **kwargs )
  return wrapper

@logiter
def euler_next( i, xi, yi, hstep, function, precise ):
  return yi + hstep * function( xi, yi )

def logtable( func ):
  def wrapper( *args, **kwargs ):
    print( '  i\t x_i         y_i         f_i         точное решение' )
    return func( *args, **kwargs )
  return wrapper

@logtable
def euler( x0, y0, hstep, steps, function, precise ):
  X = []
  Y = {}
  idx = 0
  while ( idx < steps ):
    # fill the containers
    X.append( x0 )
    Y[ x0 ] = y0

    # get next values
    y0 = euler_next( idx, x0, y0, hstep, function, precise )
    x0 += hstep

    # next iteration
    idx += 1
  return ( X, Y )

def finite_difference_k_i( k, i, X, Y, function ):
  if k == 0:
    return function( X[ i ], Y[ X[ i ] ] )
  else:
    return finite_difference_k_i( k - 1, i, X, Y, function ) - finite_difference_k_i( k - 1, i - 1, X, Y, function )

def adams( x0, y0, hstep, steps, function, precise ):
  X, Y = euler( x0, y0, hstep, 4, function, precise )
  xi = X[ 3 ]
  yi = Y[ xi ]
  i = 4
  while i < steps:
    delta0_f_i = finite_difference_k_i( 0, i - 1, X, Y, function )
    delta1_f_i = finite_difference_k_i( 1, i - 1, X, Y, function )
    delta2_f_i = finite_difference_k_i( 2, i - 1, X, Y, function )
    delta3_f_i = finite_difference_k_i( 3, i - 1, X, Y, function )
    yi = yi + delta0_f_i * hstep + delta1_f_i * hstep**2 / 2 + delta2_f_i * 5 * hstep**3 / 12 + delta3_f_i * 3 * hstep**4 / 8
    xi += hstep
    print( f'  {i}\t{ float_format( xi ) } { float_format( yi ) } { float_format( function( xi, yi ) ) } { float_format( precise( xi ) ) }' )
    X.append( xi )
    Y[ xi ] = yi
    i += 1
  return ( X, Y )
