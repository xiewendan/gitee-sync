if __name__ == '__main__':
    import requests

    szUrl = "http://10.249.80.162:5000/upload"
    szPath = r"C:\Users\gzxiejinchun\Desktop\code review优化.pdf"

    dictFile = {'file': open(szPath, 'rb')}

    RequestObj = requests.post(szUrl, files=dictFile)

    print(RequestObj.url)
    print(RequestObj.text)
