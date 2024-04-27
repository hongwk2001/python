import json

with open('data.json', 'r') as f:
    json_obj = json.load(f)

pretty_json_str = json.dumps(json_obj, indent=2)

print("pretty_json", type(pretty_json_str), pretty_json_str  )

new_file_content = ""
line_no = 0
given_key = 'id'
new_val = 'metafix1'

def get_replace_from_to(src_txt, txt_fr, txt_to, new_val):
    fr1 =   txt_fr
    to1 = txt_to
    replace_fr = src_txt[src_txt.index(  txt_fr): src_txt.index(txt_to) + len(txt_to)]
    replace_to = src_txt[src_txt.index(  txt_fr): src_txt.index(txt_to)] + new_val
    return replace_fr, replace_to

for line in pretty_json_str.splitlines() :
    line_no +=1
    dict_str = "{" + f"{line}" + "}"
    dict_val = None

    # just Trying to convert to dict,
    # only "name" : "value" will be converted
    try:
        # can convert to Dict ?
        dict_val = eval(dict_str)
        try:
            # do we have key
            found_val = dict_val[f"{given_key}"]

            # make more precise by including "key": "value" altogether.
            replace_fr, replace_to  = get_replace_from_to(line, given_key, found_val, new_val )
            new_line = line.replace(replace_fr, replace_to)
            print(f"At {line_no} from: [{replace_fr}] after :[{replace_to}]")
            print(f"At {line_no} from: [{line}] after :[{new_line}]")

            new_file_content += new_line

        except KeyError:
            # not found given key
            new_file_content += line
    except SyntaxError:
        # most of lines that can not be converted to Dict will end up here
        new_file_content += line

# new content
print('new_file_content',  type(new_file_content),  new_file_content)
# make it pretty again
print('final pretty:' ,  json.dumps( json.loads(new_file_content ) , indent=2))
