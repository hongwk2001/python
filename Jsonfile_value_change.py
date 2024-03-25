import json

with open('data.json', 'r') as f:
    json_obj = json.load(f)

pretty_json_str = json.dumps(json_obj, indent=2)

print("pretty_json", type(pretty_json_str), pretty_json_str  )

new_file_content = ""
line_no = 0

for line in pretty_json_str.splitlines() :
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
            # make more precise by including "key": "value" altogether.
            replace_fr = f'\"{given_key}\": \"{found_val}\"'
            replace_to = f'\"{given_key}\": \"{new_val}\"'
            new_line = line.replace(replace_fr  ,  replace_to )
            print(f"At {line_no} before: [{line}] after :[{new_line}]")
            new_file_content += new_line
    except TypeError:
            new_file_content += line
    except KeyError:
        new_file_content += line

print('new_file_content',  type(new_file_content),  new_file_content)

print('final pretty:' ,  json.dumps( json.loads(new_file_content ) , indent=2))
