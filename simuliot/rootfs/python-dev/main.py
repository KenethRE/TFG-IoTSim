#!/usr/bin/python3
from time import sleep
import temp

def hello():
    sleep(1)
    print("Hello World!")

def main():
    number = temp.tempProbe()
    print ("The temperature is: " + str(number))


if __name__ == "__main__":
    main()