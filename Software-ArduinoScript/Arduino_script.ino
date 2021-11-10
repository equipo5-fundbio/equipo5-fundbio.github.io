#include <SoftwareSerial.h>

//pin 10 como RX y 11 como TX
SoftwareSerial BT(10, 11);

char serial_input;
//Definición de pines de componentes
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
  BT.begin(19600);
}

void loop() {
  // Si hay un caracter disponible, leerlo y realizar una acción en base este
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
  // Determina el pin del sensor correspondiente
  sensor = determinar_sensor(num_sensor);
  
  // 100 veces toma la medida del sensor y la envía en forma de string
  for (i=0;i<100;i++){
    BT.write(String(analogRead(sensor)));
    // cada 0.6 segundos -> 1 minuto
    delay(600);
  }
  // Confirmar que las mediciones se han completado
  BT.write("Done")
}

void activar_bomba(int num_bomba){
  // Valores de presión se inicializan por seguridad
  int presion_i, presion_o = 0, presion_max = 1023;
  int sensor = determinar_sensor(num_bomba);
  String presion_str = "";
  String nuevo_c;
  
  // Mientras hayan caracteres disponibles, se leen y se van sumando en
  // una cadena de texto que representará la presión enviada
  while (BT.available() > 0){
    nuevo_c = String(BT.read());
    presion_str = String(presion_str + nuevo_c);
  }
  // Si se ha recibido la presión, se convierte a número entero
  // y se define como la presión máxima
  if (presion_str != ""){
    presion_i = presion_str.toInt();
    presion_max = presion_i;
    //Encendido de la bomba
    digitalWrite(num_bomba + 1, HIGH);
    
    //Leer la presión cada 0.1 segundos y enviarla
    do{
      presion_o = analogRead(sensor);
      BT.write(String(presion_o));
      // Si llega un caracter se rompe el bucle
      if (BT.available() > 0){
        break;
      }
      delay(100);
      // Ejecutar hasta que se alcance la presión que se indicó
    }while(presion_o < presion_max);
    
    // Apagar la bomba
    digitalWrite(num_bomba + 1, LOW);
    // Confimar que el proceso ha terminado
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
