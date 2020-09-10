#define LEDs_ADDR 0x80001010
#define SWs_ADDR 0x80001012

#define READ_GPIO(dir) (*(volatile unsigned *)dir)
#define WRITE_GPIO(dir,value) { (*(volatile unsigned *)dir) = (value); }

int main ( void )
{
    while (1) { 
        WRITE_GPIO(LEDs_ADDR,READ_GPIO(SWs_ADDR));
    }
    return(0);
}