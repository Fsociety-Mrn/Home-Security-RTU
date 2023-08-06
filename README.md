# Production Website 

### Requirements 
dapat python version ay 3.10.x

## MGA DAPAT AT HINDI DAPAT GAWIN KASI MAG KAKA BUG

1. kapag after mag register name, tapusing ang facial capture at facial training  
kasi magkakaroon ng empty folder sa Registered-Faces, at magkakaroon ng bug sa facial training  
2. kapag nag facial training wag i rerefresh!

3. kapag walang camera madetect, lipat lipat mo lang ng camera tas rerun mo
4. dapat sa registered-faces folder walang empty folder doon
5. check the pins


### NOTE: sa TEST folder nandun lahat ng mga sensor na pang test kung gumagana ba o hindi


### Paano mag add ng user sa TG ?

1. message ka muna sa "@rtutrybot"
2. click moto  https://api.telegram.org/bot6038531962:AAHmGRmFAXfSezff24artpEu7Ty5DOCqXtQ/getUpdates  
hanapin mo yung message na sinend mo tas hanapin mo yung "id" : "copy mo yung ID number"
3. punta ka sa mga sumusunod :  
    - templates/index.html  line 78
    - templates/facial-login.html  line 41
    - templates/finger-login.html  line 28
    - templates/surveilance.html  line 140
4. sa code mag add ka ng new chat_id tapos paste mo yung na copy mong chat number  
example: 
```shell
      const chat_id1 = 1509744956;
      const chat_id2 = 1102282141;
      const chat_id3 = 1240058920;
      const chat_id4 = 1282718818;
      const chat_id5 = "paste mo dito yung number pre"; // new TG user    
      var IDs = [
                 chat_id1,
                 chat_id2,
                 chat_id3,
                 chat_id4
                 ,const chat_id5 = "paste mo dito yung number pre"; // new TG user  
                ];
```
NOTE: wag kalimutan ang coma " , " , yung var IDs ay naka array

### Paano palitan ang background picture o iedit ?

punta ka sa "static/css/main.css" at line 238

- uncomment molang yung line 230 to 236  
- tapos upload ka ng bagong picture for example: "test.jpg"  
- upload molang sa "static/css/images"  
- sa code naman palitan molang yung route  
for example:

old code
```shell
		background: #0f2833 url("images/bgee.png") bottom left;  //palitan mo yung bgee.png to test.jpg
		background-repeat: repeat-x;
		height: 100%;
		left: 0;
		opacity: 1;
		position: fixed;
		top: 0;

pang background color to
        // comment molang to
		/* background: #348cb2 bottom left;
		background-repeat: repeat-x;
		height: 100%;
		left: 0;
		opacity: 1;
		position: fixed;
		top: 0; */
```

new code
```shell
		background: #0f2833 url("images/test.jpg") bottom left;  //napalitan na
		background-repeat: repeat-x;
		height: 100%;
		left: 0;
		opacity: 1;
		position: fixed;
		top: 0;

pang background color to
        // comment molang to
		/* background: #348cb2 bottom left;
		background-repeat: repeat-x;
		height: 100%;
		left: 0;
		opacity: 1;
		position: fixed;
		top: 0; */
```



### kapag mag aalis ng registered people

1. delete mo lang yung folder ng registered people
2. tas punta ka sa "Facerecognition/Face_Recognition.py" tas scroll down pinaka baba
3. line 134 uncomment mo tas run mo yung script after mag run,  
   kapag goods naman icomment mo ule

example:
old
```shell
# uncomment or tanggal # lang
# print(Face_Recognition().Face_Train())

```
new
```shell
# uncomment or tanggal # lang
print(Face_Recognition().Face_Train())

kapag goods naman, icomment mo ule
# print(Face_Recognition().Face_Train())

```

## install requirements packages

locate mo muna via Terminal ang 'requirements.txt'

```shell
pip install -r requirements.txt
```

Note: sana maging okay sa installation
