def std_print_items( items ):
  for idx, data in enumerate( items, start=1 ):
    print( f'[ {idx} ]: {data}' )
  print( '[ X ]: Выйти' )

def std_read_item_from_items( header, items ):
  item = None
  while True:
    print( header )
    std_print_items( items )
    try:
      item = int( input( '> ' ) )
      if ( item < 1 or item > len( items ) ):
        print( 'Осуществляем выход...' )
        exit()
      else:
        return item - 1
    except ( ValueError ):
      print( "Неверный формат данных. Попробуйте еще раз..." )

def std_read_pair( header ):
  xy = None
  while True:
    xy = input( header )
    try:
      x, y = xy.split( ' ', 2 )
      return ( float( x ), float( y ) )
    except ( ValueError ):
      print( "Неверный формат данных. Попробуйте еще раз..." )
    except ( IndexError ):
      print( "Неверный формат данных. Попробуйте еще раз..." )

def std_read_single( header ):
  single = None
  while True:
    single = input( header )
    try:
      return float( single )
    except ( ValueError ):
      print( "Неверный формат данных. Попробуйте еще раз..." )

def std_read_positive( header, error ):
  positive = None
  while True:
    positive = std_read_single( header )
    if positive > 0:
      return positive
    else:
      print( error )