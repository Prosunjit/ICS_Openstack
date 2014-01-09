
'''
* The left side of each entry in the config list, is a path of an entry in the given json formatted string
* if the right hand side contains "any" keyword, all values are taken as valid value;
* if contains "includes" keyword, only the values inside include are considered. If matched value from
  the json path is not included in the include list, the corresponding filed is not shown in the output;

'''


config = {
    "_context_request_id":"any",
    "event_type":"does_not_include(  scheduler.run_instance  )",
    "_unique_id":"any",
    "payload.hostname":"any",
    "payload.state_description":"any",
    "payload.instance_id":"any"
}