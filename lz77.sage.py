def compress(byte_len):
    search_buffer = 4 # define the search buffer
    lookahead_buffer = 8 # define the look-ahead buffer

    output = []
    
    i = 0

    while i<byte_len:
        match_len = 0
        match_offset = 0
        match_char = None



