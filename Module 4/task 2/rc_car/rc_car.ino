
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <Stepper.h>
#include <ESP32Servo.h>

// ------------       BLE stuff -----------
BLEServer *pServer = NULL;
BLECharacteristic * pTxCharacteristic;
bool deviceConnected = false;
bool oldDeviceConnected = false;
uint8_t txValue = 0;

// See the following for generating UUIDs:
// https://www.uuidgenerator.net/
#define SERVICE_UUID           "6E400001-B5A3-F393-E0A9-E50E24DCCA9E" // UART service UUID
#define CHARACTERISTIC_UUID_RX "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
#define CHARACTERISTIC_UUID_TX "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

// --------------- Motor & Servo Stuff ----------------
int speed = 15; //    SPEED IN RPM OF MOTOR
Servo myservo;  // create servo object to control a servo
int pos = 0;    // variable to store the servo position
int servoPin = 12;
const int stepsPerRevolution = 2048;  // change this to fit the number of steps per revolution
// ULN2003 Motor Driver Pins
#define IN1 17 //19
#define IN2 5 //18
#define IN3 18 //5
#define IN4 19 //17
// initialize the stepper library
Stepper myStepper(stepsPerRevolution, IN1, IN3, IN2, IN4);

class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
    };

    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
    }
};

//class for doing things with received values!
class MyCallbacks: public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic *pCharacteristic) {
      // std::string buffer = pCharacteristic->getValue();
      // this was a pain. had to switch from getValue to getData
      //issue with getData giving pre-formatted into characterstic values, didn't work for floats
      uint8_t* buffer = pCharacteristic->getData();
      if ((char)buffer[0] == '!') {  //Sensor data flag
          Serial.println("Magnetometer Data:");
          float x = *( (float*)(buffer + 2) );
          Serial.print("x = ");
          Serial.println(x, 7);
          float y = *( (float*)(buffer + 6) );
          Serial.print("y = ");
          Serial.println(y, 7);
          float z = *( (float*)(buffer + 10) );
          Serial.print("z = ");
          Serial.println(z, 7); 
        Serial.println("");
      }
    }

};


void setup() {
  Serial.begin(115200);
  setupBLE();
  myStepper.setSpeed(speed);
  setupServo();

}

void loop() {
  //1 is 1/speed a second. so 1 loop per 1/15th a second = delay of 0.066 seconds
  //5 is 5/speed a second. so 1 loop per 1/3 a second = delay of 0.333 seconds
  // myStepper.step(5);

  //servo range 45. from 68 to 113
  // pos = ((pos + 1) % 45);
  // Serial.println(pos + 68);
  // myservo.write(int(pos + 68));
  // myservo.write(int(90));
  if (pos == 0){
    delay (1000);
  }
  delay(3000);

  // disconnecting
  if (!deviceConnected && oldDeviceConnected) {
      delay(500); // give the bluetooth stack the chance to get things ready
      pServer->startAdvertising(); // restart advertising
      Serial.println("start advertising");
      oldDeviceConnected = deviceConnected;
  }
  // connecting
  if (deviceConnected && !oldDeviceConnected) {
      oldDeviceConnected = deviceConnected;
  }
}

//all this was in setup - moving to own function
void setupBLE(){
  
  // Create the BLE Device
  BLEDevice::init("Car Thingy");

  // Create the BLE Server
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());

  // Create the BLE Service
  BLEService *pService = pServer->createService(SERVICE_UUID);

  // Create a BLE Characteristic
  pTxCharacteristic = pService->createCharacteristic(
										CHARACTERISTIC_UUID_TX,
										BLECharacteristic::PROPERTY_NOTIFY
									);
                      
  pTxCharacteristic->addDescriptor(new BLE2902());

  BLECharacteristic * pRxCharacteristic = pService->createCharacteristic(
											 CHARACTERISTIC_UUID_RX,
											BLECharacteristic::PROPERTY_WRITE
										);

  pRxCharacteristic->setCallbacks(new MyCallbacks());

  // Start the service
  pService->start();

  // Start advertising
  pServer->getAdvertising()->start();
  Serial.println("Waiting a client connection to notify...");
}

void setupServo(){
  //servo:
  // Allow allocation of all timers
	ESP32PWM::allocateTimer(0);
	ESP32PWM::allocateTimer(1);
	ESP32PWM::allocateTimer(2);
	ESP32PWM::allocateTimer(3);
	myservo.setPeriodHertz(50);    // standard 50 hz servo
	myservo.attach(servoPin, 0, 3500); // attaches the servo on pin 18 to the servo object
}


void printSensorDataXYZ(uint8_t *buffer) {

  float x = *( (float*)(buffer + 2) );
  Serial.print("x = ");
  Serial.println(x, 7);

  float y = *( (float*)(buffer + 6) );
  Serial.print("y = ");
  Serial.println(y, 7);

  float z = *( (float*)(buffer + 10) );
  Serial.print("z = ");
  Serial.println(z, 7); 

}

boolean checkCRC(uint8_t *buffer) {

  uint8_t len = sizeof(buffer);
  uint8_t crc = buffer[len-2];
  uint8_t sum = 0;

  for (int i = 0; i < (len-1); i++) {

    sum += buffer[i];

  }

  Serial.print("CRC ");

  if ((crc & ~sum) == 0) {
    Serial.println("PASS");
    return true;
  }

  else {
    Serial.println("FAIL");
    return false;
  }

}
//       ------ Sending packet stuff, I don't need but useful maybe later
// if (deviceConnected) {
//     Serial.printf("*** Sent Value: %d ***\n", txValue);
//     need to check if this is necessary to receive vales
//     pTxCharacteristic->setValue(&txValue, 1);
//     pTxCharacteristic->notify();
//     txValue++;
// delay(10); // bluetooth stack will go into congestion, if too many packets are sent
