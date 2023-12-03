import cv2
import serial
import time



class recogRobot:
    def __init__(self):
        self.arduino = serial.Serial('COM3', 9600, timeout=.1)#初始化串口连接
        self.cap =cv2.VideoCapture(0)#镜头开启
        self.degreeX=103#横向舵机5
        self.degreeY=103#纵向舵机9
        #45 y向下 x向右
        
        self.centerX=320#屏幕中心位置 310 330
        self.centerY=240#屏幕中心位置 230 250
        # self.facePosX=""#面部位置x
        # self.facePosY=""#面部位置y
        # self.para = []#xywh of face
        self.xml="./FaceRecogModel/haarcascade_frontalface_alt_tree.xml"
        

        # width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        # height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 输出分辨率
        # print(f"分辨率为 {width}x{height}")

    def streaming(self):#前台镜头开始捕捉
        while(True):
            ret,frame = self.cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_detector = cv2.CascadeClassifier(self.xml)
            self.faces = face_detector.detectMultiScale(gray, 1.1, -1)
            
            if len(self.faces)!=0:
            
                x, y, w, h =self.faces[0]
                print(self.degreeX,self.degreeY)
                xx=int(x+w//2)
                yy=int(y+h//2)
                cv2.circle(frame, (xx,yy), h, (0, 255, 0), 2)
                self.tracking(xx,yy)
                # time.sleep(1)    
            

            
            cv2.imshow("video", frame)
            
            
            c = cv2.waitKey(5)
            if c == 's':
                break

        self.cap.release()
        cv2.destroyAllWindows()
        
    def scaning(self):#没有人脸的时候开始横向旋转扫描
        
        while(len(self.faces)==0):
            self.degreeX=self.degreeX&180
            self.servoTrans(self.degreeX,103)
            self.degreeX += 10
        
        
        pass
    def tracking(self,xx,yy):#初现人脸的时候开始扫描,传入当前人脸坐标
        
        
        if xx<250:
            self.left()
        if xx>390:
            self.right()
        if yy<120:
            self.up()
        if yy>360:
            self.down()


    def servoTrans(self,x,y):
        
        self.arduino.write(bytes(str(x)+','+str(y),'utf-8'))
        cv2.waitKey(50)
        # self.arduino.write(bytes(str(self.degreeX)+','+str(self.degreeY),'utf-8'))

    def up(self):
        self.degreeY+=6
        self.degreeY%=180
        self.servoTrans(self.degreeX,self.degreeY)
        time.sleep(1)

    def down(self):
        self.degreeY-=6
        self.degreeY%=180
        self.servoTrans(self.degreeX,self.degreeY)
        time.sleep(1)

    def left(self):
        self.degreeX+=7
        self.degreeX%=180
        self.servoTrans(self.degreeX,self.degreeY)
        time.sleep(1)
    
    def right(self):
        self.degreeX-=7
        self.degreeX%=180
        self.servoTrans(self.degreeX,self.degreeY)
        time.sleep(1)



    


def run ():
    r = recogRobot()
    r.streaming()
    
    # i=30
    # while i<150:        
    #     r.servoTrans(i,i)
    #     i+=5

    #     time.sleep(1)

    # r.servoTrans(103,103)  
    


if __name__ == "__main__":
    run()
    
