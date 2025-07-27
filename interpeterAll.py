# this project is a basic interpeter
# Added:
# string, float and int operators support (for string only +)

# progres:
# adding veruble support # achived getting verbs
# creating interpeter (setting values)

# tokenizer (tokenize)

def tokenizer(input_calculator: str):
    operators = ["+","-","*","/","="]
    seperators = ["(",")"]
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

        elif character == ("'" or '"'):
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
            if token_type != "NUMBER":
                if add_to_output != "":
                    token_output.append((token_type,add_to_output))
                add_to_output= ""
            token_type = "NUMBER"

        elif character in seperators:
            if token_type:
                if add_to_output != "":
                    token_output.append((token_type,add_to_output))
                add_to_output= ""
            token_type = "SEPARATOR"
           

        elif (character not in operators) and not (character in seperators):
            if len(add_to_output) > 0:
                if not add_to_output[0].isalnum() and add_to_output[0] != ("" or " ") and character  in seperators:
                    # Error 
                    print(token_output, character, add_to_output)
                    print("The Identifier cant start by a operator!")
                    exit()
                

            if token_type != "IDENTIFIER":
                if add_to_output != "":
                    token_output.append((token_type,add_to_output))
                add_to_output= ""
            token_type = "IDENTIFIER"

        elif character.isalpha() and character not in operators:
            if token_type != "SYMBLE":
                if add_to_output != "":
                    token_output.append((token_type,add_to_output))
                add_to_output= ""
            token_type = "SYMBLE"

        add_to_output += character

    if add_to_output:
        token_output.append((token_type,add_to_output))

    return token_output


# parser (set up steps)
def parser(token_line: list):
    output = []
    operators = ['+', "-", "*", "/"]
    seperators = ["(",")"]
    step1 = ['+', "-"]
    step2 = ["*", "/"]
    sepAdd = 0 # add to make the enything in seperators first

    for i in range(len(token_line)):
        charecter = token_line[i]  

        

        if charecter[1] in seperators:
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
            output.append((0,charecter))      
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
    seperators = ["(",")"]
    operators = ["+", "-", "*", "/"]
     
    Continue = True
    output = []
    t = 0
    while Continue:
        

        # configering
        while t < len(step_line):
            char1 = step_line[t][1]
            if char1[1] in seperators:
                step_line.pop(t)

            if t < len(step_line)-1: 
                if char1[0] == "IDENTIFIER" and step_line[t+1][1][1] != "=":
                    if step_line[t+1][1][0] != "OPARATOR" or step_line[t+1][1][1] != "=":
                        if char1[1] in storege:
                            step_line.insert(t, (0,(storege.get(char1[1])[1][0],storege.get(char1[1])[1][1])))
                            step_line.pop(t + 1)
                        else:
                            print("Cant find veruble! ")
                            exit()
            elif char1[0] == "IDENTIFIER":
                if char1[1] in storege:
                    step_line.insert(t, (0,(storege.get(char1[1])[1][0],storege.get(char1[1])[1][1])))
                    step_line.pop(t + 1)
                else:
                    print("Cant find veruble! ")
                    exit()
                
            # dubuge see line
            t += 1

        biggest = 0
        location = 0
        
        for i in range(len(step_line)):
            char = step_line[i]
            if char[1][1] in seperators:
                continue
            elif char[0] > biggest:
                biggest = char[0]
                location = i
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

            step_line[location] = (0, (step_line[location-1][1][0], str(result)))
            step_line.pop(location+1)
            step_line.pop(location-1)

        elif step_line[location][1][1] == "-":
            num1 = step_line[location-1][1][1]
            num2 = step_line[location+1][1][1]
            result = min(float(num1),float(num2))
            step_line[location] = (0, ('NUMBER', str(result)))
            step_line.pop(location+1)
            step_line.pop(location-1)

        elif step_line[location][1][1] == "*":
            num1 = step_line[location-1][1][1]
            num2 = step_line[location+1][1][1]
            result = mul(float(num1),float(num2))
            step_line[location] = (0, ('NUMBER', str(result)))
            step_line.pop(location+1)
            step_line.pop(location-1)

        elif step_line[location][1][1] == "/":
            num1 = step_line[location-1][1][1]
            num2 = step_line[location+1][1][1]
            result = div(float(num1),float(num2))
            step_line[location] = (0, ('NUMBER', str(result)))
            step_line.pop(location+1)
            step_line.pop(location-1)
        


        found = False
        

        for i in output:
            if i[1][0] == "OPARATOR" and i[1][1] != "=":
                found = True
        if found == False:
            Continue = False
    
    print("finised")

    output = step_line #[0][1][1]
    for i in range(len(output)):
        element = step_line[i]
        if typeTest(element[1][1], float):
            if int(float(element[1][1])) == float(element[1][1]):
                output[i] = (element[0] , ("NUMBER",int(float(element[1][1]))) )

    return output     

def interpeter(finelise_code: list, storege: dict):
    for i in range(len(finalise)):
        charecter = finalise[i][1]
        
        if i < len(finelise_code):
            if charecter[0] == "IDENTIFIER":
                pass


test = "hi = 40 * hi" 

storage = {'hi': (0,("NUMBER", "40"))}

test = tokenizer(test)
test = parser(test)
test = finalise(test, storage)
print(test)

