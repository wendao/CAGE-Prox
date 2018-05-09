import sys

map_pos = {}
lines = open( sys.argv[1], 'r' ).readlines()
for line in lines:
  elems = line.split()
  pos = int(elems[0])
  mut = elems[1]
  map_pos[pos] = mut

lines = open( sys.argv[2], 'r' ).readlines()
elems = lines[0].split()
for elem in elems:
  print elem, map_pos[int(elem)]
