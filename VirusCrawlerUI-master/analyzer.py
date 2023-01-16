from pikepdf import Pdf
import os
import sys
import subprocess
import shlex 
import json
import eel

pdfIdPath = "pdfid/pdfid.py"
# pdfIdPath = os.path.join(sys._MEIPASS, "pdfid.py")
pdfParserPath = "pdf-parser.py"
# pdfParserPath = os.path.join(sys._MEIPASS, "pdf-parser.py")

#Checks to see if there is an argument for a PDF file
#TO DO: Check if it's an actual PDF file
def fileCheck():
    if len(sys.argv) < 2:
        # print('Error, please provide a PDF file.')
        exit()

#grabs and returns the number of pages in the PDF as a list
def pageCount(pdf):
    pages = []
    for pageNum in range(len(pdf.pages)):
        pages.append(pageNum)
    return pages

#pdfid CLI tool to get info for signatures
def pdfid(fileName):
    # print(pythonPath + ' '+ pdfIdPath + ' ' + fileName)
    pdfid_Stream = os.popen(pythonPath + ' '+ pdfIdPath + ' ' + fileName, 'r')
    # pdfid_Stream = os.popen('C:/Users/Duncan/AppData/Local/Programs/Python/Python310/python.exe ./pdfid/pdfid.py ' + fileName, 'r')
    output = pdfid_Stream.read().splitlines()
    # print(output)
    return output[2:-2]

'''def removeFiles():

    try:
        cmd = shlex.split('rm eval.001.log eval.uc.001.log output.js test.js')
        subprocess.call(cmd)
    except FileNotFoundError:
        pass'''

#An instance of /AA or /OpenAction in conjunction with /JavaScript is one indication (95%) of malware
#calls the pdf-parser.py CLI tools with various options
class pdf_parser():

    # display stats for pdf document
    def stats(self, fileName):
        stream = os.popen(pythonPath + ' '+ pdfParserPath + ' -a ' + fileName, 'r')
        output = stream.read()
        # print(output)

    # string to search in indirect objects (except streams)
    # searches for string 'Encoding'
    # Returns: prints the entire object where the string was found
    def encoding(self, fileName):
        stream = os.popen(pythonPath + ' '+ pdfParserPath + ' --search=Encoding ' + fileName, 'r')       
        output = stream.read()
        # print(output)

    def jsSearch(self, fileName):
        stream = os.popen(pythonPath + ' '+ pdfParserPath + ' -s /JavaScript ' + fileName, 'r')    
        output = stream.read().splitlines()
        stream.close()
        # print(output)
        for line in output:
            if "obj" in line:
                return line

        return 0

    def getObjs(self, fileName):
        
        stream = os.popen(pythonPath + ' '+ pdfParserPath + ' -s /JavaScript ' + fileName, 'r')    
        output = stream.read().splitlines()
        stream.close()
        # print(output)
        myList = []

        for line in output:
            if "obj" in line:
                myList.append(line)

        return myList

    def jumpToObj(self, fileName, objNum):

        stream = os.popen(pythonPath + ' '+ pdfParserPath + ' -o ' + objNum + ' ' + fileName)
        output = stream.read().splitlines()
        stream.close()
        # print(output)
        return output

    def flateDecodeSearch(self, fileName, objNum):
        stream = os.popen(pythonPath + ' '+ pdfParserPath + ' -o ' + objNum + ' ' + fileName)
        output = stream.read().splitlines()
        # print(output)
        for line in output:
            if "/FlateDecode" in line:
                return True

        return False            
    #Does not work if python pdf-parser.py -s javascript returns more than 2 obj identifiers
    '''def createDeobfuscatedFiles(self, fileName):
        
        object_reference_list = []
        parser = pdf_parser()

        try:
            stream = os.popen('python pdf-parser.py -s javascript ' + fileName, 'r')
            output = stream.read()
            stream.close()

            output = (output.split('obj')) # put each object into its own list
            output = ' '.join(output)
            output = output.split(' ')  # separate each list into smaller lists

            #Find the position of the object reference of the /JS identifier 
            objectIndex = output.index('/JS')
            objectIndex = output[objectIndex+1]

            objectIndex = str(objectIndex)  #Turn the object number into a string.
            runCmd = f'python pdf-parser.py -o {objectIndex} {fileName}' #Create the command that will be ran.

            #Run the command
            runCmd = os.popen(runCmd, 'r')
            stream = runCmd.read()
            runCmd.close()

            #Search this new output for any encodings.
            newStr = stream.split(' ')  #Parse the normal looking output.

            # If /Filter exists then run the decode option
            if newStr.index('/Filter') != False:
                runCmd = f'python pdf-parser.py -o {objectIndex} -f {fileName}'
                runCmd = os.popen(runCmd, 'r') 
                stream = runCmd.read()

            retcode = os.popen(f'python pdf-parser.py -o {objectIndex} -f -d test.js {fileName}') 
            stream = retcode.read() #os.popen will error if the stream is not read().
            retcode.close()
            # Don't add 'r', or 'w' in os.popen if we don't intend to do anything with the stream.
            # A.k.a in situations where we only want to call the command to open a file.
            # Adding 'r' or 'w' in this situation breaks the pipe for some reason.
        
            #call spider-monkey which creates eval.uc.001.log and eval.001.log deobfuscated js files
            spiderMonkey = str('./js')    # Path to where spidermonkey program is located. 
            retcode = os.popen(f'{spiderMonkey} test.js')
            stream = retcode.read()
            retcode.close()

            #call repl which creates output.js file of deobfuscated js code
            retcode = os.popen('python repl/main.py test.js')
            stream = retcode.read()
            retcode.close()
    
        except:
            return 0'''

#the class that holds all of the signature detection functions
class signatures():
    
    # checks to see if signature one or two is present
    def sig_one_and_two(self, fileName, pdf):
        output = pdfid(fileName)
        # print(output)
        jsFlag = 0
        jsObfuscatedFlag = 0
        aaFlag = 0
        oaFlag = 0
        acroFlag = 0

        for i in range(0, len(output)):
            if "JavaScript" in output[i]:
                if(output[i][-1] != "0"):
                    #immediatly returns for signature 2 is obfuscation is found
                    if(output[i][-1] == ")"):
                        jsObfuscatedFlag = 1
                        return 2
                    jsFlag = 1

            elif "/AA" in output[i]:
                if(output[i][-1] != "0"):
                    aaFlag = 1

            elif "/OpenAction" in output[i]:
                if(output[i][-1] != "0"):
                    oaFlag = 1

            elif "/AcroForm" in output[i]:
                if(output[i][-1] != "0"):
                    acroFlag = 1

        #final check for signature 1
        if jsFlag == 1 or jsObfuscatedFlag == 1:
            if aaFlag == 1 or oaFlag == 1 or acroFlag == 1:
                if len(pageCount(pdf)) == 1:
                    return 1
        return 0

    def sig_three(self, fileName):
        cmd = pdf_parser()
        # print(cmd)
        if cmd.jsSearch(fileName) != 0:
            obj = cmd.jsSearch(fileName)
        else:
            return 0

        objNum = ''
        
        for i in range(4, len(obj)):
            if obj[i].isnumeric():
                objNum += obj[i]

            if not obj[i].isnumeric():
                break

        if cmd.flateDecodeSearch(fileName, objNum):
            return True

        return False 
    
    # Checks if /JS code has been referenced first
    def sig_three_v2(self, fileName):

        parser = pdf_parser()
        flag = False
        output = parser.getObjs(fileName)
        # print(output)

        try:
            # Find the obj reference #
            for i in range(0, len(output)):
                objNum = output[i][4]
                stream = parser.jumpToObj(fileName, objNum)
                # Find the /JS reference #
                for line in range(0, len(stream)):
                    if "/JS" in stream[line]:
                        index = stream[line].index("/JS")
                        js_reference_number = (stream[line][index+4])
                        if flag != True:
                            flag = parser.flateDecodeSearch(fileName, js_reference_number)

        except:
            return 0

        return flag

    def sig_four(self, fileName):
        
        jsObfuscatedFlag = 0
        jsFlag = 0

        output = pdfid(fileName)
        # print(output)

        #Check PDFID output for signs of /ObjStm
        #If found, un-embed it.
        for i in range(0, len(output)):
            if "ObjStm" in output[i]:
                if(output[i][-1] != "0"):
                    stream = os.popen(pythonPath + ' '+ pdfParserPath + ' -s /ObjStm -f {fileName} | ./pdfid/pdfid.py --force')
                    output = stream.read().splitlines()
                    stream.close()

        #Check the new PDFID output for signs of /JavaScript or /JS            
                    for i in range(0, len(output)):
                        if "JavaScript" in output[i]:
                            if (output[i][-1] != "0"):
                            #immediatly returns for signature 2 is obfuscation is found
                                if(output[i][-1] == ")"):
                                    jsObfuscatedFlag = 1
                                    return 2
            
                        elif "JavaScript" in output[i]:
                            if (output[i][-1] != "0"):
                                jsFlag = 1
            
                        elif "/JS" in output[i]:
                            if (output[i][-1] != "0"):
                                jsFlag = 1

        return jsFlag
            

    def sig_five(self):
        
        stream = os.popen('cat eval.001.log')
        output = stream.read()
        stream.close()
        # print(output)

        index = 1

        flag = False
        
        #Find identifier util.printf searching byte by byte
        while index > -1 :
            
            index = output.find('C')

            if output[index] == 'C' and output[index+1] == 'o' and output[index+2] == 'l' and output[index+3] == 'l' and output[index+4] == 'a' and output[index+5] == 'b' and output[index+6] == '.' and output[index+7] == 'c' and output[index+8] == 'o' and output[index+9] == 'l' and output[index+10] == 'l' and output[index+11] == 'e' and output[index+12] == 'c' and output[index+13] == 't' and output[index+14] == 'E' and output[index+15] == 'm' and output[index+16] == 'a' and output[index+17] == 'i' and output[index+18] == 'l' and output[index+19] == 'I' and output[index+20] == 'n' and output[index+21] == 'f' and output[index+22] == 'o':
               flag = True
               index = -1

            else:    
                output = list(output[index+1:])
                output = ''.join(output)
            
        return flag

    def sig_six(self):
        
        stream = os.popen('cat eval.001.log')
        output = stream.read()
        stream.close()
        # print(output)

        index = 1

        flag = False
        
        #Find identifier util.printf searching byte by byte
        while index > -1 :
            
            index = output.find('C')

            if output[index] == 'C' and output[index+1] == 'o' and output[index+2] == 'l' and output[index+3] == 'l' and output[index+4] == 'a' and output[index+5] == 'b' and output[index+6] == '.' and output[index+7] == 'g' and output[index+8] == 'e' and output[index+9] == 't' and output[index+10] == 'I' and output[index+11] == 'c' and output[index+12] == 'o' and output[index+13] == 'n':
               flag = True
               index = -1

            else:    
                output = list(output[index+1:])
                output = ''.join(output)
            
        return flag

    def sig_seven(self):
        # print(output)
        
        stream = os.popen('cat eval.001.log')
        output = stream.read()
        stream.close()

        index = 1

        flag = False
        
        #Find identifier util.printf searching byte by byte
        while index > -1 :
            
            index = output.find('u')

            if output[index] == 'u' and output[index+1] == 't' and output[index+2] == 'i' and output[index+3] == 'l' and output[index+4] == '.' and output[index+5] == 'p' and output[index+6] == 'r' and output[index+7] == 'i' and output[index+8] == 'n' and output[index+9] == 't' and output[index+10] == 'f':
               flag = True
               index = -1

            else:    
                output = list(output[index+1:])
                output = ''.join(output)
            
        return flag

    def sig_eight(self):
        
        # print(output)
        stream = os.popen('cat eval.001.log')
        output = stream.read()
        stream.close()

        index = 1

        flag = False
        
        #Find identifier util.printf searching byte by byte
        while index > -1 :
            
            index = output.find('s')

            if output[index] == 's' and output[index+1] == 'p' and output[index+2] == 'e' and output[index+3] == 'l' and output[index+4] == 'l' and output[index+5] == '.' and output[index+6] == 'c' and output[index+7] == 'u' and output[index+8] == 's' and output[index+9] == 't' and output[index+10] == 'o' and output[index+11] == 'm' and output[index+12] == 'D' and output[index+13] == 'i' and output[index+14] == 'c' and output[index+15] == 't' and output[index+16] == 'i' and output[index+17] == 'o' and output[index+18] == 'n' and output[index+19] == 'a' and output[index+20] == 'r' and output[index+21] == 'y' and output[index+22] == 'O' and output[index+23] == 'p' and output[index+24] == 'e' and output[index+25] == 'n':
               flag = True
               index = -1

            else:    
                output = list(output[index+1:])
                output = ''.join(output)
            
        return flag

    def sig_nine(self):
        
        stream = os.popen('cat eval.001.log')
        output = stream.read()
        stream.close()

        index = 1
        # print(output)

        flag = False
        
        #Find identifier util.printf searching byte by byte
        while index > -1 :
            
            index = output.find('g')

            if output[index] == 'g' and output[index+1] == 'e' and output[index+2] == 't' and output[index+3] == 'A' and output[index+4] == 'n' and output[index+5] == 'n' and output[index+6] == 'o' and output[index+7] == 't' and output[index+8] == 's':
               flag = True
               index = -1

            else:    
                output = list(output[index+1:])
                output = ''.join(output)
            
        return flag
    
@eel.expose
def doWork(fileName, pathName):
    global pythonPath
    
    
    if pathName is None:
        pythonPath = 'python'
    else:
        pythonPath = pathName
    
    for r,d,f in os.walk("c:\\"):
        for files in f:
            if files == fileName:
                fileName = os.path.join(r,files)
                
    eel.show_log(fileName)
                
    pdf = Pdf.open(fileName)
    pages = pageCount(pdf)

    file = (fileName)

    cmd = pdf_parser()
    signature = signatures()
    flag = 0
    #cmd.createDeobfuscatedFiles(file)

    jsonResult = {"result": 0, "sig_one": 0, "sig_two": 0, "sig_three": 0, "sig_four": 0}

    #cmd.stats(file)
    #cmd.encoding(file)
    if signature.sig_one_and_two(file, pdf) == 1:
        #print("WARNING, SIGNATURE 1 TRIGGERED")
        jsonResult["result"] = 1
        jsonResult["sig_one"] = 1
        flag = 1
    if signature.sig_one_and_two(file, pdf) == 2:
        #print("WARNING, SIGNATURE 2 TRIGGERED") 
        jsonResult["result"] = 1
        jsonResult["sig_two"] = 1
        flag = 1
    if signature.sig_three(file):
        #print('WARNING, SIGNATURE 3 TRIGGERED')
        jsonResult["result"] = 1
        jsonResult["sig_three"] = 1
        flag = 1
    if signature.sig_four(file):
        jsonResult["result"] = 1
        jsonResult["sig_four"] = 1  
        flag = 1       

    if flag == 0:
        jsonResult["result"] = 0

    #removeFiles()
    return json.dumps(jsonResult)

def main():
    doWork()


if __name__ == "__main__":
    main()