import json
import random

#Let's use the same pattern as last time. 
def expression_factory(s,names):
    """ Makes an expression from its serialization """
    if s is None:
        return None
    
    #Begin the long if-else statement (figure out how to do this in a better manner?)
    expression_type = s["constraint_type"]
    if expression_type == "oto_conditional":
        return oto_expression(s["constraint_params"]["inputs"],s["constraint_params"]["outputs"]),names
    elif expression_type == "otm_conditional":
        return otm_expression(s["constraint_params"]["inputs"],s["constraint_params"]["outputs"]),names
    elif expression_type == "free_expression":
        return s["constraint_params"]
    else:
        return "DEFAULT",names
    

def oto_expression(expr_inputs,expr_outputs):
    expr = ""
    for expr_input,expr_output in zip(expr_inputs,expr_outputs):
        expr += "'"+expr_output+"' if exp_inp =="+"'"+expr_input+"' else "
    expr +="'default'"
    return expr

def otm_expression(expr_inputs,expr_outputs):
    expr = ""
    for i in range(len(expr_inputs)):
        expr += str(expr_outputs[i])+" if exp_inp =='"+str(expr_inputs[i])+"' else "
    expr +="-1"
    return expr