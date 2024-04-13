import json

def fine_ds_ver(file_path, given_key) -> list:
    with open(file_path, 'r') as f:
        lines = f.readlines()

    vers=[]
    for line_no, line in enumerate(lines):
        if given_key in line:
            vers.append({line_no + 1:line})
#            print("ver added", vers[-1])
    return vers

def get_replace_from_to(src_txt, txt_fr, txt_to, new_val):
    replace_fr = src_txt[src_txt.index( txt_fr): src_txt.index(txt_to) + len(txt_to)]
    replace_to = src_txt[src_txt.index( txt_fr): src_txt.index(txt_to)] + new_val
    return replace_fr, replace_to

def pretty_json(file_path, YN)->str:
    if YN == 'Y':
        with open(file_path, 'r') as f:
            json_obj = json.load(f)
        pretty_json_str = json.dumps(json_obj, indent=2)
    else:
        with open(file_path, 'r') as f:
             pretty_json_str=f.readlines()

    print("pretty_json", type(pretty_json_str), pretty_json_str)
    return pretty_json_str


def align_field_position(file_path, given_key,pretty_json_yn, overwrite):
    # this changes file too much for production
    # use with caution
    pretty_json_str = pretty_json(file_path, pretty_json_yn)

    new_file_content = ""
    line_no = 0
    new_val = 'metafix1'
    counter = 0

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
                found_val = str(dict_val[f"{given_key}"])

                # make more precise by including "key": "value" altogether.
                counter+=1
                replace_fr, replace_to  = get_replace_from_to(line, given_key, found_val, new_val=str(counter) )
                new_line = line.replace(replace_fr, replace_to)
                print(f"At {line_no} from: [{replace_fr}] after :[{replace_to}]")
                print(f"At {line_no} from: [{line}] after :[{new_line}]")

                new_file_content += new_line

            except KeyError:
                # not found given key
                new_file_content += line
        except TypeError:
            # most of lines that can not be converted to Dict will end up here
            new_file_content += line
        except SyntaxError:
            # most of lines that can not be converted to Dict will end up here
            new_file_content += line

    # # new content
    # print('new_file_content',  type(new_file_content),  new_file_content)
    # # make it pretty again
    # print('final pretty:' ,  json.dumps( json.loads(new_file_content ) , indent=2))
    if overwrite == 'Y' :
        with open(file_path,'w', newline='\n') as out:
            out.write(new_file_content)
        print('over wrote on', file_path)

import os

if __name__ == "__main__":
    file_path = os.path.join('.', 'data.json')
    given_key = 'fileposition'

    # search test
    results = fine_ds_ver(file_path, given_key)
    for r in results:
        print ( r )

    # now replace test
    align_field_position(file_path, given_key, pretty_json_yn='Y', overwrite='Y')