#include <SoftwareSerial.h>

SoftwareSerial BT(10, 11);

char serial_input;
int BOMBA1 = 2, BOMBA2 = 3, BOMBA3 = 4;
int SENSOR1 = A0, SENSOR2 = A1, SENSOR3 = A2;


void leer_datos_sensor(int );
void activar_bomba(int );
int determinar_sensor(int );

void setup() {
  pinMode(BOMBA1, OUTPUT);
  pinMode(BOMBA2, OUTPUT);
  pinMode(BOMBA3, OUTPUT);
  pinMode(SENSOR1, INPUT);
  pinMode(SENSOR2, INPUT);
  pinMode(SENSOR3, INPUT);
  BT.begin(38400);
}

void loop() {
  if(BT.available() > 0){
    serial_input = BT.read();
    switch(serial_input){
      case 'a':
        leer_datos_sensor(1);
        break;
      case 'b':
        leer_datos_sensor(2);
        break;
      case 'c':
        leer_datos_sensor(3);
        break;
      case 'd':
        activar_bomba(1);
        break;
      case 'e':
        activar_bomba(2);
        break;
      case 'f':
        activar_bomba(3);
        break;
      default:
        break;
    }
  }
  delay(1000);
}

void leer_datos_sensor(int num_sensor){
  int sensor, i;
  sensor = determinar_sensor(num_sensor);
  
  for (i=0;i<100;i++){
    BT.write(String(analogRead(sensor)));
    delay(600);
  }
  BT.write("Done")
}

void activar_bomba(int num_bomba){
  int presion_i, presion_o = 0, presion_max = 1023;
  int sensor = determinar_sensor(num_bomba);
  String presion_str = "";
  String nuevo_c;
  
  while (BT.available() > 0){
    nuevo_c = String(BT.read());
    presion_str = String(presion_str + nuevo_c);
  }
  
  if (presion_str != ""){
    presion_i = presion_str.toInt();
    presion_max = presion_i;
    digitalWrite(num_bomba + 1, HIGH);
    
    do{
      presion_o = analogRead(sensor);
      BT.write(String(presion_o));
      if (BT.available() > 0){
        break;
      }
      delay(100);
    }while(presion_o < presion_max);
    
    digitalWrite(num_bomba + 1, LOW);
    BT.write("Done");
  }
}

int determinar_sensor(int num_sensor){
  if (num_bomba == 1){
    return SENSOR1;
  }
  else if (num_bomba == 2){
    return SENSOR2;
  }
  else{
    return SENSOR3;
  }
}
