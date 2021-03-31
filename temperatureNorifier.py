from pigpio_dht import DHT22
import pigpio
from notificationHandler import NotificationHandler

PUSHBULLET_KEY = 'YOUR PUSHBULLET API KEY'

def didReceiveCommand(command):
    print("did receive command")
    global notificationHandler
    global sensor
    if command == '@temperature':
        result = sensor.read()
        if result['valid']:
            out = "Temperature = {0:0.1f} C  Humidity = {1:0.1f}%".format(result['temp_c'], result['humidity'])
        else:
            out = "Please try again! The data read from sensor was invalid!"
    else:
        out = "Invalid command! Please type '@temperature' in order to get information about temperature and humidity!"
    pushData = {'type': 'TEXT_MESSAGE', 'text': out}
    notificationHandler.pushToMobile(pushData)


notificationHandler = NotificationHandler(PUSHBULLET_KEY, didReceiveCommand)
pushData = {'type': 'TEXT_MESSAGE', 'text': 'TemperatureNotifier app starts !'}
notificationHandler.pushToMobile(pushData)

gpio = 4 # BCM Numbering
pi = pigpio.pi()
sensor = DHT22(gpio, timeout_secs=10, pi=pi)
