import os

def getRequest(request):
    class Parse:
        def __init__(self, request):
            if request == "":
                self.empty = True	# If there is no request
            else:
                self.empty = False
                requestComponents = request.split("\r\n")
                self.method = requestComponents[0].split(" ")[0]		# GET method
                self.path = requestComponents[0].split(" ")[1]		# GET path
                self.content = requestComponents[-1]					# GET request content
    return Parse(request)

class Response:
    def __init__(self, path):
        if(path == "/"):
            path = "/index.html"
        # Parse file name
        typeOfFile = path.split(".")[-1]

        listFiles = getListOfFiles("page")
        if(("page" + path) in listFiles):
            self.status = 401 if(path == "/401.html") else 200
            self.path = "page" + path
            # If login via url, throw 404 error
            if(path == "/images.html" and open("login.txt", "r").read() == "GET"):
                self.status = 404
                self.path = "page/404.html"
        else:
            self.status = 404
            self.path = "page/404.html"

        # self.connection = "Connection: close"
        if(typeOfFile in ["html", "htm"]):
            self.contentType = "Content-Type: text/html"
        elif(typeOfFile == "css"):
            self.contentType = "Content-Type: text/css"
        elif(typeOfFile == "png"):
            self.contentType = "Content-Type: image/png"
        elif(typeOfFile in ["jpg", "jpeg"]):
            self.contentType = "Content-Type: image/jpeg"
        elif(typeOfFile == "ico"):
            self.contentType = "Content-Type: image/x-icon"
        else:
            # self.contentType = "Content-Type: application/octet-stream"
            # Content type: text/html to load page 404 error when file does not exist
            self.contentType = "Content-Type: text/html"

        if(self.status == 200):
            header = "HTTP/1.1 200 OK"
        elif(self.status == 401):
            header = "HTTP/1.1 401 Unauthorized"
        else:
            header = "HTTP/1.1 404 Not Found"

        # self.header = "%s\r\n%s\r\n%s\r\n"%(header, self.contentType, self.connection)
        self.header = "%s\r\n%s\r\n"%(header, self.contentType)

    def transferFile(self):
        content = open(self.path, "rb").read()
        self.header += "Content-Length: %d\r\n\r\n"%(len(content))
        print("--------------------\n[SERVER]\n[HEADER]\n%s"%(self.header))
        result = self.header.encode("utf-8") + content + "\r\n".encode("utf-8")
        print("--------------------\n[SERVER]\nTransfer file %s completely\n"%(self.path.split("/")[-1]))
        return result
        # self.header += "Transfer-Encoding: chunked\r\n\r\n"
        # BUFF_SIZE = 1024*50
        # content = "".encode("utf-8")
        # buffer = open(self.path, "rb")
        # L = buffer.read(BUFF_SIZE)
        # while(len(L) == BUFF_SIZE):
        #     size = len(L)
        #     content += ("{:X}\r\n".format(size)).encode('utf-8')
        #     content += L 
        #     content += "\r\n".encode()
        #     L = buffer.read(BUFF_SIZE)
        # size = len(L)
        # content += ("{:X}\r\n".format(size)).encode('utf-8')
        # content += L
        # content += "\r\n0".encode('utf-8')

        # print("--------------------\n[SERVER]\n[HEADER]\n%s"%(self.header))
        # result = self.header.encode("utf-8") + content + "\r\n\r\n".encode("utf-8")
        # print("--------------------\n[SERVER]\nTransfer file %s completely\n"%(self.path.split("/")[-1]))
        # return result

# GET Method
def getMethod(connection, request):
    open("login.txt", "w").write("GET")
    response = Response(request.path).transferFile()
    connection.sendall(response)
    print("--------------------\n[SERVER]\nRequest %s with path %s DONE\n"%(request.method, request.path))

# POST Method
def postMethod(connection, request):
    if(request.content == "uname=admin&psw=123456&remember=on" or request.content == "uname=admin&psw=123456"):
        open("login.txt", "w").write("POST")
        response = Response(request.path).transferFile()
    else:
        response = Response("/401.html").transferFile()
    connection.sendall(response)
    print("--------------------\n[SERVER]\nRequest %s with path %s DONE\n"%(request.method,request.path))

# Get list of all files in folder Page
def getListOfFiles(dirName):
    # Create a list of file and sub directories  
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = dirName + '/' + entry
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles