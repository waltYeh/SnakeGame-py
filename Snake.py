from graphics import *
from button import Button
import random
import time
class Food:
	def __init__(self,win,xPos,yPos):
		self.w=win
		self.x=xPos
		self.y=yPos
		self.food=Circle(Point(self.x,self.y),0.5)
		self.food.setFill("green3")
		self.food.draw(self.w)
	def Reposition(self,xPos,yPos):
		dx=xPos-self.x
		dy=yPos-self.y		
		self.x=xPos
		self.y=yPos
		self.food.move(dx,dy)
	def getPos(self):
		return self.x, self.y
	def Clear(self):
		self.food.undraw()
	def FoodPosGenerate(self,snake,wall):
		i=0
		while 1:
			rdm_x=random.randint(1,19)
			rdm_y=random.randint(1,19)
			if rdm_x!=self.x or rdm_y!=self.y:#not at the same position
				if snake.FoodInterf(rdm_x,rdm_y) and wall.FoodInterf(rdm_x,rdm_y):
				#not at where snake is, and not where wall is
					break
			i+=1
			if i>30:
				return -1,-1
		return rdm_x,rdm_y
class Snake:
	def __init__(self,win,xPos,yPos,length):
		self.w=win
		self.x=xPos
		self.y=yPos
		self.h=3	#1 rightward, 2 upward, 3 leftward, 4 downward
		self.l=length
		self.q=[]	#stores coord of each node
		self.shape=[]	#stores the shape of nodes to be drawn
		for i in range(length):
			self.q.append([xPos+i,yPos])
			self.shape.append(Rectangle(Point(xPos+i-0.5,yPos-0.5)\
				,Point(xPos+i+0.5,yPos+0.5)))
			self.shape[i].setOutline("green")
			self.shape[i].setFill("green")
			self.shape[i].draw(win)
	def getLocations(self):
		return self.x,self.y
	def getHead(self):
		ret=self.h
	def Move_Eat(self,m_e):
		if m_e==0:#move, pop last node, if eat, no poping
			self.q.pop()
			self.shape[-1].undraw()
			self.shape.pop()
		else:
			self.l+=1
		if self.h==1:
			dx=1
			dy=0
			self.x+=1
		elif self.h==2:
			dy=1
			dx=0
			self.y+=1
		elif self.h==3:
			dx=-1
			dy=0
			self.x-=1
		elif self.h==4:
			dy=-1
			dx=0
			self.y-=1
		self.x,self.y=self.Check_xy_Add_q(dx,dy)
		newshape=Rectangle(Point(self.x-0.5,self.y-0.5)\
			,Point(self.x+0.5,self.y+0.5))
		newshape.setOutline("green")
		newshape.setFill("green")
		newshape.draw(self.w)
		self.shape.insert(0,newshape)
	def Turn(self,newHeading):
		self.h=newHeading
	def CheckSelfEat(self):
		xHead=self.q[0][0]
		yHead=self.q[0][1]
		try:
			self.q[1:].index([xHead,yHead])
			return 1#self eat
		except:
			return 0#safe
	def Clear(self):
		for i in range(self.l):
			self.shape[i].undraw()
	def FoodInterf(self,fd_x,fd_y):#return 1 when food not at where snake is
		try:
			self.q[:].index([fd_x,fd_y])
			return 0
		except:
			return 1
	def Check_xy_Add_q(self,dx,dy):
		if self.x==0:
			newq=[19,self.y]
			self.q.insert(0,newq)
			return 19,self.y
		elif self.x==20:
			newq=[1,self.y]
			self.q.insert(0,newq)
			return 1,self.y
		elif self.y==0:
			newq=[self.x,19]
			self.q.insert(0,newq)
			return self.x,19
		elif self.y==20:
			newq=[self.x,1]
			self.q.insert(0,newq)
			return self.x,1
		else:
			newq=[self.q[0][0]+dx,self.q[0][1]+dy]
			self.q.insert(0,newq)
			return self.x,self.y
	def CheckIntoWall(self,wall):
		if wall.linelist[self.y-1][self.x-1]=="1":
			return 1
		else:
			return 0
	def Flash(self):
		for i in range(self.l):
			self.shape[i].undraw()
		time.sleep(0.5)
		for i in range(self.l):
			self.shape[i].draw(self.w)
		time.sleep(0.5)
		for i in range(self.l):
			self.shape[i].undraw()
		time.sleep(0.5)
		for i in range(self.l):
			self.shape[i].draw(self.w)
		time.sleep(0.5)
class Wall:
	def __init__(self,win,file):
		self.w=win
		self.linelist=[]
		self.WallPos=[]
		self.WallBlocks=[]
		f=open(file,"r")
		for i in range(19):
			linestr=f.readline()
			self.linelist.append(linestr.split())		
		for i in range(19):
			roll=self.linelist[18-i]
			for j in range(19):
				item=roll[j]
				if item=="1":
					self.WallPos.append([j+1,i+1])
					self.WallBlocks.append(Rectangle(Point(j+1-0.5,(i+1-0.5)),Point(j+1+0.5,(i+1+0.5))))
					self.WallBlocks[-1].setOutline("red")
					self.WallBlocks[-1].setFill("yellow")
					self.WallBlocks[-1].draw(win)
	def FoodInterf(self,fd_x,fd_y):
		try:
			self.WallPos[:].index([fd_x,fd_y])
			return 0
		except:
			return 1	
	def Clear(self):
		for i in range(len(self.WallBlocks)):
			self.WallBlocks[i].undraw()			
def Click2Turn(clk_x,clk_y,head,snk_x,snk_y):
	if head==1 or head==3:
		if clk_y>snk_y:
			newhead=2
		else:
			newhead=4
	else:
		if clk_x>snk_x:
			newhead=1
		else:
			newhead=3
	return newhead
def CheckFoodEat(snk_x,snk_y,h,fd_x,fd_y):
	if h==1 and (fd_x==snk_x+1 or fd_x==snk_x-18) and fd_y==snk_y:
		return 1
	if h==2 and fd_x==snk_x and (fd_y==snk_y+1 or fd_y==snk_y-18):
		return 1
	if h==3 and (fd_x==snk_x-1 or fd_x==snk_x+18) and fd_y==snk_y:
		return 1
	if h==4 and fd_x==snk_x and (fd_y==snk_y-1 or fd_y==snk_y+18):
		return 1
	return 0
def GameOver(snake,food,Bt,w):
	snake.Flash()
	snake.Clear()
	food.Clear()
	Bt.label.undraw()
	Bt.label=Text(Point(14.0,-2.0),"Start")
	Bt.label.draw(w)
	Bt.deactivate()
def main():
	win=GraphWin("Snake", 500,600)
	win.setCoords(0.0,-4.0,20.0,20.0)
	playGround=Rectangle(Point(0.0,0.0),Point(20.0,20.0))
	playGround.setFill("black")
	playGround.draw(win)
	BtQuite=Button(win, Point(18.0,-2.0), 3.0, 3.0, "Quite")
	BtQuite.activate()
	BtStart=Button(win, Point(14.0,-2.0), 3.0, 3.0, "Start")
	BtPause=Button(win, Point(10.0,-2.0), 3.0, 3.0, "Pause")
	BtWall1=Button(win, Point(4,-3), 1, 1, "1")
	BtWall2=Button(win, Point(5.2,-3), 1, 1, "2")
	BtWall3=Button(win, Point(6.4,-3), 1, 1, "3")
	InpLevel=Entry(Point(3,-1.3),2)
	InpLevel.setText("1")
	InpLevel.draw(win)
	Text(Point(5,-1.3),"Score:").draw(win)
	Text(Point(1.2,-1),"Level:").draw(win)
	Text(Point(1.2,-1.6),"(1~5)").draw(win)
	Text(Point(2,-3),"Map:").draw(win)
	score=0.0
	ScoreCounter=Text(Point(7,-1.3),score)
	ScoreCounter.draw(win)
	Wall1=Wall(win,"Wall1.txt")
	wall=1
#main loop
	while True:
		BtStart.activate()
		BtPause.deactivate()
		BtWall1.activate()
		BtWall2.activate()
		BtWall3.activate()
#Preparation loop
		while True:
			q=win.getMouse()
			if BtQuite.clicked(q):
				break
			if BtWall1.clicked(q):
				Wall1.Clear()
				Wall1=Wall(win,"Wall1.txt")
				wall=1
			if BtWall2.clicked(q):
				Wall1.Clear()
				Wall1=Wall(win,"Wall2.txt")
				wall=2
			if BtWall3.clicked(q):
				Wall1.Clear()
				Wall1=Wall(win,"Wall3.txt")
				wall=3
			elif BtStart.clicked(q):
				try:
					Level=eval(InpLevel.getText())
					[1,2,3,4,5].index(Level)
					break
				except:
					continue
#end of Preparation
		score=0.0
		ScoreCounter.setText(score)
		if BtQuite.clicked(q):
			break
		BtStart.label.undraw()
		BtStart.label=Text(Point(14.0,-2.0),"Stop")
		BtStart.label.draw(win)
		BtPause.label.undraw()
		BtPause.label=Text(Point(10.0,-2.0),"Pause")
		BtPause.label.draw(win)
		BtPause.activate()
		if wall==1:
			Food1=Food(win,5,10)
			Snake1=Snake(win,10,10,6)
		elif wall==2:
			Food1=Food(win,11,11)
			Snake1=Snake(win,15,11,6)
		elif wall==3:
			Food1=Food(win,10,10)
			Snake1=Snake(win,15,10,6)
		paused=0
		BtWall1.deactivate()
		BtWall2.deactivate()
		BtWall3.deactivate()
#Game loop	
		while True:			
			time.sleep(-0.2*Level+1.2)
			q=win.checkMouse()
			if q!=None:
				if BtQuite.clicked(q):
					break
				elif BtStart.clicked(q):#stop
					Snake1.Clear()
					Food1.Clear()
					BtStart.label.undraw()
					BtStart.label=Text(Point(14.0,-2.0),"Start")
					BtStart.label.draw(win)
					BtStart.deactivate()
					break
				elif BtPause.clicked(q):
					if paused==0:#pause
						BtPause.label.undraw()
						BtPause.label=Text(Point(10.0,-2.0),"Resume")
						BtPause.label.draw(win)
						paused=1
					else:#resume
						BtPause.label.undraw()
						BtPause.label=Text(Point(10.0,-2.0),"Pause")
						BtPause.label.draw(win)
						paused=0
				elif q.getX()>=0 and q.getY()>=0 and paused==0:
					Snake1.Turn(Click2Turn(q.getX(),q.getY(),Snake1.h,Snake1.x,Snake1.y))
			if paused==0:
				eat=CheckFoodEat(Snake1.x,Snake1.y,Snake1.h,Food1.x,Food1.y)				
				if eat:
					score+=(Level*0.5+0.5)*eat
					ScoreCounter.setText(score)
					NewFd_x,NewFd_y=Food1.FoodPosGenerate(Snake1,Wall1)
					Food1.Reposition(NewFd_x,NewFd_y)
				Snake1.Move_Eat(eat)
				if Snake1.CheckSelfEat():
					GameOver(Snake1,Food1,BtStart,win)
					break
				if Snake1.CheckIntoWall(Wall1):
					GameOver(Snake1,Food1,BtStart,win)
					break
#end of Game loop
		try:
			if BtQuite.clicked(q):
				break
		except:
			pass
#end of main loop
	win.close()
main()