from machine import Pin
import utime


def main():
    led = Pin(2, Pin.OUT)
    counter = 0
    on = True
    while True:
        counter += 1
        if counter % 25000 == 0:    # CPU benchmark value: 8266->25k, ESP32->120k
            if on:
                led.off()
            #     utime.sleep_ms(500)
            else:
                led.on()
            print(counter)
            on = not on


# must be temp_update.py

if __name__ == '__main__':
    main()
