import spidev
import time


spi = spidev.SpiDev() # create spi object connecting to /dev/spidev0.1
spi.open(0x00,1)
spi.max_speed_hz = 250000 # set speed to 250 Khz
spi.mode = 0b00

smallDelay = 0.01

try:

    data = spi.xfer2([0x40,0x0A,0x3c]) # Set IOCON bank=0, mirror=0, seqop=1, disslw=1,haen=1,odr=0,intpol=0
    time.sleep(smallDelay) # sleep for smallDelay seconds
    data = spi.xfer2([0x40,0x00,0x00]) #Set IODIRA to outputs
    time.sleep(smallDelay)
    data = spi.xfer2([0x40,0x01,0x00]) #Set IODIRB to outputs
    time.sleep(smallDelay)

    data = spi.xfer2([0x41,0x01,0x00]) #read back IOCON
    print("IOCON read back as: ",hex(data[2])," ",bin(data[2]))
    print("this should have read back 0x3c")
    time.sleep(smallDelay)

    data = spi.xfer2([0x40,0x12,0xff]) #Set all pins on port A to high
    time.sleep(smallDelay)
    data = spi.xfer2([0x41,0x12,0x00]) #read back port A
    print("read back from port A after set to high: ", hex(data[2]))
    
    time.sleep(2)
    data = spi.xfer2([0x40,0x12,0x00]) # Set all pins on port A to low
    time.sleep(smallDelay)
    data = spi.xfer2([0x41,0x12,0x00]) # read back on all pins on port A.
    print("read back from port A after set to low: ", hex(data[2]))


finally:
    spi.close() # always close the port before exit

