import json

json.with open('data.json', 'r') as f:

with open('data.json', 'r') as f:
    new_file_content = ""
    line_no = 0

    for line in f :
        line_no +=1
        dict_str = "{" + f"{line}" + "}"
        dict_val = None

        # just Trying to convert to dict,
        # most case it will not  like { alone,  }, alone
        # only "name" : "value" will be converted
        try:
            dict_val = eval(dict_str)
        except Exception:
            pass

        given_key = 'id'
        new_val = 'metafix1'

        # even after
        try:
            found_val = dict_val [f"{given_key}"]
            if found_val is not None :
                new_line = line.replace(found_val, new_val)
                print( f"At {line_no} before: [{line}] after :[{new_line}]")
                new_file_content += new_line
        except Exception:
            new_file_content += line


print( new_file_content)