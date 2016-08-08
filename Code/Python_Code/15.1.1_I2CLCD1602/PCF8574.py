########################################################################
# Filename    : PCF8574.py
# Description : PCF8574拓展GPIO
# Author      : freenove
# modification: 2016/06/26
########################################################################
import smbus
import time
class PCF8574_I2C(object):
	OUPUT = 0
	INPUT = 1
	
	def __init__(self,address):
		# Note you need to change the bus number to 0 if running on a revision 1 Raspberry Pi.
		self.bus = smbus.SMBus(1)
		self.address = address
		self.currentValue = 0
		
	def readByte(self):#读取所有PCF8574端口的数据，由于电路连接原因，返回值为上次的端口写入值，并不是真正的端口值
		#value = self.bus.read_byte(self.address)
		return self.currentValue#value
		
	def writeByte(self,value):#向PCF8574所有端口写数据
		self.currentValue = value
		self.bus.write_byte(self.address,value)

	def digitalRead(self,pin):#读PCF8574其中一个端口的数据
		value = readByte()	
		return (value&(1<<pin)==(1<<pin)) and 1 or 0
		
	def digitalWrite(self,pin,newvalue):#向PCF8574其中一个端口写数据
		value = self.currentValue #bus.read_byte(address)
		if(newvalue == 1):
			value |= (1<<pin)
		elif (newvalue == 0):
			value &= ~(1<<pin)
		self.writeByte(value)	

def loop():
	mcp = PCF8574_I2C(0x27)
	while True:
		#mcp.writeByte(0xff)
		mcp.digitalWrite(3,1)
		print 'Is 0xff? %x'%(mcp.readByte())
		time.sleep(1)
		mcp.writeByte(0x00)
		#mcp.digitalWrite(7,1)
		print 'Is 0x00? %x'%(mcp.readByte())
		time.sleep(1)
		
class PCF8574_GPIO(object):#函数接口标准化
	OUT = 0
	IN = 1
	BCM = 0
	BOARD = 0
	def __init__(self,address):
		self.chip = PCF8574_I2C(address)
		self.address = address
	def setmode(self,mode):#PCF8574的端口属于准双向IO，不需要设置输入输出模式
		pass
	def setup(self,pin,mode):
		pass
	def input(self,pin):#读取PCF8574一个端口的数据
		return self.chip.digitalRead(pin)
	def output(self,pin,value):#向PCF8574其中一个端口写数据
		self.chip.digitalWrite(pin,value)
		
def destroy():
	bus.close()
	
if __name__ == '__main__':
	print 'Program is starting ... '
	try:
		loop()
	except KeyboardInterrupt:
		destroy()
		
	
