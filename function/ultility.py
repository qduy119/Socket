import os

def getRequest(request):
    # Parse request
    class Parse:
        def __init__(self, request):
            if request == "":
                self.empty = True	# If there is no request
                self.method = ""
                self.path = ""
                self.content = ""
            else:
                self.empty = False
                requestComponents = request.split("\r\n")
                self.method = requestComponents[0].split(" ")[0]		# Parse GET method
                self.path = requestComponents[0].split(" ")[1]		    # Parse path
                self.content = requestComponents[-1]					# Parse content
    return Parse(request)

def Response(path):
        if(path == "/"):
            path = "/index.html"
        # Parse file name
        typeOfFile = path.split(".")[-1]
        listFiles = getListOfFiles("page")
        status = 0
        filePath = ""
        contentType = ""
        startLine = ""
        if(("page" + path) in listFiles):
            status = 401 if(path == "/401.html") else 200
            filePath = "page" + path
        else:
            status = 404
            filePath = "page/404.html"

        # self.connection = "Keep-Alive: timeout=10, max=100\r\nConnection: keep-alive"
        # self.connection = "Connection: close"
        if(typeOfFile in ["html", "htm"]):
            contentType = "Content-Type: text/html"
        elif(typeOfFile == "css"):
            contentType = "Content-Type: text/css"
        elif(typeOfFile == "png"):
            contentType = "Content-Type: image/png"
        elif(typeOfFile in ["jpg", "jpeg"]):
            contentType = "Content-Type: image/jpeg"
        elif(typeOfFile == "ico"):
            contentType = "Content-Type: image/x-icon"
        else:
            # Content type: text/html to load page 404 error when file does not exist
            contentType = "Content-Type: text/html"

        if(status == 200):
            startLine = "HTTP/1.1 200 OK"
        elif(status == 401):
            startLine = "HTTP/1.1 401 Unauthorized"
        else:
            startLine = "HTTP/1.1 404 Not Found"

        content = open(filePath, "rb").read()
        contentLength = "Content-Length: %d"%(len(content))
        headerResponse = "%s\r\n%s\r\n%s\r\n\r\n"%(startLine, contentType, contentLength)
        print("--------------------\n[HEADER RESPONSE for %s]\n%s"%(path, headerResponse))
        result = headerResponse.encode("utf-8") + content + "\r\n".encode("utf-8")
        print("--------------------\n[SERVER]\nTransfer file %s completely\n"%(filePath.split("/")[-1]))
        return result

# Get list of all files in folder "Page"
def getListOfFiles(dirName):
    # Create a list of file and sub directories  
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = dirName + '/' + entry
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles
