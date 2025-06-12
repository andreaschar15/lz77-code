import sys
import json
def compress(image_bytestream, byte_len):
    search_buffer = 4096 # define the search buffer
    lookahead_buffer = 64 # define the look-ahead buffer

    compressed = []

    position = 0

    while position<byte_len:
        match_len = 0
        match_offset = 0

        window_start = max(0, position - search_buffer)


        for length in range(4, min(lookahead_buffer, byte_len -position) + 1):

            pattern = image_bytestream[position:position +length]
            window = image_bytestream[window_start:position]
            window_pos = window.rfind(pattern)

            if window_pos != -1 and length > match_len:
                match_len = length
                match_offset = len(window) - window_pos

        if match_len >=4 and position + match_len < byte_len:
            next_byte = image_bytestream[position + match_len]
            compressed.append((1, match_offset, match_len, next_byte))  # Match: flag=1
            position += match_len
        else:
            compressed.append((0, 0, 0, image_bytestream[position]))
            position += 1



    print(compressed)
    literal_count = sum(1 for flag, _, _, _ in compressed if flag == 0)
    match_count = sum(1 for flag, _, _, _ in compressed if flag == 1)
    print(f"Literals: {literal_count}, Matches: {match_count}")
    # Calculate and print sizes
    original_size = byte_len / 1024
    # Estimate JSON size
    json_output = json.dumps(compressed)
    compressed_size = len(json_output) / 1024
    print(f"Original image size: {original_size:.2f} KB")
    print(f"Compressed JSON size: {compressed_size:.2f} KB")

    return "done. check terminal"




    '''# Calculate and print sizes
    original_size = byte_len / 1024  # Convert bytes to KB
    # Estimate binary compressed size
    compressed_binary_size = 0
    for offset, length, next_byte in compressed:
        if length >= 3:
            # Match: 1 byte for offset (search_buffer <= 4), 1 byte for length (lookahead_buffer <= 8), 1 byte for next_byte
            compressed_binary_size += 3
        else:
            # Literal: 1 byte for the byte itself
            compressed_binary_size += 1
        # Add 1 bit for flag (literal vs match), rounded up to bytes per group of 8
    compressed_binary_size += (len(compressed) + 7) // 8  # Ceiling division for flag bits
    compressed_size = compressed_binary_size / 1024  # Convert to KB
    print(f"Original image size: {original_size:.2f} KB")
    print(f"Compressed image size: {compressed_size:.2f} KB")'''


## this is supposed to grab from a file directly and convert it here to a bytestream.
'''if __name__ == '__main__':
    # Expect two arguments: image_path (string) and byte_len (integer)
    if len(sys.argv) > 2:
        image_path = sys.argv[1]
        try:
            byte_len = int(sys.argv[2])  # Convert byte_len to integer
            # Read image file as bytes
            with open(image_path, 'rb') as f:
                image_bytestream = f.read()
            if byte_len > len(image_bytestream):
                print(json.dumps({"error": "byte_len exceeds bytestream length"}))
                sys.exit(1)
            # Run compression
            result = compress(image_bytestream, byte_len)
            # Ensure next_byte is JSON-serializable (convert to int)
            serialized_result = [(offset, length, int(next_byte)) for offset, length, next_byte in result]
            print(json.dumps(serialized_result))
        except ValueError:
            print(json.dumps({"error": "byte_len must be an integer"}))
        except FileNotFoundError:
            print(json.dumps({"error": f"Image file not found: {image_path}"}))
        except Exception as e:
            print(json.dumps({"error": f"Compression error: {str(e)}"}))
    else:
        print(json.dumps({"error": "Two arguments required: image_path and byte_len"}))'''
