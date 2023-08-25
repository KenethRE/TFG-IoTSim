#!/usr/bin/python3
from time import sleep
import tempDevice as temp

def hello():
    sleep(1)
    print("Hello World!")

def main():
    temperature = temp.tempDevice()
    number = temperature.contactProbe()
    print ("The temperature is: " + str(number))

if __name__ == "__main__":
    main()