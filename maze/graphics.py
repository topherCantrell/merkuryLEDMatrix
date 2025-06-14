MAZE = """
11.11.222.333.44
1.1.1.2.2...3.4.
1.1.1.222..3..44
1...1.2.2.3...4.
1...1.2.2.333.44
"""

TILT = """
111.222.3...444.
.1...2..3....4..
.1...2..3....4..
.1..222.333..4..
"""

HYPHEN_A="""
...333...
...3.3...
11.333.22
...3.3...
...3.3...
"""

DIGITS = """
111
1.1
1.1
1.1
111

..1
..1
..1
..1
..1

111
..1
111
1..
111

111
..1
111
..1
111

1.1
1.1
111
..1
..1

111
1..
111
..1
111

111
1..
111
1.1
111

111
..1
..1
..1
..1

111
1.1
111
1.1
111

111
1.1
111
..1
111
"""

def show_data(ascii,title):
    data = ascii.replace('\n', '').replace(' ', '').replace('.', '0')
    bdata = bytearray()
    for i in range(0, len(data)):
        bdata.append(int(data[i],16))
    print(f'{title}={bytes(bdata)}')

show_data(TILT, "TILT")
show_data(MAZE, "MAZE")
show_data(HYPHEN_A, "HYPHEN_A")
show_data(DIGITS, "DIGITS")


# TILT=b'\x01\x01\x01\x00\x02\x02\x02\x00\x03\x00\x00\x00\x04\x04\x04\x00\x00\x01\x00\x00\x00\x02\x00\x00\x03\x00\x00\x00\x00\x04\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x03\x00\x00\x00\x00\x04\x00\x00\x00\x01\x00\x00\x02\x02\x02\x00\x03\x03\x03\x00\x00\x04\x00\x00'
# MAZE=b'\x01\x01\x00\x01\x01\x00\x02\x02\x02\x00\x03\x03\x03\x00\x04\x04\x01\x00\x01\x00\x01\x00\x02\x00\x02\x00\x00\x00\x03\x00\x04\x00\x01\x00\x01\x00\x01\x00\x02\x02\x02\x00\x00\x03\x00\x00\x04\x04\x01\x00\x00\x00\x01\x00\x02\x00\x02\x00\x03\x00\x00\x00\x04\x00\x01\x00\x00\x00\x01\x00\x02\x00\x02\x00\x03\x03\x03\x00\x04\x04'
# HYPHEN_A=b'\x00\x00\x00\x03\x03\x03\x00\x00\x00\x00\x00\x00\x03\x00\x03\x00\x00\x00\x01\x01\x00\x03\x03\x03\x00\x02\x02\x00\x00\x00\x03\x00\x03\x00\x00\x00\x00\x00\x00\x03\x00\x03\x00\x00\x00'