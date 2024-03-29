#!/usr/bin/python3

import sys

oneByteInstructions={"NOP":"00",
                     "LDAR":"05",
                     "LDBR":"06",
                     "STAR":"09",
                     "STBR":"0a",
                     "LDAB":"0b",
                     "LDBA":"0c",
                     "LDCA":"0d",
                     "LDCB":"0e",
                     "LDAC":"0f",
                     "LDBC":"10",
                     "LDCR":"13",
                     "STCR":"15",
                     "OUTA":"17",
                     "OUTB":"18",
                     "OUTR":"19",
                     "OUTS":"1b",
                     "OUTU":"1c",
                     "ADDR":"1d",
                     "SUBR":"20",
                     "ROR1":"23",
                     "ROR2":"24",
                     "ROR3":"25",
                     "ROR4":"26",
                     "ROR5":"27",
                     "ROR6":"28",
                     "ROR7":"29",
                     "NANDR":"2a",
                     "STPC":"30",
                     "LDPC":"31",
                     "HLT":"ff",}

twoBytesInstructions={"LDAI":"01",
                      "LDBI":"02",
                      "LDCI":"11",
                      "OUTI":"16",
                      "ADDI":"1e",
                      "SUBI":"21",
                      "NANDI":"2b"}

threeBytesInstructions={"LDA":"03",
                        "LDB":"04",
                        "STA":"07",
                        "STB":"08",
                        "LDC":"12",
                        "STC":"14",
                        "OUT":"1a",
                        "ADD":"1f",
                        "SUB":"22",
                        "NAND":"2c",
                        "JMP":"2d",
                        "JZ":"2e",
                        "JC":"2f"}

def printUsage():
    print("Usage: asmCompiler inputFile [-o outputFile] [-h]")

def printHelp():
    print("Usage: asmCompiler inputFile [-o outputFile] [-h]")
    print("  -h    Print this help message")
    print("  -o    Specify output file")

def compileFile(inputFile,outputFile):
    file=open(inputFile)
    code=file.read()
    file.close()
    compiledCode=compileCode(code)
    file=open(outputFile,"w")
    file.write(compiledCode)
    file.close()

def evalMacros(code):
    label="autogenlabel%d"
    lbl=0
    needStack=False
    for i,inst in enumerate(code):
        if inst[0]=="JNC":
            code[i:i+1]=[["JC",label%lbl],["JMP",inst[1]],[label%lbl+":"]]
            lbl+=1
        elif inst[0]=="JNZ":
            code[i:i+1]=[["JZ",label%lbl],["JMP",inst[1]],[label%lbl+":"]]
            lbl+=1
        elif inst[0]=="JGZ":
            code[i:i+1]=[["JZ",label%lbl],["NANDI","80"],["LDBA"],["NANDR"],["JZ",inst[1]],[label%lbl+":"]]
            lbl+=1
        elif inst[0]=="JLZ":
            code[i:i+1]=[["NANDI","80"],["LDBA"],["NANDR"],["JZ",label%lbl],["JMP",inst[1]],[label%lbl+":"]]
            lbl+=1
        elif inst[0]=="ROL1":
            code[i]=["ROR7"]
        elif inst[0]=="ROL2":
            code[i]=["ROR6"]
        elif inst[0]=="ROL3":
            code[i]=["ROR5"]
        elif inst[0]=="ROL4":
            code[i]=["ROR4"]
        elif inst[0]=="ROL5":
            code[i]=["ROR3"]
        elif inst[0]=="ROL6":
            code[i]=["ROR2"]
        elif inst[0]=="ROL7":
            code[i]=["ROR1"]
        elif inst[0]=="SHR1":
            code[i:i+1]=[["ROR1"],["STB","#B"],["NANDI","7f"],["LDBA"],["NANDR"],["LDB","#B"]]
        elif inst[0]=="SHR2":
            code[i:i+1]=[["ROR2"],["STB","#B"],["NANDI","3f"],["LDBA"],["NANDR"],["LDB","#B"]]
        elif inst[0]=="SHR3":
            code[i:i+1]=[["ROR3"],["STB","#B"],["NANDI","1f"],["LDBA"],["NANDR"],["LDB","#B"]]
        elif inst[0]=="SHR4":
            code[i:i+1]=[["ROR4"],["STB","#B"],["NANDI","f"],["LDBA"],["NANDR"],["LDB","#B"]]
        elif inst[0]=="SHR5":
            code[i:i+1]=[["ROR5"],["STB","#B"],["NANDI","7"],["LDBA"],["NANDR"],["LDB","#B"]]
        elif inst[0]=="SHR6":
            code[i:i+1]=[["ROR6"],["STB","#B"],["NANDI","3"],["LDBA"],["NANDR"],["LDB","#B"]]
        elif inst[0]=="SHR7":
            code[i:i+1]=[["ROR7"],["STB","#B"],["NANDI","1"],["LDBA"],["NANDR"],["LDB","#B"]]
        elif inst[0]=="SHL1":
            code[i:i+1]=[["ROR7"],["STB","#B"],["NANDI","fe"],["LDBA"],["NANDR"],["LDB","#B"]]
        elif inst[0]=="SHL2":
            code[i:i+1]=[["ROR6"],["STB","#B"],["NANDI","fc"],["LDBA"],["NANDR"],["LDB","#B"]]
        elif inst[0]=="SHL3":
            code[i:i+1]=[["ROR5"],["STB","#B"],["NANDI","f8"],["LDBA"],["NANDR"],["LDB","#B"]]
        elif inst[0]=="SHL4":
            code[i:i+1]=[["ROR4"],["STB","#B"],["NANDI","f0"],["LDBA"],["NANDR"],["LDB","#B"]]
        elif inst[0]=="SHL5":
            code[i:i+1]=[["ROR3"],["STB","#B"],["NANDI","e0"],["LDBA"],["NANDR"],["LDB","#B"]]
        elif inst[0]=="SHL6":
            code[i:i+1]=[["ROR2"],["STB","#B"],["NANDI","c0"],["LDBA"],["NANDR"],["LDB","#B"]]
        elif inst[0]=="SHL7":
            code[i:i+1]=[["ROR1"],["STB","#B"],["NANDI","80"],["LDBA"],["NANDR"],["LDB","#B"]]
        elif inst[0]=="INITSTACK":
            code[i:i+1]=[["STA","#A"],["LDAI","ff"],["STA","#SPH"],["LDAI","fa"],["STA","#SPL"],["LDA","#A"]]
        elif inst[0]=="PUSHA":
            code[i:i+1]=[["STA","#A"],["STB","#B"],["STC","#C"],["LDCA"],["LDA","#SPL"],["LDBI","1"],["JZ",label%lbl],["JMP",label%lbl+"b"],[label%lbl+":"],["LDA","#SPH"],["SUBR"],["STA","#SPH"],["LDA","#SPL"],[label%lbl+"b:"],["SUBR"],["STA","#SPL"],["LDBA"],["LDA","#SPH"],["STCR"],["LDA","#A"],["LDB","#B"],["LDC","#C"]]
            lbl+=1
            needStack=True
        elif inst[0]=="PUSHB":
            code[i:i+1]=[["STA","#A"],["STB","#B"],["STC","#C"],["LDCB"],["LDA","#SPL"],["LDBI","1"],["JZ",label%lbl],["JMP",label%lbl+"b"],[label%lbl+":"],["LDA","#SPH"],["SUBR"],["STA","#SPH"],["LDA","#SPL"],[label%lbl+"b:"],["SUBR"],["STA","#SPL"],["LDBA"],["LDA","#SPH"],["STCR"],["LDA","#A"],["LDB","#B"],["LDC","#C"]]
            lbl+=1
            needStack=True
        elif inst[0]=="PUSHC":
            code[i:i+1]=[["STA","#A"],["STB","#B"],["LDA","#SPL"],["LDBI","1"],["JZ",label%lbl],["JMP",label%lbl+"b"],[label%lbl+":"],["LDA","#SPH"],["SUBR"],["STA","#SPH"],["LDA","#SPL"],[label%lbl+"b:"],["SUBR"],["STA","#SPL"],["LDBA"],["LDA","#SPH"],["STCR"],["LDA","#A"],["LDB","#B"]]
            lbl+=1
            needStack=True
        elif inst[0]=="POPA":
            code[i:i+1]=[["STB","#B"],["STC","#C"],["LDA","#SPH"],["LDB","#SPL"],["LDCR"],["LDAB"],["ADDI","1"],["STA","#SPL"],["JZ",label%lbl],["JMP",label%lbl+"b"],[label%lbl+":"],["LDA","#SPH"],["ADDR"],["STA","#SPH"],[label%lbl+"b:"],["LDAC"],["LDB","#B"],["STC","#C"]]
            lbl+=1
            needStack=True
        elif inst[0]=="POPB":
            code[i:i+1]=[["STA","#A"],["STC","#C"],["LDA","#SPH"],["LDB","#SPL"],["LDCR"],["LDAB"],["ADDI","1"],["STA","#SPL"],["JZ",label%lbl],["JMP",label%lbl+"b"],[label%lbl+":"],["LDA","#SPH"],["ADDR"],["STA","#SPH"],[label%lbl+"b:"],["LDBC"],["LDA","#A"],["STC","#C"]]
            lbl+=1
            needStack=True
        elif inst[0]=="POPC":
            code[i:i+1]=[["STA","#A"],["STB","#B"],["LDA","#SPH"],["LDB","#SPL"],["LDCR"],["LDAB"],["ADDI","1"],["STA","#SPL"],["JZ",label%lbl],["JMP",label%lbl+"b"],[label%lbl+":"],["LDA","#SPH"],["ADDR"],["STA","#SPH"],[label%lbl+"b:"],["LDA","#A"],["STB","#B"]]
            lbl+=1
            needStack=True
        elif inst[0]=="CALL":
            code[i:i+1]=[["STPC"],["STA","#B"],["LDAI","1"],["STA","#A"],["LDAB"],["LDCA"],["ADDI","67"],["STA","#C"],["LDBC"],["SUBR"],["JC",label%lbl+"b"],["LDAI","0"],["STA","#A"],[label%lbl+"b:"],["LDA","#SPL"],["LDBI","1"],["JZ",label%lbl+"c"],["JMP",label%lbl+"d"],[label%lbl+"c:"],["LDA","#SPH"],["SUBR"],["STA","#SPH"],["LDA","#SPL"],[label%lbl+"d:"],["SUBR"],["STA","#SPL"],["LDBA"],["LDA","#SPH"],["LDC","#C"],["STCR"],["LDC","#B"],["LDBI","1"],["LDA","#A"],["JZ",label%lbl+"e"],["LDAC"],["ADDR"],["LDCA"],[label%lbl+"e:"],["LDA","#SPL"],["JZ",label%lbl+"f"],["JMP",label%lbl+"g"],[label%lbl+"f:"],["LDA","#SPH"],["SUBR"],["STA","#SPH"],["LDA","#SPL"],[label%lbl+"g:"],["SUBR"],["STA","#SPL"],["LDBA"],["LDA","#SPH"],["STCR"],["JMP",inst[1]]]
            lbl+=1
            needStack=True
        elif inst[0]=="RET":
            code[i:i+1]=[["STC","#C"],["LDA","#SPH"],["LDB","#SPL"],["LDCR"],["LDAB"],["ADDI","1"],["STA","#SPL"],["JZ",label%lbl],["JMP",label%lbl+"b"],[label%lbl+":"],["LDA","#SPH"],["ADDR"],["STA","#SPH"],[label%lbl+"b:"],["STC","#A"],["LDA","#SPH"],["LDB","#SPL"],["LDCR"],["LDAB"],["ADDI","1"],["STA","#SPL"],["JZ",label%lbl+"c"],["JMP",label%lbl+"d"],[label%lbl+"c:"],["LDA","#SPH"],["ADDR"],["STA","#SPH"],[label%lbl+"d:"],["LDBC"],["LDA","#A"],["LDC","#C"],["LDPC"]]
            lbl+=1
            needStack=True
    return needStack

def compileCode(code):
    compiledCode="v2.0 raw\n"
    compiled=[]

    code=[c.upper().strip().split() if ";" not in c else c[:c.index(";")].upper().strip().split() for c in code.splitlines() if c.strip()!="" and c.strip()[0]!=";"]
    if evalMacros(code):
        code=[["LDAI","ff"],["STA","#SPH"],["LDAI","fa"],["STA","#SPL"],["LDAI","0"]]+code

    labels={}
    variables={"#SPL":"fffb","#SPH":"fffc","#A":"fffd","#B":"fffe","#C":"ffff"}
    findLabelsAndVariables(code,labels,variables)
    replaceLabels(code,labels)
    replaceVariables(code,variables)

    for inst in code:
        compileInstruction(inst,compiled)

    compiledCode+=" ".join(compiled)
    return compiledCode

def evalNum(num,b=1):
    n=int(num,16)
    while n<0:
        n+=256**b
    while n>=256**b:
        n-=256**b
    return n

def findLabelsAndVariables(code,labels,variables):
    address=0
    for inst in code:
        if inst[0][0]=="*":
            variables[inst[0]]=hex(evalNum(inst[1],2))[2:]
        elif inst[0][-1]==":":
            labels[inst[0][:-1]]=hex(address)[2:]
        elif inst[0] in oneByteInstructions:
            address+=1
        elif inst[0] in twoBytesInstructions:
            address+=2
        elif inst[0] in threeBytesInstructions:
            address+=3

def replaceLabels(code,labels):
    for i in range(len(code)):
        if len(code[i])>1 and code[i][1] in labels:
            code[i][1]=labels[code[i][1]]

def replaceVariables(code,variables):
    for i in range(len(code)):
        if len(code[i])>1 and code[i][1] in variables:
            code[i][1]=variables[code[i][1]]

def compileInstruction(inst,compiled):
    if inst[0] in oneByteInstructions:
        compiled.append(oneByteInstructions[inst[0]])
    elif inst[0] in twoBytesInstructions:
        compiled.append(twoBytesInstructions[inst[0]])
        compiled.append(hex(evalNum(inst[1]))[2:])
    elif inst[0] in threeBytesInstructions:
        compiled.append(threeBytesInstructions[inst[0]])
        compiled.append(hex(evalNum(inst[1],2)>>8)[2:])
        compiled.append(hex(evalNum(inst[1],2)&0xff)[2:])

if __name__=="__main__":
    if len(sys.argv)<2:
        printUsage()
        sys.exit(0)
    if "-h" in sys.argv:
        printHelp()
        sys.exit(0)
    inputFile=None
    if len(sys.argv)>1:
        inputFile=sys.argv[1]
    if "-o" in sys.argv and len(sys.argv)>sys.argv.index("-o")+1:
        outputFile=sys.argv[sys.argv.index("-o")+1]
    elif inputFile!=None:
        outputFile=inputFile[:inputFile.index(".")]+".out" if "." in inputFile else inputFile+".out"
    if inputFile!=None:
        compileFile(inputFile,outputFile)
    else:
        printUsage()
