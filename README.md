# SS.Moker

---

A restful service simulator for those who is developing a client for a not published service like me.
    
Of course it will **not** provide a **REAL** service logic, It can only send response for fixed contents in specified data file, with some variables supported by extensible plugins.
    
##Usage

---

Simply execute ss_mock.py to start the server.

Then you can post or get content from it.

##Configuration

---

###mock_index.json

    [
        {
            "path": "/sendmesreq/\\d+",
            "datafile": "sendsms.json",
            "request": {
                "url": "1",
                "encoding": "utf-8",
                "format": "json"
            },
            "method": ["POST", "GET"],
            "response": {
                "url": 0,
                "encoding": "utf-8",
                "header": {
                    "content-type": "application/json"
                }
            }
        }
    ]

Its a json array, each element in it is a fake endpoint.

+ **path**: A regular express to match the requesting url.

+ **datafile**: A data file in 'data' dir to respond the client request.

+ **request**: Reserved.

+ **method**: An array of 'POST' or 'GET', here we can select different data file for different request method.

+ **reponse**: Detail of response.

  - *url*: If the response content should be url_encoded.
  
  - *encoding*: Encoding of output content.
  
  - *header*: Http header will send to the client.
  
###data

We will put data files in 'data' folder.

In the sample named 'sendsms.json':

    {
      "RspCode": "0000",
      "RspDesc": "_|{'type':'datafile', 'name': 'sample', 'method': 'random', 'pattern': '%s'}|_"
    }

It's the content that will reply the http request to url "/sendsms/28348".

There is a parameter in the item "RspDesc" surrounded by "_|" and "|_". In this case It means the item will processed by the plugin *"datafile"*, the parameters is:

+ **name**: Datafile name.

+ **method**: "random" or other, means that it will read a random line for the data file, or line by line.

+ **pattern**: Here we can use it to format the line read from the datafile for output.

And now we have provide two addtional plugins:

+ **timedata**: It can generate date time and format it for the return value.

+ **sequence**: A simple auto increment ID.


More details can get form pydocs in the plugins folder. 


