import struct

def pack_array(data):

    string = data[0].encode()

    # Create the format string for struct packing
    format_string = f"{len(string)}s{len(data) - 1}B"

    # Pack the data using struct.pack
    packed_data = struct.pack(format_string, string, *data[1:])

    return packed_data

data = ["CAN", 0x20, 0xAA]
packed_data = pack_array(data)

print(packed_data)

a,b,c = struct.unpack('3s2B', packed_data)
print(a.decode())
print(b)
print(c)
