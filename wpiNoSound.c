  
#include <stdlib.h>
#include <stdio.h>
#include <wiringPi.h>
#include <unistd.h>

int main()
{
    wiringPiSetupGpio () ;
	pinMode (2, OUTPUT) ; //green
        pinMode (3, OUTPUT) ; //green
        pinMode (4, OUTPUT) ; //green
        pinMode (5, OUTPUT) ; //green
        digitalWrite (2,0); // initially off
        digitalWrite (3,0); // initially off
        digitalWrite (4,1); // initially on


	digitalWrite (5,0); // initially on 
	pinMode (6, OUTPUT) ;//SPKR
    int freq = 300;
    int i = 0;
    while(i<1000){
        // digitalWrite (6,1); // turn on spkr
        i++;
        usleep(freq);
        // digitalWrite (6,0); // shut off spkr
	usleep(freq);    
}
    // digitalWrite (6,0); // shut off 
	digitalWrite (4,0); // shut off 

   printf("done");
   return 0;
}
