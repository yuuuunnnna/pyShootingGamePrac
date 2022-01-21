import pygame #cmd창에서 pip install pygame해서 설치해줬당
import sys
import random
from time import sleep



padWidth = 480
padHeight = 640
rockImage = ['rock01.png','rock02.png','rock03.png','rock04.png','rock05.png',\
             'rock06.png','rock07.png','rock08.png','rock09.png','rock10.png',\
             'rock11.png','rock12.png','rock13.png','rock14.png','rock15.png',\
             'rock16.png','rock17.png','rock18.png','rock19.png','rock20.png',\
             'rock21.png','rock22.png','rock23.png','rock24.png','rock25.png',\
             'rock26.png','rock27.png','rock28.png','rock29.png','rock30.png']
            

explosionSound = ['explosion01.wav','explosion02.wav','explosion03.wav','explosion04.wav']


#게임에 등장하는 객체 드로잉
def drawObject(obj,x,y):
    global gamePad
    gamePad.blit(obj,(x,y))


#운석 맞춘 개수 계산
def writeScore(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf',20)
    text = font.render('파괴한 운석 수: ' + str(count),True,(255,255,255))
    gamePad.blit(text,(10,0))
    

#운석이 화면 아래로 떨어진 개수 
def writePassed(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf',20)
    text = font.render('놓친 운석: ' + str(count),True,(255,0,0))
    gamePad.blit(text,(350,0))
    

#게임메세지 출력 
def writeMessage(text):
    global gamePad,gameoverSoumd
    textfont = pygame.font.Font('NanumGothic.ttf',60)
    text = textfont.render(text,True,(255,0,0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text,textpos) #화면에 출력 
    pygame.display.update()
    pygame.mixer.music.stop()
    gameoverSound.play()
    sleep(2)
    pygame.mixer.music.play(-1)
    runGame()

#충돌시 메시지 
def crash():
    global gamePad
    writeMessage('전투기파괴!')

#게임오버메시지
def gameOver():
    global gamePad
    writeMessage('게임오버!')





def initGame():
    global gamePad, clock,background ,fighter, missile, explosion, missileSound, gameoverSound
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth,padHeight)) #게임 화면 크기 
    pygame.display.set_caption('PyShooting') #게임이름
    background = pygame.image.load('background.png') #배경그림
    fighter = pygame.image.load('fighter.png')#전투기 그림
    missile = pygame.image.load('missile.png') #미사일 그림
    explosion = pygame.image.load('explosion.png')#폭발그림
    pygame.mixer.music.load('music.wav')
    pygame.mixer.music.play(-1)
    missileSound = pygame.mixer.Sound('missile.wav')
    gameOverSound = pygame.mixer.Sound('gameover.wav')

    clock = pygame.time.Clock()


def runGame():
    
    global gamdPad, clock, background, fighter, missile, explosion, missileSound, gameoverSound


    
    #전투기 크기
    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    #전투기 초기 위치(x,y)
    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0

    #무기좌표 리스트
    missileXY = []

    #운석 랜덤생성
    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size #운석크기
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    destroySound = pygame.mixer.Sound(random.choice(explosionSound))

    #운석초기위치설정
    rockX = random.randrange(0, padWidth - rockWidth) 
    rockY = 0 #꼭대기
    rockSpeed = 2


    #전투기 미사일에 운석이 맞았을 때 true
    isShot = False
    shotCount = 0
    rockPassed = 0
    

    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]: #게임프로그램 종료
                pygame.quit()
                sys.exit()
            
            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT: #전투기 왼쪽으로 이동 
                    fighterX -=5
                    
                elif event.key == pygame.K_RIGHT: #전투기 오른쪽 이동
                    fighterX +=5

                elif event.key == pygame.K_SPACE:
                    missileSound.play()
                    missileX = x + fighterWidth/2 #미사일을 비행기 중간에서 나가
                    missileY = y - fighterHeight
                    missileXY.append([missileX, missileY])

            if event.type in [pygame.KEYUP]: #방향키 뗄 때 멈춤
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0
                    

        drawObject(background,0,0) #배경화면그리기
            # 전투기 위치 재조
        x += fighterX
        if x<0:
            x = 0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth
                
        #전투기가 운석과 충돌했는지 체크
        if y < rockY + rockHeight:
            if(rockX > x and rockX < x + fighterWidth) or \
                (rockX + rockWidth > x and rockX + rockWidth < x + fighterWidth):
                crash()
            
        drawObject(fighter,x,y) #비행기 게임화면 좌표에 그리


        
        #미사일발사 화면에 그리기                        
        if len(missileXY) != 0:
            for i,bxy in enumerate(missileXY): #미사일 요소에 대해 반복
                bxy[1] -= 10 #총알 y좌표 -10(위로 이동)
                missileXY[i][1] = bxy[1]

                if bxy[1] < rockY: #미사일이 운석에 맞았을 때
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1
                        
            
                if bxy[1] <= 0: #미사일이 화면 밖 벗어나면
                    try:
                        missileXY.remove(bxy) #미사일 제거
                    except:
                        pass
                    
        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx, by)




        writeScore(shotCount) #운석 맞춘 점수 표시

        
        rockY += rockSpeed #운석 아래로 움직임



        #운석이 지구로 떨어진 경우
        
        if rockY > padHeight:
            rock = pygame.image.load(random.choice(rockImage))
            #운석 랜덤생성
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size #운석크기
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            #운석초기위치설정
            rockX = random.randrange(0, padWidth - rockWidth) 
            rockY = 0 #꼭대기
            rockPassed += 1 
            #rockSpeed = 2

        #운석 3개 놓치면 게임 오버 
        if rockPassed == 3:
            gameOver()

        #놓친 운석 수 표시
        writePassed(rockPassed)

        
        #운석 맞춘 경우
        if isShot:
            #운석폭발
            drawObject(explosion, rockX, rockY) #운석 폭발 그리기
            destroySound.play() #운석폭발 소리 
            rock = pygame.image.load(random.choice(rockImage))
            #운석 랜덤생성
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size #운석크기
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            #운석초기위치설정
            rockX = random.randrange(0, padWidth - rockWidth) 
            rockY = 0 #꼭대기
            destroySound = pygame.mixer.Sound(random.choice(explosionSound))
            #rockSpeed = 2
            isShot = False 


            #운석맞추면 속도 증가
            rockSpeed +=0.2
            if rockSpeed >= 10:
                rockSpeed = 10


        drawObject(rock, rockX, rockY)
                        
        pygame.display.update() #게임화면 다시그림

        clock.tick(60) #게임화면 초당 프레임 수 60으로 설정

    pygame.quit() #게임종료

initGame()
runGame()
    
