import os

def getRequest(request):
    # Parse request
    class Parse:
        def __init__(self, request):
            if request == "":
                self.empty = True	# Nếu không có request
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
        connection = "Connection: close"
        if(("page" + path) in listFiles):
            status = 401 if(path == "/401.html") else 200
            filePath = "page" + path
        else:
            status = 404
            filePath = "page/404.html"

        # Chỉ xét những Content-Type có trong đồ án này
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
            # Content-Type: text/html để load page 404 khi file không tồn tại
            contentType = "Content-Type: text/html"

        if(status == 200):
            startLine = "HTTP/1.1 200 OK"
        elif(status == 401):
            startLine = "HTTP/1.1 401 Unauthorized"
        else:
            startLine = "HTTP/1.1 404 Not Found"

        content = open(filePath, "rb").read()
        contentLength = "Content-Length: %d"%(len(content))
        headerResponse = "%s\r\n%s\r\n%s\r\n%s\r\n\r\n"%(startLine, contentType, contentLength, connection)
        print("--------------------\n[HEADER RESPONSE for %s]\n%s"%(path, headerResponse))
        result = headerResponse.encode("utf-8") + content + "\r\n".encode("utf-8")
        print("--------------------\n[SERVER]\nTransfer file %s completely\n"%(filePath.split("/")[-1]))
        return result

# Hàm lấy tất cả các file trong folder "Page"
def getListOfFiles(dirName):
    # # Tạo một danh sách chứa file và các đường dẫn con  
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = dirName + '/' + entry
        # Nếu entry cũng là 1 đường dẫn thì lấy danh sách các file trong đường dẫn đó
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles
