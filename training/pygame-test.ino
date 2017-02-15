
// duration for output
int time = 1000;
// initial command
int command = 0;

void setup() {
  pinMode(13, OUTPUT);
  pinMode(10, OUTPUT);
  Serial.begin(115200); 
}

void loop() {

  reset();
    
  //receive command
  if (Serial.available() > 0){
    command = Serial.read();
  }
  else{
    command = 0;
  }
   send_command(command);
}


void up(){
  digitalWrite(13, HIGH);
  delay(100);
}

void down(){
  digitalWrite(10, HIGH);
  delay(100);
}


void reset(){
  digitalWrite(13, LOW);
  digitalWrite(10, LOW);
}

void send_command(int command){
  switch (command){

     //reset command
     case 0: reset(); break;

     // single command
     case 1: up(); break;
     case 2: down(); break;

     default: Serial.print("Invalid Command\n");
    }
}
