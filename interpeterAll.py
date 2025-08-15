# this project is a basic interpeter
# Added:
# string, float and int operators support (for string only +)
# adding veruble support # achived getting verbs
# fix verubel not liking number in the veurbes

# progres:
# creating interpeter (setting values)
# keywords: output

# next steps:
# adding more keywords
# adding keywords functionality
# return value to keywords

# steps tutorial
# add keywords functionality: get all elements with step count of keyword + 10

# may cusse problomes lines:
# 61 - add number to verubles

# tokenizer (tokenize)

def tokenizer(input_calculator: str):
    operators = ["+","-","*","/","="]
    seperators = ["(",")",","]
    token_output = []
    add_to_output = ""
    token_type = ""
    onString = False
    stopString = ""
    for i in range(len(input_calculator)):
        character = input_calculator[i]
        
        if onString:
            if character == stopString:
                onString = False
                continue
            else:
                token_type = "STRING"
                add_to_output += character
                continue

        elif character in ["'" , '"']:
            onString = True
            if add_to_output != "":
                token_output.append((token_type,add_to_output))
            add_to_output = ""
            stopString = character
            continue
            
            
        elif character.isspace():
            continue

        elif character in operators:
            if token_type != "OPARATOR":
                if add_to_output != "":
                    token_output.append((token_type,add_to_output))
                add_to_output = ""
            token_type = "OPARATOR"

        elif character.isnumeric() or character == ".":
            if token_type == "IDENTIFIER":
                add_to_output += character
                continue
            if token_type != "NUMBER":
                if add_to_output != "":
                    token_output.append((token_type,add_to_output))
                add_to_output= ""
            token_type = "NUMBER"



        elif character in seperators:
            if add_to_output:
                token_output.append((token_type,add_to_output))
                add_to_output = ""

            if token_type == "":
                token_type = "SEPARATOR"
            token_type = "SEPARATOR"
            token_output.append((token_type,character))
            
            token_type = ""
            continue

        

        elif (character not in operators) and (character not in seperators):
            if len(add_to_output) > 0:
                if not add_to_output[0].isalnum() and add_to_output[0] not in ("" or " ") and character in seperators:
                    print(token_output, character, add_to_output)
                    print("The Identifier cant start by a operator!")
                    exit()
                
            # need to add lock if the next is text and add if the type isnt text
            
            if token_type != "IDENTIFIER":
                if add_to_output != "":
                    token_output.append((token_type, add_to_output))
                add_to_output = ""
                token_type = "IDENTIFIER"



        elif character.isalpha() and character not in operators:
            if token_type != "SYMBLE":
                if add_to_output != "":
                    token_output.append((token_type,add_to_output))
                add_to_output= ""
            token_type = "SYMBLE"

        add_to_output += character

    if add_to_output and add_to_output != "\n":
        token_output.append((token_type,add_to_output))

    return token_output


# parser (set up steps)
def parser(token_line: list):
    # correct token line
    keywords = ["output", "getConsole", "if", "elif", "else", "while"]
    for i in range(len(token_line)):
        char = token_line[i]
        if char[1] in keywords:
            token_line[i] = ("KEYWORD", char[1])


    output = []
    operators = ['+', "-", "*", "/"]
    seperators = ["(",")"]
    step1 = ['+', "-"]
    step2 = ["*", "/"]
    sepAdd = 0 # add to make the enything in seperators first

    for i in range(len(token_line)):
        charecter = token_line[i]  
        
        if charecter[1] in ["(",")"]:
            if charecter[1] == "(":
                sepAdd += 10
            if charecter[1] == ")":
                sepAdd -= 10
        
        if charecter[1] in operators:
            if charecter[1] in step1:
               output.append((1+sepAdd,charecter)) 
            elif charecter[1] in step2:
                output.append((2+sepAdd,charecter))
        else:
            output.append((0+sepAdd,charecter))    
    
    return output


# tools
def plus(num1, num2):
    return num1 + num2

def min(num1, num2):
    return num1 - num2

def mul(num1, num2):
    return num1 * num2

def div(num1, num2):
    return num1 / num2

def typeTest(value,typeGive):
    try:
        typeGive(value)
        return True
    except:
        return False
    
# finalise: do all calculations
def finalise(step_line: list, storege: dict):
    t = 0
    seperators = ["(",")",","]
    operators = ["+", "-", "*", "/"]
    Continue = True
    output = []
    t = 0
    while t < len(step_line):
        char1 = step_line[t][1]
        if char1[1] in ["(",")"]:
            step_line.pop(t)
            t -= 1
        
        if t+1 < len(step_line): 
            if char1[0] == "IDENTIFIER" and step_line[t+1][1][1] != "=":
                if char1[1] in storege:
                    step_line.insert(t, (step_line[t][0],(storege.get(char1[1])[1][0],storege.get(char1[1])[1][1])))
                    step_line.pop(t + 1)
                else:
                    print("Cant find veruble!", char1[1])
                    exit()
        elif char1[0] == "IDENTIFIER":

            if char1[1] in storege:
                step_line.insert(t, (storege.get(char1[1])[0],(storege.get(char1[1])[1][0],storege.get(char1[1])[1][1])))
                step_line.pop(t + 1)
            else:
                print("Cant find veruble!", char1[1])
                exit()
                
        # dubuge see line
        t += 1

    
    while Continue:

        # configering
        biggest = 0
        location = 0
        
        for i in range(len(step_line)):
            char = step_line[i]
            if char[1][1] in ["(",")"] or char[1][1] not in operators:
                continue
            
            elif char[0] > biggest:
                biggest = char[0]
                location = i

        if not step_line:
            break
        result = 0
        
        # Error Adding String
        if step_line[location][1][1] == "+":
            num1 = step_line[location-1][1][1]
            num2 = step_line[location+1][1][1]
            if step_line[location-1][1][0] == "NUMBER" and step_line[location+1][1][0] == "NUMBER":
                result = plus(float(num1),float(num2))
            
            elif step_line[location-1][1][0] != step_line[location+1][1][0]:
                # fisr error handeling
                print("unexpected Error while adding!")
                exit()
            else:
                result = plus(num1,num2)

            step_line[location] = (step_line[location-1][0], (step_line[location-1][1][0], str(result)))
            step_line.pop(location+1)
            step_line.pop(location-1)

        elif step_line[location][1][1] == "-":
            num1 = step_line[location-1][1][1]
            num2 = step_line[location+1][1][1]
            result = min(float(num1),float(num2))
            step_line[location] = (step_line[location-1][0], ('NUMBER', str(result)))
            step_line.pop(location+1)
            step_line.pop(location-1)

        elif step_line[location][1][1] == "*":
            num1 = step_line[location-1][1][1]
            num2 = step_line[location+1][1][1]
            result = mul(float(num1),float(num2))
            step_line[location] = (step_line[location-1][0], ('NUMBER', str(result)))
            step_line.pop(location+1)
            step_line.pop(location-1)

        elif step_line[location][1][1] == "/":
            num1 = step_line[location-1][1][1]
            num2 = step_line[location+1][1][1]
            result = div(float(num1),float(num2))
            step_line[location] = (step_line[location-1][0], ('NUMBER', str(result)))
            step_line.pop(location+1)
            step_line.pop(location-1)
        


        found = False
        

        for i in step_line:
            if i[1][0] == "OPARATOR" and i[1][1] != "=":
                found = True
                break
            else:
                found = False
                
        if found == False:
            Continue = False
            
        

        
    

    output = step_line #[0][1][1]
    for i in range(len(output)):
        element = step_line[i]
        if typeTest(element[1][1], float):
            if int(float(element[1][1])) == float(element[1][1]):
                output[i] = (element[0] , ("NUMBER",int(float(element[1][1]))) )

    return output     

def interpeter(finelise_code: list, storage: dict):
    for i in range(len(finelise_code)):
        charecter = finelise_code[i][1]
        step = finelise_code[i][0]
        
        code = []
        if i < len(finelise_code):
            # check code 
            if charecter[0] == "IDENTIFIER":
                set_value = finelise_code[i+2:len(finelise_code)]

                # error cheking
                Return = ""
                main_type = set_value[0][1][0]
                for char2 in set_value:
                    if char2[1][0] != main_type:
                        print("Error value type isn't the same!")
                        exit()
                    Return += str(char2[1][1])

                storage[charecter[1]] = (0,(main_type,Return))
                
                
            # checke if the charecter
            if charecter[0] == "KEYWORD":
                keyword = charecter
                for ch in finelise_code[i:len(finelise_code)]:
                    if ch[0] >= step+10:
                        code.append(ch)
                if charecter[1] == "output":
                    pr = ""
                    for i in code:
                        if i[1][1] == ",":
                            pr += " "
                        else:
                            pr += str(i[1][1])

                    location = 0
                    while location < len(pr):
                        char = pr[location]
                        if char == "\\":
                            if pr[location+1] == "n":
                                print("\n", end="")
                                location += 1
                            if pr[location+1] == "t":
                                print("\t", end="")
                                location += 1
                        else:
                            print(char,end="")
                        location += 1
                    
                        

    return finelise_code,storage      



file = open("test.yo", "r")
s = {}
for i in file.readlines():
    test = tokenizer(i)
    test = parser(test)
    test = finalise(test, s)
    test = interpeter(test, s)
    