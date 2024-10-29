
# dict ptr
def get_value(input_dict : dict, key : str):
    if key == 'Pose':
        return input_dict['{']['Solid']['boundingObject']['Pose']
    elif key == 'size':
        try :
            value = input_dict['{']['Solid']['boundingObject']['Pose']['Box']['size']
        except :
            value = None
        return value

def parse_proto(proto_string):
    def parse_block(lines):
        block_dict = {}
        key = None

        while True:
            try:
                line = next(lines).strip()
            except StopIteration:
                break

            if not line or line.startswith("#"):  # Ignore comments and empty lines
                continue

            if "{" in line:
                # Extract key name from the current line
                key = line.split()[0]
                sub_block = parse_block(lines)  # Recursively parse the sub-block
                block_dict[key] = sub_block

            elif "}" in line:
                break  # End of the current block

            else:

                if line.startswith("translation") or line.startswith("rotation"):
                    parts = line.split()
                    key = parts[0]
                    value = parts[1:]
                    block_dict[key] = " ".join(value)

                elif line.startswith('size'):
                    parts = line.split()
                    print(parts)
                    key = parts[0]
                    value = parts[1:] # x, z, y 건물의 정보
                    block_dict[key] = " ".join(value)
                
                # if "field" in line:
                #     # Handle fields in the PROTO definition
                #     parts = line.split()
                #     key = parts[2]
                #     value = parts[3:]
                #     block_dict[key] = " ".join(value)
                # else:
                #     # Handle array fields such as 'point', 'coordIndex', 'texCoordIndex', etc.
                #     key = line.split()[0]
                #     if key not in block_dict:
                #         block_dict[key] = []
                #     # Keep reading lines to get the entire array
                #     while True:
                #         line = next(lines).strip()
                #         if line.endswith("]"):
                #             block_dict[key].append(line[:-1].strip())
                #             break
                #         else:
                #             block_dict[key].append(line)

        return block_dict

    # Convert proto_string into an iterator of lines
    lines = iter(proto_string.strip().splitlines())
    return parse_block(lines)


# 데이터를 바이너리 파일로 저장
#with open("proto_files/Museum.proto", "r") as file:
    #proto_content = file.read()
    # print(proto_content)

#proto_dict = parse_proto(proto_content)

# print(proto_dict)

#print(get_value(proto_dict, 'Pose'))