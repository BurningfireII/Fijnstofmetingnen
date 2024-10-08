from ds3231 import DS3231
import sps30
import time
import machine as mc
print(__name__)

def toggs():
    """
    this is a function that toggles the onboard led to show there is activity  
    """
    for i in range(10):
        led.toggle()
        time.sleep(0.1)
        led.toggle()
        time.sleep(0.1)
    time.sleep(1)

if __name__ == "__main__":
    # defines pins for sps30
    time.sleep(1)
    led = mc.Pin(25, mc.Pin.OUT)
    sda = mc.Pin(0)
    scl = mc.Pin(1)
    i2c = mc.I2C(0, sda=sda, scl=scl, freq=100000)
    
    toggs()
    # defines pins for SPS30, ground the select pin for I2C
    DSsda = mc.Pin(18)
    DSscl = mc.Pin(19)
    DSi2c = mc.I2C(1, sda=DSsda, scl=DSscl)

    toggs()
    
    sps = sps30.SPS30(i2c, print_output=True)
    sps.start_measurement()
    time.sleep(3)
    
    toggs()
    
    ds = DS3231(DSi2c)
    #dt = (2024, 6, 5, 13, 56, 55)
    #ds.datetime(dt)

    
    sps.clean_fan()
    time.sleep(10)
    
    toggs()
    
    current_time = [0, 0, 0, 0, 0]
    run = True
    
    while run:
        # measurment loop
        toggs()
            
        time.sleep(5)
        try:
            sps.read_data() # read data
            print(sps.last_measurement)
            f = open("measurements.txt","a") # open file
            length = len(sps.last_measurement)-1

            # formats data
            for index, i in enumerate(sps.last_measurement):
                if index == length:
                    string = (str(i)+";")
                else:    
                    string = (str(i)+",")
                f.write(string) # writes data
            f.write("\n") 
            f.close()
            
            t = open("time.txt","a")
            old_time = current_time[1]
            current_time[0] = ds.datetime()[1]
            current_time[1] = ds.datetime()[2]
            current_time[2:5] = ds.datetime()[4:7]
            length = 4
            
            # loop to format time
            for index, i in enumerate(current_time):
                if index == length:
                    string = (str(i)+";")
                else:    
                    string = (str(i)+",")
                t.write(string) # writes time 
            t.write("\n")
            t.close()
            if current_time[1] - old_time > 1: # determines if fan should be cleaned
                sps.clean_fan()
                time.sleep(10)
            print("good night")
            #mc.deepsleep(265*10**3) # sleep
            
        except KeyboardInterrupt:
            run = False
        
    
