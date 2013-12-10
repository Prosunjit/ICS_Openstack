from  dl import dependency_list as conf_dependency_list

'''
arg dl: configuration file content, return "def" of each dependency name
'''
def readDNDefinition(dl):
  defition={}
  for dn in dl :
     defition[dn] = dl[dn]["def"]
  return defition

'''
arg dl: configuration file content, return "e_def" of each dependency name
'''

def readDnElaDefinition(dl):
  defition={}
  for dn in dl :
     defition[dn] = dl[dn]["e_def"]
  return defition

'''
given a list of lists of lists. return flat list
input: [[1],[2,[3,4],5],6] output [1,2,3,4,5,6]
'''
def flatten(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

'''
we have to elaborate dependency list with respect to every dn to ensure that every dn is elaborated
input:{'11': ['111', '112'], '13': ['13'], '12': ['121', '22', '124'] }
output: elaborate each dn
'''
def elaborate_all(d_list):

    for dn in d_list :
        elaborate(d_list,dn)

'''
arg d_list is call by reference type
d_list :{'11': ['111', '112'], '111': ['111']}
dn:111
output: {'11': ['111', '112'], '111': ['111']}
'''
def elaborate(d_list, dn):
    if (d_list[dn].__len__()) == 1:
        return dn
    else:
        elaborated_dn=[]
        rhs=d_list[dn]
        for d in rhs:
            elaborated_dn.append(elaborate(d_list,d))
        d_list[dn] = flatten(elaborated_dn)
        return d_list[dn]

'''
elaborate_dependency_list function modifies the first arg dl with elaborated form.
input:
output:
'''
def json_elaborate_dependency_list(dl,elaborated_def):
    for d in elaborated_def:
        dl[d]["e_def"] = elaborated_def[d]
        #print d, dl[d]["e_def"], elaborated_def[d]
    return dl

'''
return true if listB starts with listA
A=['a','b'], B = ['a'], list(A,B) return true
'''
def sub_list(listA,listB):

    for i in range(0,listB.__len__()):
        if listB[i] != listA[i] :

            return False

    return True

'''
input pattern:
elaborated_dn_def_list:{'11': ['111', '112'], '13': ['13'], '12': ['121', '122', '123', '124'], '21': ['112', '121']}
elaborated_dn: ['111', '112', '121', '122', '123', '124', '13']

output:
'''
def calculate_evalorder(elaborated_dn_def_list, elaborated_dn):
    dn_match={}
    for i in range(0,elaborated_dn.__len__()):
        match ={}
        for dn in elaborated_dn_def_list:
            rhs_dn = elaborated_dn_def_list[dn]
            if sub_list(elaborated_dn[i:],rhs_dn) == True:
                match[dn] = rhs_dn.__len__()
        # sort the dict named match here based on the value of the dict element.
        dn_match[elaborated_dn[i]] =  match
    return dn_match
    pass

def expand():
    dn_defition_list= readDNDefinition(conf_dependency_list)

    elaborate_all(dn_defition_list) # every definition in the dn_defition_list is elaborated now on. show have to be run with every individual dn
    elaborated_def = dn_defition_list # tmp
    json_elaborate_dependency_list(conf_dependency_list,elaborated_def)
    e_d = readDnElaDefinition(conf_dependency_list)
    #print e_d
    print calculate_evalorder(e_d,e_d["1"])

def test():
    print sub_list(["1","2","3"],["1","2"])
#test()
expand()
