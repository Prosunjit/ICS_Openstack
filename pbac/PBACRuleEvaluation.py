import sys, os
import json

global conditions
global evalorder
global eval_values
evaluation_result={}

def readfile(file_name):
    with open (file_name, "r") as myfile:
        data=myfile.read()
        return data

def test(rule_index=0):
    global conditions, evalorder, eval_values
    eval_values={}
    jsondata = readJSONfile("ruleset.conf")
    #rule_index=0
    conditions = jsondata['Action']['Rules'][rule_index]['Conditions']
    evalorder = jsondata['Action']['Rules'][rule_index]['EvalOrder']
    for e in evalorder:
        (e_name, e_value) = return_key_value(e)
        eval_values[e_name] = evaluateExpression(e_value)
        #print e_name, e_value

        #print eval_values["exp_name"]
    print eval_values

def evaluateExpression(exp):
    # exp : [{u'and': [u'cond1', u'cond2']}]
    #print exp
    operator,conditions = return_key_value(exp[0])

    if (operator == "and"):
        return and_(conditions)
    elif (operator == "or"):
        return or_(conditions)


def and_(conditions):
    evaluation = True;
    for cond in conditions:
        (cond_name,cond_body,incondition) =  find_cond_body(cond)
        if incondition:
           evaluation =  evaluation and  process_cond(cond_name,cond_body)
        else:
            evaluation = evaluation and  process_eval(cond_name,cond_body)
    return evaluation

def or_(conditions):
    evaluation = False;
    for cond in conditions:
        (cond_name,cond_body,incondition) =  find_cond_body(cond)
        if incondition:
           evaluation =  evaluation or  process_cond(cond_name,cond_body)
        else:
            evaluation = evaluation or  process_eval(cond_name,cond_body)
    return evaluation

def find_cond_body(condname):
    global conditions
    global evalorder
    working_condition = None
    incondition=True
    #print "find cond body", condname, working_condition
    #search in conditions first
    for condition in conditions:
        (cond_name, cond_body) = return_key_value(condition)
        if (cond_name == condname):
            working_condition = cond_body
    #search in the EvalOrder list
    if working_condition == None:
        for condition in evalorder:
            (cond_name, cond_body) = return_key_value(condition)
            if (cond_name == condname):
                incondition=False
                # we have to evaluate cond_body
                #working_condition = cond_body
    #print "find cond body", condname, working_condition,incondition
    return (condname, working_condition,incondition)



def list2Dict(list):
    dictionary = {}
    for item in list:
       dictionary = dict(dictionary.items()+item.items())
    return dictionary

def process_cond(cond_name,working_condition):
    # working_condition = [{u'provquery': [u'subject/object/action', u'depname']}, {u'cardinality': u''}, {u'integerequal': u'3'}]

    cond_func = {}
    cond_func_result={}

    # converting list into dictionary
    cond_func = list2Dict(working_condition)

    fun_arg = None

    for fun_name,fun_arg in cond_func.items():
        if (fun_name == "provquery"):
            cond_func_result[fun_name] = prov_query(fun_arg)
        elif (fun_name == "cardinality"):
            cond_func_result[fun_name] = check_cardinality(fun_arg)

    return evaluate_cond(cond_name,cond_func_result)



def evaluate_cond (cond_name, cond_function_values):
    global evaluation_result
    if cond_function_values.has_key("provquery") and cond_function_values.has_key("cardinality"):
        evaluation_result[cond_name]=assert_equal (len(cond_function_values["provquery"]),int(cond_function_values["cardinality"]))
        return evaluation_result[cond_name]
    else:
        return False
'''
input is an expression with precomputed evaluation ex( eval1 and eval2)
'''
def process_eval(cond_name,working_condition):
    # we ignore the working_condition cause we know this eval has already been evaluated. just search it.
    global eval_values
    return eval_values[cond_name]


def assert_equal(a,b):
    return a==b
def prov_query(arg):

    return ["a","b","c"]
def check_cardinality(arg):
    return arg

def cardinality(list):
    return list.length;

def return_key_value(dictionary):
    for key, value in dictionary.items():
        pass
    return (key, value)



def readJSONfile(file_name):
    data = readfile(file_name)
    json_data = json.loads(data)
    return json_data

test()
#print assert_equal(3,4)
