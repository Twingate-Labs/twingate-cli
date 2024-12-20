import re

def does_addr_match_res_definition(resource_definition,addr):
    regex_definition = resource_definition.replace(".",r"\.").replace("*",".*").replace("?",".?")
    x = re.search(regex_definition, addr)
    if x:
        #print(x[0])
        return True#,x[0]
    else:
        return False#,""
    
# returns the number of TLDs present after the last meta character (* or ?)
def get_number_of_tlds_after_last_meta_char(res_definition):
    meta_chars = ['?','*']
    pos_list = []
    for char in meta_chars:
        pos = res_definition.rfind(char)
        pos_list.append(pos)
    
    last_meta_char_pos = max(pos_list)
    #if last_meta_char_pos > -1:
    post_meta_char_resource = res_definition[last_meta_char_pos+1:]
    tlds = post_meta_char_resource.split('.')
        
    return len(tlds)

# returns the number of characters before the first meta character (* or ?)
def get_number_of_chars_before_first_meta_char(res_definition):    
    meta_chars = ['?','*']
    pos_list = []
    for char in meta_chars:
            pos = res_definition.rfind(char)
            pos_list.append(pos)

    first_meta_char_pos = min(i for i in pos_list if i > -1)
    return first_meta_char_pos
    
# returns an ordered list of resources against two variables
# variable 1: number of TLDs after last meta character (in descending order)
# variable 2: number of characters before first meta character (in descending order)
# the returned list is from "narrowest" resource definition to "broadest"
def resource_definition_matcher(res_definition_list):
    order_list_of_resource_definitions = []
    scores = {}
    for res in res_definition_list:
        nb_of_tlds = get_number_of_tlds_after_last_meta_char(res)
        nb_of_chars = get_number_of_chars_before_first_meta_char(res)
        score = {"nb_of_tlds":nb_of_tlds,"nb_of_chars":nb_of_chars}
        scores[res] = score
        
    sorted_keys = sorted(scores, key=lambda x: (scores[x]['nb_of_tlds'],scores[x]['nb_of_chars']), reverse=True)
    ordered_scores = {}
    #print(sorted_keys)
    for k in sorted_keys:
        ordered_scores[k]=scores[k]
        
    return ordered_scores

def resource_definition_matcher2(df):
    order_list_of_resource_definitions = []
    scores = {}
    #df = df.reset_index()  # make sure indexes pair with number of rows
    for index, row in df.iterrows():
        res = row['address.value']
        resid = row['id']
        nb_of_tlds = get_number_of_tlds_after_last_meta_char(res)
        nb_of_chars = get_number_of_chars_before_first_meta_char(res)
        score = {"nb_of_tlds":nb_of_tlds,"nb_of_chars":nb_of_chars}
        scores[resid] = score
        
    sorted_keys = sorted(scores, key=lambda x: (scores[x]['nb_of_tlds'],scores[x]['nb_of_chars']), reverse=True)
    ordered_scores = {}
    #print(sorted_keys)
    for k in sorted_keys:
        ordered_scores[k]=scores[k]
    #print(sorted_keys)

    # in case there are duplicate resources in the DF
    df = df.drop_duplicates('id')

    df = df.set_index('id')

    df = df.reindex(sorted_keys)

    #df = df.loc[sorted_keys]
    return df

# returns the number and list of ambiguous resources from a list of resource definition
# ambiguous resources are ambiguous if and only if they have the same 2 scores (number of TLDs after last meta char
# and number of chars before first meta chars)
def detect_res_definition_ambiguity(scores):   
    seen = []
    seen_res = []
    uniq = []
    nb_of_ambiguities = 0
    ambiguity_list = []
    for key in scores:
        if scores[key] not in seen:
            seen.append(scores[key])
            seen_res.append(key)
        else:
            idx = seen.index(scores[key])
            nb_of_ambiguities = nb_of_ambiguities+1
            ambiguity_list.append(str(key)+"|"+str(seen_res[idx]))
            #print("ambiguity detected for:"+str(key) + " and: "+str(seen_res[idx]))
    
    return nb_of_ambiguities,ambiguity_list

