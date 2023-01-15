
# def to_binary(input_string):
#     result = ''.join(format(ord(i), '08b') for i in input_string)
#     return result


# def binary_to_str(input_binary):
#     def BinaryToDecimal(binary):
#         int_string = int(binary, 2)
#         return int_string

#     str_data = ' '
#     for i in range(0, len(input_binary), 8):
#         temp_data = input_binary[i:i + 8]
#         decimal_data = BinaryToDecimal(temp_data)
#         str_data = str_data + chr(decimal_data)

#     return str_data