
import sympy


SCHEMATIC = """\
                __
              __ll__                                  
             __ ll __                                 
                ll                                  
                ll    Vcc {vsVal}
                ll
            llllllllll                                
            ll      ll                                
            ll      ll                                
            ll      ll 
            ll      ll    R1 {r1Val}
            ll      ll                    
            ll      ll                   
            ll      ll                   
            llllllllll                                
                ll                                
                ll                                    
                ll    V1 {v1Val}
                ll
                ll
            llllllllll                                
            ll      ll                                
            ll      ll                                
            ll      ll 
            ll      ll    R2 {r2Val}          
            ll      ll                    
            ll      ll                   
            ll      ll                   
            llllllllll                                                       
                ll                                
                ll                                    
                ll    V2 {v2Val}
                ll
                ll
            llllllllll                                
            ll      ll                                
            ll      ll                                
            ll      ll 
            ll      ll    R3 {r3Val}
            ll      ll                    
            ll      ll                   
            ll      ll                   
            llllllllll         
                ll                                    
                ll                                    
            ____ll____                                
              ______                                  
                __                                    
        """


# TODO add user input using arguments
# TODO make a algotrithm that solves for easy available resistor values
# TODO Print only the values


# volatage divider symbols
vs = sympy.Symbol('vs')
r1 = sympy.Symbol('r1')
r2 = sympy.Symbol('r2')
vout = sympy.Symbol('vout')

# the equation
voltageDivider = sympy.Eq((vs * r2) / (r1 + r2), vout)

# the desired voltages
set_vs = 5
set_vout1 = 3
set_vout2 = 1.2
set_pot = 10000

def main():
    getInput()
    calculate()
    printSchematicValues()

def calculate():
    # make these global so other functions can access them
    global v1ResistorResult, v2ResistorResult
    
    
    # put in all the values to find R3 (the bottom resistor, r2 in the equation)
    v2Resistor = voltageDivider.subs(vs, set_vout1).subs(r1, set_pot).subs(vout, set_vout2)

    # solve for R3 (r2 in the equation)
    v2ResistorResult = sympy.solve(v2Resistor, r2)[0] # take the first index of all the posibile anwsers

    #total resistance of the v2 network (the sum of v2Resistor and the potmeter)
    rt = v2ResistorResult + set_pot

    v1Resistor = voltageDivider.subs(vs, set_vs).subs(r2, rt).subs(vout, set_vout1)
    v1ResistorResult = sympy.solve(v1Resistor, r1)[0] # take the first index of all the posibile anwsers


def getInput():
    global set_vs, set_pot, set_vout1, set_vout2
    
    # TODO Polish this section a bit 
    
    input1Pending = True
    while (input1Pending):
        input1 = input("set_vs: ")
        if(input1 == "schematic"):
            printSchematic()
            exit()
        elif(input1.isdecimal()):
            set_vs = input1
            input1Pending = False
        else:
            print("error wrong input")
    
    set_pot = int(input("set_r2: "))
    set_vout1 = float(input("set_vout1: "))
    set_vout2 = float(input("set_vout2: "))


def formatResistance(resistance, decSymbol):

    res = int(resistance)/1000
    # limit the number of decimals, thank you stackoverflow
    res = "{:.2f}".format(res)

    # remove all the bullshit zeros, thank you stackoverflow
    res = str(res.rstrip('0').rstrip('.')) if '.' in res else res    

    return addUnit(res, 'k')


def formatVoltage(voltage):
    return addUnit(voltage, 'v')


def addUnit(text, decSymbol):
    text = str(text)
     # if the string has a decimal place replace that with the decSymbol ('v' or 'k')
    if '.' in text:
        text = str(text).replace('.', decSymbol)
    # else just add the k at the end
    else:
        text += decSymbol
    return text


# print the schematic with values
def printSchematicValues():
    
    # insert all the values
    print(SCHEMATIC.format(vsVal = formatVoltage(set_vs), r1Val = formatResistance(v1ResistorResult, 'k'), v1Val = formatVoltage(set_vout1), r2Val = formatResistance(set_pot, 'k'), v2Val = formatVoltage(set_vout2), r3Val = formatResistance(v2ResistorResult, 'k')))


def printSchematic():
    s = SCHEMATIC
   
    # loop through each string formattable field
    for x in range(s.count('{')):
        strStart = s.index('{')
        strEnd = s.index('}')
        # clear them
        s = s.replace(s[strStart:strEnd+1], "")

    # print the clean schematic 
    print(s)


if __name__ == "__main__":
    main()