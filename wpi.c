  
#include <stdlib.h>
#include <stdio.h>
#include <wiringPi.h>
#include <unistd.h>

int main()
{
    wiringPiSetupGpio () ;
	pinMode (4, OUTPUT) ; //green
	digitalWrite (2,1); // initially on 
	pinMode (6, OUTPUT) ;//SPKR

    int i = 0;
    while(i<50){
        digitalWrite (6,1); // turn on spkr
        i++;
        usleep(300);
        digitalWrite (6,0); // shut off spkr
    }
    digitalWrite (6,0); // shut off 
	digitalWrite (2,0); // shut off 

   printf("done");
   return 0;
}