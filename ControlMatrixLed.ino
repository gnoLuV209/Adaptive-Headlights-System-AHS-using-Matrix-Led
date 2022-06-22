#include "LedControl.h"
LedControl lc=LedControl(12,11,10,2);

int x;
byte module_left=0;
byte module_right=0;
// fill array for opening full
byte normal_mode[] =                             
{
B11111111,
B11111111,
B11111111,
B11111111,
B11111111,
B11111111,
B11111111,
B11111111
};
// fill array for 4 columns
byte area1_mode[] =                             
{
B00001111,
B00001111,
B00001111,
B00001111,
B00001111,
B11111111,
B11111111,
B11111111
};

byte area2_mode[] =                             
{
B11110000,
B11110000,
B11110000,
B11110000,
B11110000,
B11111111,
B11111111,
B11111111
};

byte area3_mode[] =                             
{
B00001111,
B00001111,
B00001111,
B00001111,
B00001111,
B11111111,
B11111111,
B11111111
};

byte area4_mode[] =                             
{
B11110000,
B11110000,
B11110000,
B11110000,
B11110000,
B11111111,
B11111111,
B11111111
};

void setup() {
Serial.begin (115200);
Serial.setTimeout(1);
//we deal with two MAX7219 modules, and we can power them on and set intensity independenty:
// the MAX72XX is in power-saving mode on startup,
// we have to do a wakeup call
lc.shutdown (0,false);
lc.shutdown (1,false);
// set the brightness to a medium values
lc.setIntensity (0,8);                       // 0 = low; 8 = high – first variable is module number i.e. module 0
lc.setIntensity (1,8);                       // 0 = low; 8 = high – first variable is module number i.e. module 1
// clear the displays
lc.clearDisplay (0);
lc.clearDisplay (1);
module_left  = 0;
module_right = 1;
}

void loop() {
x = Serial.readString().toInt();
if (x==0)
{
//lc.clearDisplay (0);
//lc.clearDisplay (1);
normal();
}
if (x==1)
{
lc.clearDisplay (0);
lc.clearDisplay (1);
area1();
delay(2000);
} 
if (x==2)
{
lc.clearDisplay (0);
lc.clearDisplay (1);
area2();
delay(2000);
} 
if (x==3)  
{   
lc.clearDisplay (0);
lc.clearDisplay (1);
area3(); 
delay(2000);

} 
if (x==4)  
{   
lc.clearDisplay (0);
lc.clearDisplay (1);
area4(); 
delay(2000);

}      
}



void normal()
{
for (int i = 0; i < 8; i++)
{
lc.setRow (0,i,normal_mode[i]);
lc.setRow (1,i,normal_mode[i]);
}
}

void area1()
{
for (int i = 0; i < 8; i++)
{
lc.setRow (0,i,area1_mode[i]);
lc.setRow (1,i,normal_mode[i]);
}
}
void area2()
{
for (int i = 0; i < 8; i++)
{
lc.setRow (0,i,area2_mode[i]);
lc.setRow (1,i,normal_mode[i]);
}
}

void area3()
{
for (int i = 0; i < 8; i++)
{
lc.setRow (1,i,area3_mode[i]);
lc.setRow (0,i,normal_mode[i]);
}
}

void area4()
{
for (int i = 0; i < 8; i++)
{
lc.setRow (1,i,area4_mode[i]);
lc.setRow (0,i,normal_mode[i]);
}
}


