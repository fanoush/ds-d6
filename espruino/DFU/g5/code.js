E.kickWatchdog();
function KickWd(){
  if( (typeof(BTN1)=='undefined')||(!BTN1.read()) ) E.kickWatchdog();
}
var wdint=setInterval(KickWd,2000);
E.enableWatchdog(20, false);

var bpp=4; // powers of two work
var g=Graphics.createArrayBuffer(454,454,bpp);
E.kickWatchdog();
/*
// MIT License (c) 2020 fanoush https://github.com/fanoush
// see full license text at https://choosealicense.com/licenses/mit/

var SPI3 = E.compiledC(`
// int cmd(int,int)
// int cmd4(int,int,int,int)
// void setpins(int,int,int,int)
// void setwin(int,int,int,int)
// int enable(int,int)
// void disable()
// void blit_setup(int,int,int,int)
// int blt_pal(int,int,int)

// not used
// int cmds(int,int)
// int data(int,int)
// void save()
// void restore()
// int fill_color(int,int)

// bpp 16,12 and 8 supported
#define LCD_BPP 8
// with SHARED_SPIFLASH we need to enable SPI only iniside native code and disable it before return
// to allow espruino to execute from SPI flash on shared SPI pins
#define SHARED_SPIFLASH
// also we may need to unselect flash chip CS pin as Espruino is in a middle of read command
//#define SPIFLASH_CS (1<<xx)

//SPI0 0x40003000
//SPI1 0x40004000
//SPI2 0x40023000
//SPI3 0x4002F000
#define SPIBASE 0x4002F000
#define SPI3

typedef unsigned int uint32_t;
typedef signed int int32_t;
typedef unsigned short uint16_t;
typedef unsigned char uint8_t;
typedef signed char int8_t;
#define NULL ((void*)0)
// if code is in RAM we can put global data into text/code segment
// this allows simpler pc-relative addressing and shorter/faster code
#define __code __attribute__((section(".text")))
//#define __code
// _code volatile uint32_t *SPI =(uint32_t*)SPIBASE;
// direct constant makes smaller/faster code
#define SPI ((volatile uint32_t*)SPIBASE)
//divide register offsets by sizeof(uint32_t)
#define REG(offset) (offset/4)
// SPI master documentation
// https://infocenter.nordicsemi.com/topic/com.nordic.infocenter.nrf52832.ps.v1.1/spi.html?cp=4_2_0_47
// common/nonDMA registers
#define READY REG(0x108)
#define INTENSET REG(0x304)
#define INTENCLR REG(0x308)
#define ENABLE REG(0x500)
#define PSELSCK REG(0x508)
#define PSELMOSI REG(0x50c)
#define PSELMISO REG(0x510)
#define PSELCSN REG(0x514)
#define CSNDUR REG(0x564)
#define CSNPOL REG(0x568)
#define PSELDCX REG(0x56c)
#define DCXCNT REG(0x570)
#define ERRT195 REG(4)
#define RXD REG(0x518)
#define TXD REG(0x51c)
#define FREQUENCY REG(0x524)
#define CONFIG REG(0x554)
/// EasyDMA registers
#define TASKS_START REG(0x010)
#define TASKS_STOP REG(0x014)
#define EVENTS_STOPPED REG(0x104)
#define EVENTS_ENDRX REG(0x110)
#define EVENTS_END REG(0x118)
#define EVENTS_ENDTX REG(0x120)
#define EVENTS_STARTED REG(0x14C)
#define SHORTS REG(0x200)
#define RXDPTR REG(0x534)
#define RXDMAXCNT REG(0x538)
#define RXDAMOUNT REG(0x53C)
#define RXDLIST REG(0x540)
#define TXDPTR REG(0x544)
#define TXDMAXCNT REG(0x548)
#define TXDAMOUNT REG(0x54C)
#define TXDLIST REG(0x550)
#define ORC  REG(0x5c0)
#define GPIO(x) ((volatile uint32_t*)(0x50000000+x))
#define OUT     GPIO(0x504)
#define OUTSET  GPIO(0x508)
#define OUTCLR  GPIO(0x50c)
//#define OUTSET1  GPIO(0x808)
//#define OUTCLR1  GPIO(0x80c)
#define IN     GPIO(0x510)
// direction 1=output
#define DIR     GPIO(0x514)
#define DIRSET     GPIO(0x518)
#define DIRCLR     GPIO(0x51c)

__code uint32_t pSCK= -1;
__code uint32_t pMOSI= -1;
//__code uint32_t pMISO= -1;
#define pMISO (-1)
__code uint32_t pCS= 0;
__code uint32_t pCD= 0; //command/data
// if not SPI3 we don't handle CS,CD pins >31
void setpins(int sck,int mosi,int cs,int cd){
  pSCK=sck;pMOSI=mosi;
#ifdef SPI3
  pCS=cs;
  pCD=cd;
#else
  pCS=1<<cs;
  pCD=1<<cd;
#endif
}
__code uint32_t savedintflags=0;
__code uint32_t savedmode=0;
void save(){
  savedintflags=SPI[INTENSET];
  savedmode=SPI[ENABLE];
}
void restore(){
  SPI[ENABLE]=0;
  SPI[INTENSET]=savedintflags;
  SPI[ENABLE]=savedmode;
}
// pins need to be already preconfigured as gpio input/outputs
int setup(uint32_t speed,uint32_t mode){
  if (pSCK>=0 && (pMISO>=0||pMOSI>=0)){
    uint32_t flags=SPI[INTENSET];
    if (flags) SPI[INTENCLR]=flags; // clear all interrupt flags
    SPI[PSELSCK]=pSCK;
    SPI[PSELMOSI]=pMOSI;
    SPI[PSELMISO]=pMISO;
#ifdef SPI3
    SPI[CSNPOL]= 0; //active low
    SPI[CSNDUR]= 1; //15.625ns
    SPI[PSELCSN]= pCS; //-1;
    SPI[PSELDCX]= pCD;
    //SPI[DCXCNT]=0;
#endif
    SPI[FREQUENCY]=speed<<24; // 0x80=8mbits,0x40=4mbits,...
    SPI[CONFIG]=mode<<1; //msb first
    return 1;
  }
  return 0;
}
void disable(){
  SPI[ENABLE]=0;
  SPI[READY]=0;
#ifdef SPI3
  SPI[ERRT195]=1; // Errata 195
#endif
  uint32_t flags=SPI[INTENSET];
  if (flags) SPI[INTENCLR]=flags; // clear all interrupt flags
}

int enable(uint32_t speed,uint32_t mode){
  if (SPI[ENABLE]) return -1;
  if (setup(speed,mode)){
#ifndef SHARED_SPIFLASH
    SPI[ENABLE]=7;//SPIM with DMA
    SPI[TASKS_STOP]=1;
#endif
    return 1;
  }
  return 0;
}

int write_dma(uint8_t *buffer, uint32_t len,int async);

void spi_cs_on(){
#ifdef SHARED_SPIFLASH
#ifdef SPIFLASH_CS
  *OUTSET = SPIFLASH_CS;
#endif
    SPI[ENABLE]=7;//SPIM with DMA
#endif
#ifndef SPI3
//if(pCS>0)
  *OUTCLR = pCS; // CHIP SELECT
#endif
}

void spi_cs_off(){
#ifndef SPI3
  //if(pCS>0)
  *OUTSET = pCS; // CHIP SELECT
#endif
#ifdef SHARED_SPIFLASH
  SPI[ENABLE]=0;//disable SPI
#ifdef SPI3
  SPI[ERRT195]=1; // Errata 195
#endif
#endif
}

void send(uint8_t *buffer, int len, int cmdlen){
#ifdef SPI3
// we can send cmd+data as one DMA transfer
  SPI[DCXCNT]=cmdlen;
  write_dma(buffer,len,0);
//    SPI[DCXCNT]=0;
#else
// toggle DC pin ourselves and send two transfers
  if (cmdlen){
    *OUTCLR = pCD; // CMD
    if(pCS>0) *OUTCLR = pCS; // CHIP SELECT
    write_dma(buffer,cmdlen,0);
    buffer+=cmdlen;len-=cmdlen;
  }
  *OUTSET = pCD; // data
  if (len>0)
    write_dma(buffer,len,0);
#endif
return;
}

int cmd_data(uint8_t *buffer, int len, int cmdlen){
  //if (pCD<=0) return -1;
  spi_cs_on();
  send(buffer,len,cmdlen);
  spi_cs_off();
  return 0;
}

int cmd(uint8_t *buffer, int len){
  return cmd_data(buffer,len,1);
}

int data(uint8_t *buffer, int len){
  return cmd_data(buffer,len,0);
}

int cmds(uint8_t *ptr,int bufflen){
  int cnt=0;
  if (!ptr || bufflen<=0) return cnt;
  //if (pCD<=0) return -1;
  spi_cs_on();
  uint8_t *endptr=ptr+bufflen;
  uint8_t len;
  while ((len=*ptr++)!=0){
    if ((ptr+len)>endptr) {cnt=-cnt;break;}// break if we would go past buffer
    send(ptr,len,1);
    ptr+=len;cnt++;
  }
  spi_cs_off();
  return cnt;
}
// send command with up to 3 parameters (espruino allows methods with up to 4 parameters)
int cmd4(int c0,int d1,int d2, int d3){
  int cnt=0;
  uint8_t buff[4];
  if (c0>=0)buff[cnt++]=c0; else return 0;
  if (d1>=0)buff[cnt++]=d1;
  if (d2>=0)buff[cnt++]=d2;
  if (d3>=0)buff[cnt++]=d3;
  cmd(buff,cnt);
  return cnt;
}
__code uint8_t c[15] =  {
    5, 0x2a, 0,0, 0,0,
    5, 0x2b, 0,0, 0,0,
    1, 0x2c,
  0 };

void setwin(uint16_t x1,uint16_t x2,uint16_t y1,uint16_t y2){
  c[3]=x1&255;c[2]=x1>>8; //0x2a params
  c[5]=x2&255;c[4]=x2>>8;
  c[9]=y1&255;c[8]=y1>>8; //0x2b params
  c[11]=y2&255;c[10]=y2>>8;
  cmds(c,sizeof(c));
}

__code uint16_t running=0;
void wait_dma(){
  if (running) {
    while (SPI[EVENTS_END] == 0); // wait for previous transfer
    SPI[EVENTS_END]=0;
    running=0;
  }
}
#ifdef LONG_WRITES
// len can be over 255 bytes, write in multiple blocks
int write_dma(uint8_t *ptr, uint32_t len, int async)
{
  wait_dma();
  int offset = 0;
//  SPI[RXDPTR]=0;
  SPI[RXDMAXCNT]=0;
  SPI[EVENTS_END]=0;
  do {
    SPI[TXDPTR]=(uint32_t)(ptr + offset);
    if (len < 0x100) {
      SPI[TXDMAXCNT]=len;
      len = 0;
    } else {
      SPI[TXDMAXCNT]=0xff;
      offset = offset + 0xff;
      len = len - 0xff;
    }
    SPI[TASKS_START]=1;
    if (async && len==0){
      running=1; // do not wait for last part
    } else {
        while (SPI[EVENTS_END] == 0);
        SPI[EVENTS_END]=0;
    }
  } while (len != 0);
  return 0;
}
#else
int write_dma(uint8_t *ptr, uint32_t len, int async)
{
  wait_dma();
//  SPI[RXDPTR]=0;
  SPI[RXDMAXCNT]=0;
  SPI[EVENTS_END]=0;
  SPI[TXDPTR]=(uint32_t)(ptr);
  SPI[TXDMAXCNT]=len;
  SPI[TASKS_START]=1;
    if (async){
      running=1; // do not wait for last part
    } else {
        while (SPI[EVENTS_END] == 0);
        SPI[EVENTS_END]=0;
    }
  return 0;
}

#endif
__code uint16_t blit_w=0; //dest width
__code uint16_t blit_h=0; // dest height
__code uint16_t blit_bpp=0; // source bpp
__code uint16_t blit_stride=0; // source line stride
void blit_setup(uint16_t w,uint16_t h,uint16_t bpp, uint16_t stride){
  blit_w=w;blit_h=h;blit_bpp=bpp;blit_stride=stride;
}
#define LCHUNK 96 //192 // 132 //96 //48 //36 // divisible by 3 and 2

#if LCD_BPP==8
//only 8 bit palette entry
typedef uint8_t palbuff_t;
#else
typedef uint16_t palbuff_t;
#endif

int blt_pal(uint8_t *buff,palbuff_t* palbuff,uint8_t xbitoff){
  uint8_t *pxbuff=buff;
  uint8_t bpp=blit_bpp;
  if (pxbuff==NULL || palbuff==NULL || bpp==0 || bpp>8) return -1;
  uint8_t mask=(1<<bpp)-1; //pixel bitmask
  uint8_t bpos=xbitoff; //position of first bit in source
  uint16_t val=(*pxbuff++)|((*pxbuff++)<<8);val>>=bpos; // we prefetch 8-16 bits
  uint16_t w=blit_w;
  uint16_t h=blit_h;
  uint8_t lbuff_1[LCHUNK];
  uint8_t lbuff_2[LCHUNK];
  uint8_t *lbuff=lbuff_1;
  int lbufpos=0;
  int lbuffnum=0;
  spi_cs_on();
#ifdef SPI3
  SPI[DCXCNT]=0;
#else
  *OUTSET = pCD; // data
#endif
  do {
    w=blit_w;
    do {
#if LCD_BPP==12
      // pixel 1
      uint16_t px1=palbuff[val&mask]; // get color
      val=val>>bpp;bpos+=bpp;
      //pixel 2
      uint16_t px2=palbuff[val&mask]; // get color
      val=val>>bpp;bpos+=bpp;
      if(bpos>=8){bpos-=8;val=val|(*pxbuff++)<<(8-bpos);} //less than 8 bits, prefetch another byte
      //put 2x 12bit pixels into buffer
      lbuff[lbufpos++]=px1>>4;
      lbuff[lbufpos++]=(px1<<4)|(px2>>8);
      lbuff[lbufpos++]=px2&255;
      w-=2;
#elif LCD_BPP==16
      // pixel 1
      uint16_t px1=palbuff[val&mask]; // get color
      val=val>>bpp;bpos+=bpp;
      if(bpos>=8){bpos-=8;val=val|(*pxbuff++)<<(8-bpos);} //less than 8 bits, prefetch another byte
      //put 16bit pixel into buffer
      lbuff[lbufpos++]=px1>>8;
      lbuff[lbufpos++]=px1&255;
      w--;
#elif LCD_BPP==8
      // pixel 1
      // get color from palette or as direct value if no palette
      uint8_t px1= (palbuff) ? palbuff[val&mask] : val&mask;
      val=val>>bpp;bpos+=bpp;
      if(bpos>=8){bpos-=8;val=val|(*pxbuff++)<<(8-bpos);} //less than 8 bits available, prefetch another byte
      //put 8bit pixel into buffer
      lbuff[lbufpos++]= px1 ; //(bpp==6) ? px1<<2 : px1 ; // 6bit shift to 8bit - DK08
      w--;
#elif LCD_BPP==6
      // send 4 packed 6bit pixels in 3 bytes
      uint8_t px[4];
      for (int i=0;i<4;i++){
        px[i] = (palbuff) ? palbuff[val&mask] : val&mask;
        val=val>>bpp;bpos+=bpp;
        if(bpos>=8){bpos-=8;val=val|(*pxbuff++)<<(8-bpos);} //less than 8 bits available, prefetch another byte
      }
      //pack into 3 bytes
      lbuff[lbufpos++]= px[0]<<2 | px[1]>>4;
      lbuff[lbufpos++]= px[1]<<4 | px[2]>>2;
      lbuff[lbufpos++]= px[2]<<6 | px[3];
      w-=4;
#endif
      if (lbufpos >= LCHUNK){
        // buffer full, start async draw and switch to other buffer
        write_dma(lbuff,lbufpos,1);
        lbuffnum=1-lbuffnum;
        lbuff = lbuffnum ? lbuff_2 : lbuff_1;
        lbufpos=0;
      }
    } while(w>0);
    buff+=blit_stride;
    pxbuff=buff;bpos=xbitoff;
    val=(*pxbuff++)|(*pxbuff++)<<8;val>>=bpos;//val=(*pxbuff++)>>bpos;
    h--;
  } while(h>0);
  // send the rest
  if (lbufpos>0){
    write_dma(lbuff,lbufpos,0);
  } else {
    wait_dma();
  }
  spi_cs_off();
  return 0;
}
#if 0
// write same buffer many times repeatedly
int write_many_dma(uint8_t *buffer, int len, int count){
  wait_dma();
  SPI[RXDPTR]=0;
  SPI[RXDMAXCNT]=0;
  SPI[EVENTS_END]=0;
  SPI[TXDPTR]=(uint32_t)(buffer);
  SPI[TXDMAXCNT]=len;
  if (count > 1)
    SPI[SHORTS]=1<<17;
  SPI[TASKS_START]=1;
  do {
    while (SPI[EVENTS_END] == 0); // wait
    SPI[EVENTS_END]=0;
    if (count <= 2) SPI[SHORTS]=0; // stop shortcut for next loop
  } while (--count);
return 0;
}
#if LCD_BPP==12
int fill_color(uint32_t val,uint32_t len){
  uint8_t buff[12]={ // 92ms for 24, 97ms for 12
//    val>>4,(val&0xf)<<4|val>>8,val&0xff,
//    val>>4,(val&0xf)<<4|val>>8,val&0xff,
//    val>>4,(val&0xf)<<4|val>>8,val&0xff,
//    val>>4,(val&0xf)<<4|val>>8,val&0xff,
    val>>4,(val&0xf)<<4|val>>8,val&0xff,
    val>>4,(val&0xf)<<4|val>>8,val&0xff,
    val>>4,(val&0xf)<<4|val>>8,val&0xff,
    val>>4,(val&0xf)<<4|val>>8,val&0xff
  };
  return write_many_dma(buff,12,len/8);
}
#elif LCD_BPP==16
int fill_color(uint32_t val,uint32_t  len){
  uint8_t buff[16]= { // 126ms for 16, 121ms for 32 bytes
//    val>>8,val&0xff, val>>8,val&0xff, val>>8,val&0xff, val>>8,val&0xff,
//    val>>8,val&0xff, val>>8,val&0xff, val>>8,val&0xff, val>>8,val&0xff,
    val>>8,val&0xff, val>>8,val&0xff, val>>8,val&0xff, val>>8,val&0xff,
    val>>8,val&0xff, val>>8,val&0xff, val>>8,val&0xff, val>>8,val&0xff
  };
  return write_many_dma(buff,16,len/8);
}
#elif LCD_BPP==8
int fill_color(uint32_t val,uint32_t len){
  uint8_t v=val&0xff;
  uint8_t buff[16]= { // 126ms for 16, 121ms for 32 bytes
    v, v, v, v,
    v, v, v, v,
    v, v, v, v,
    v, v, v, v
  };
  return write_many_dma(buff,16,len/16);
}
#endif
#endif
`);
*/
///*
// MIT License (c) 2020 fanoush https://github.com/fanoush
// see full license text at https://choosealicense.com/licenses/mit/
// compiled with options SPI3,LCD_BPP=8
var SPI3 = (function(){
  var bin=atob("AAAAAAAAAAAAAAUqAAAAAAUrAAAAAAEsAAAAAP//////////AAAAAAAAAAAQtQNMfEQggGGAooDjgBC9zP///wdLe0QbiUOxBEoTaAAr/NAAIxNgA0p6RBOBcEcY8QJAuv///6b///8t6fBBIkwdT9/4iIB8RAo04HBicgASEhKgcGFxInLjcgkSGxIHIhZIIXGjcjpgIUYR+AFb1bEYS3tETBkZM5xCFNgBJsj4AGD/98b/DUoAIxNgA2AMSxlgXWCj8jRTHmADaAAr/NAAIwNg4OcAIztgBksBIhpgvejwgQC/APUCQBjxAkA49QJARPUCQATwAkCI////cPUCQFz///84tQ9MByMjYA5LASUdYP/3lf8NSwAiGmCj9YRjGmALShBgUWCi8jRSFWAaaAAq/NAAIBhgBksgYAEiGmA4vQC/APUCQHD1AkA49QJARPUCQATwAkATtQAoHtsAKaa/jfgFEAIkASQAKqS/AqkJGY34BACkvwE0AfgELAAror8CqhIZATQhRgGoqL8C+AQ8//e3/yBGArAQvQAk+ucUSxtoMLULuxNLG2gLsRNKE2AWShJLekQABtRpHGAUalxgT/D/NJxgACQcZg1MASMjYFVqRPhQXJRqC0qZQBRgQvhIDEL4GBwYRjC9T/D/MPvnAL8A9QJABPMCQAjzAkAI9QJAZPUCQGz1AkBG/v//B0oAIxNgovV+chNgBUsBIhpgA/VAcxtoC7EDShNgcEcA9QJABPACQAjzAkAQtQNMfETE6QcBxOkJIxC9vP3//y3p8E9cTLewfEQBkZT4BLAAKADwo4AAKQDwoIAL8f8zBysA8puAASMD+gvzATvbsgKTAXhDeGeIQeoDIUlLByQcYElMACYRQSZgAPECCImyNEYN8XgJA5NIS3tEFUaz+ACgAptdRO2yBy0D6gEMAZuIvwg9E/gMwIi/GPgBOwn4BMCCv+2yxfEIDgP6DvNB+gvxiL8ZQ2McCvH/Ol8ribIf+or6Ut3N6QQy//eh/i9L3/jMwAWaACQcYKP1hGOs9adsHGDD+CyUBJvM+Dg1ASPM+AAw3/iswPxEnhus+AgwNtE0Rg3xeAm68QAPudEmS3tEAT/biBhEv7JDeAF4QeoDIRFBAPECCImyAC+k0RSz//du/hVLFkofYKP1hGOi8jRSH2DC+DSVwvg4RQEhEWAaaAAq/NAAIhpgA5sAIBhgDEsBIhpgN7C96PCPHEbL5w3xGAnI5//3S/7u50/w/zDx5wC/APUCQHD1AkA49QJARPUCQATwAkCk/f//Uv3//0j1AkDU/P//vPz//w==");
  return {
    cmd:E.nativeCall(261, "int(int,int)", bin),
    cmd4:E.nativeCall(345, "int(int,int,int,int)", bin),
    setpins:E.nativeCall(573, "void(int,int,int,int)", bin),
    setwin:E.nativeCall(105, "void(int,int,int,int)", bin),
    enable:E.nativeCall(417, "int(int,int)", bin),
    disable:E.nativeCall(529, "void()", bin),
    blit_setup:E.nativeCall(45, "void(int,int,int,int)", bin),
    blt_pal:E.nativeCall(593, "int(int,int,int)", bin),
  };
})();
//*/
E.kickWatchdog();


D37.set();

//G5 display pins
CS=D26;DC=D27;RST=D40;
SCK=D5;MOSI=D11;
// D3 and D34 is digital and analog power?

// CLK,MOSI,CS,DC
SCK.write(0);MOSI.write(0);CS.write(1);DC.write(1);
SPI3.setpins(SCK,MOSI,CS,DC);
SPI3.enable(0x14,0); //32MBit, mode 0

function toFlatString(arr){
  var b=E.toString(arr);if (b) return b;
  print("toFlatString() fail&retry!");E.defrag();b=E.toString(arr);if (b) return b;
  print("fail&retry again!");E.defrag();b=E.toString(arr);if (b) return b;
  print("failed!"); return b;
}
function toFlatBuffer(a){return E.toArrayBuffer(toFlatString(a));}
function cmd(a){
  var l=a.length;
  if (!l)return SPI3.cmd4(a,-1,-1,-1);
  if (l==2)return SPI3.cmd4(a[0],a[1],-1,-1);
  if (l==3)return SPI3.cmd4(a[0],a[1],a[2],-1);
  if (l==4)return SPI3.cmd4(a[0],a[1],a[2],a[3]);
  if (l==1)return SPI3.cmd4(a[0],-1,-1,-1);
  var b=toFlatString(a);
  SPI3.cmd(E.getAddressOf(b,true),b.length);
}
/* cmds takes array of len+cmd+data blocks like this
    5, 0x2a, 0,0, 0,0,
    5, 0x2b, 0,0, 0,0,
    1, 0x2c,
  0

// not needed here anymore
function cmds(arr){
  var b=toFlatString(arr);
  var c=SPI3.cmds(E.getAddressOf(b,true),b.length);
  if (c<0)print('lcd_cmds: buffer mismatch, cnt='+c);
  return c;
}
*/
function delayms(ms){
  digitalPulse(DC,0,ms); // DC pin is harmless
  digitalPulse(DC,0,0); // 0ms=wait for previous
}
function init(){
    D3.set(); //display enable
    delayms(10);
    RST.set();
    delayms(20);
    RST.reset();
    delayms(100);
    RST.set();
    delayms(100);
    cmd([0xFE,1]);// set manuf. page 1
    cmd([0x6C,0x0A]);
    cmd([0x04,0xA0]);
    cmd([0xFE,0x05]); // page 5
    cmd([0x05,0x01]);
    cmd([0xFE,0x00]); // page 0
    cmd([0x35,0x00]);
    cmd([0x36,0xC0]);
    cmd([0x3A,0x70|2]);  // 1=8bit grayscale,2=8bit RGB332,3=RGB111<<3|RGB111,5=16bit,6=18bit,7=24bit 
    delayms(10);
    cmd([0x53,0x20]); // enable BCON - brightness control
    cmd([0xC4,0x80]); // spi mode
    cmd(0x11);
    delayms(120);
    cmd(0x29);
    D34.reset();
    cmd([0x51,0xFF]); //Brightness 0x90 0xC0 0xFF
}

var pal;
switch(bpp){
  case 2: pal= Uint8Array([0x000,0xf00,0x0f0,0x00f]);break; // white won't fit
//  case 1: pal= Uint16Array([0x000,0xfff]);break;
  case 1:
  pal= Uint8Array(toFlatBuffer( // same as 16color below, use for dynamic colors
    [ 0x0,0x2,0x14,0x16,0xa0,0xa2,0xa8,0xb6,0x49,0x4b,0x5d,0x5f,0xe9,0xeb,0xfd,0xff ]
  ));
  g.sc=g.setColor;
  c1=pal[1]; //save color 1
  g.setColor=function(c){ //change color 1 dynamically
    c=Math.floor(c);
    if (c > 1) {
      pal[1]=pal[c]; g.sc(1);
    } else if (c==1) {
      pal[1]=c1; g.sc(1);
    } else g.sc(c);
  }; break;
  case 4: pal= Uint8Array(toFlatBuffer( // CGA
    [
// function RGB444to222(r,g,b){return(((r>>2)<<6)|((g>>2)<<4)|((b>>2)<<2)).toString(16);}
// function RGB444to332(r,g,b){return(((r>>1)<<5)|((g>>1)<<2)|((b>>2))).toString(16);}
//  0x0,0x49,0x92,0xb6,0x8c,0x64,0x0c,0x14,0x0b,0x03,0x22,0xe2,0xc0,0xec,0xfc,0xff
//  CGA palette 8bit RGB332
0x0,0x2,0x14,0x16,0xa0,0xa2,0xa8,0xb6,0x49,0x4b,0x5d,0x5f,0xe9,0xeb,0xfd,0xff
//  CGA palette 12bit RGB444
//      0x000,0x00a,0x0a0,0x0aa,0xa00,0xa0a,0xa50,0xaaa,
//     0x555,0x55f,0x5f5,0x5ff,0xf55,0xf5f,0xff5,0xfff
//16bit RGB565
//      0x0000,0x00a8,0x0540,0x0555,0xa800,0xa815,0xaaa0,0xad55,
//      0x52aa,0x52bf,0x57ea,0x57ff,0xfaaa,0xfabf,0xffea,0xffff
    ]));break;
}
// precompute addresses for flip
g.palA=E.getAddressOf(pal.buffer,true); // pallete address
g.buffA=E.getAddressOf(g.buffer,true); // framebuffer address
g.stride=g.getWidth()*bpp/8; // line stride

g.flip=function(force){
  //"jit";
  var r=g.getModified(true);
  if (force)
    r={x1:0,y1:0,x2:this.getWidth()-1,y2:this.getHeight()-1};
  if (r === undefined) return;
  var x1=r.x1&0x1fe,y1=r.y1&0x1fe; // align start to even pixel
  var xw=(r.x2-x1+1);if (xw&1) xw++;// align also width/height to even number of pixels
  var yw=(r.y2-y1+1);if (yw&1) yw++;
  SPI3.blit_setup(xw,yw,bpp,g.stride);
  SPI3.setwin(16+x1,15+x1+xw,2+y1,1+y1+yw);// offset 16,2
  var xbits=x1*bpp, bitoff=xbits%8;
  var addr=g.buffA+(xbits-bitoff)/8+y1*g.stride; // address of upper left corner
  SPI3.blt_pal(addr,g.palA,bitoff);
};

g.isOn=false;
init();
g.on=function(){
  if (this.isOn) return;
  D3.set();D34.reset();cmd(0x11);cmd(0x29);
  g.flip(true);
  this.isOn=true;
  this.setBrightness();
};
g.lowPower = function(b){cmd(0xFE); if (b) cmd(0x39); else cmd(0x38);};
g.off=function(){
  if (!this.isOn) return;
  cmd([0x51,0]);//brightness to 0
  D34.set();cmd(0x10);cmd(0x28);D3.reset();
  this.isOn=false;
};

g.lev=255;
g.setBrightness=function(lev){
  if (lev>=0 && lev<256)
    this.lev=lev;
  else
    lev=this.lev;
  if (this.isOn){
    cmd([0x51,lev]);
  }
};
var VIB=D39;
function vibon(vib){
 if(vib.i>=1)VIB.write(0);else analogWrite(VIB,vib.i);
 setTimeout(viboff,vib.on,vib);
}
function viboff(vib){
 VIB.write(1);
 if (vib.c>1){vib.c--;setTimeout(vibon,vib.off,vib);}
}
vibrate=function(intensity,count,onms,offms){
 vibon({i:intensity,c:count,on:onms,off:offms});
};
function battVolts(){
  return 4.20/0.63*analogRead(D4);
}
function battLevel(v){
  var l=3.5,h=4.19;
  v=v?v:battVolts();
  if(v>=h)return 100;
  if(v<=l)return 0;
  return 100*(v-l)/(h-l);
}
function battInfo(v){v=v?v:battVolts();return `${battLevel(v)|0}% ${v.toFixed(2)}V`;}

function randomLines(){
  g.clear();
  var cols=(bpp==1)?14:(1<<bpp)-1,w=g.getWidth(),h=g.getHeight(),r=Math.random;
  return setInterval(function(){
    g.setColor(1+r()*cols);
    g.drawLine(r()*w,r()*h,r()*w,r()*h);
      g.flip();
  },5);
}


function randomShapes(){
  g.clear();
  var cols=(bpp==1)?14:(1<<bpp)-1,w=g.getWidth()-10,h=g.getHeight()-10,r=Math.random;
  return setInterval(function(){
    g.setBgColor(0);
    g.setColor(1+r()*cols);
    x1=r()*w;x2=10+r()*w;
    y1=r()*h;y2=10+r()*h;
    if (bpp==1 && ((x1&31)==1)) g.clear(); // for bpp==1 clear sometimes so we can see ellipses again
    if (x1&1)
      g.fillEllipse(Math.min(x1,x2), Math.min(y1,y2),Math.max(x1,x2), Math.max(y1,y2));
    else
      g.fillRect(Math.min(x1,x2), Math.min(y1,y2),Math.max(x1,x2), Math.max(y1,y2));
    g.flip();
  },5);
}

// cube from https://www.espruino.com/Pixl.js+Cube+Badge
var rx = 0, ry = 0, cc = 1;
// Draw the cube at rotation rx and ry
function drawCube(xx,yy,zz) {
  // precalculate sin&cos for rotations
  var rcx=Math.cos(rx), rsx=Math.sin(rx);
  var rcy=Math.cos(ry), rsy=Math.sin(ry);
  // Project 3D into 2D
  function p(x,y,z) {
    var t;
    t = x*rcy + z*rsy;
    z = z*rcy - x*rsy;
    x=t;
    t = y*rcx + z*rsx;
    z = z*rcx - y*rsx;
    y=t;
    z += 4;
    return [xx + zz*x/z, yy + yy*y/z];
  }
  var a,b;
  // -z
  a = p(-1,-1,-1); b = p(1,-1,-1);
  g.drawLine(a[0],a[1],b[0],b[1]);
  a = p(1,1,-1);
  g.drawLine(a[0],a[1],b[0],b[1]);
  b = p(-1,1,-1);
  g.drawLine(a[0],a[1],b[0],b[1]);
  a = p(-1,-1,-1);
  g.drawLine(a[0],a[1],b[0],b[1]);
  // z
  a = p(-1,-1,1); b = p(1,-1,1);
  g.drawLine(a[0],a[1],b[0],b[1]);
  a = p(1,1,1);
  g.drawLine(a[0],a[1],b[0],b[1]);
  b = p(-1,1,1);
  g.drawLine(a[0],a[1],b[0],b[1]);
  a = p(-1,-1,1);
  g.drawLine(a[0],a[1],b[0],b[1]);
  // edges
  a = p(-1,-1,-1); b = p(-1,-1,1);
  g.drawLine(a[0],a[1],b[0],b[1]);
  a = p(1,-1,-1); b = p(1,-1,1);
  g.drawLine(a[0],a[1],b[0],b[1]);
  a = p(1,1,-1); b = p(1,1,1);
  g.drawLine(a[0],a[1],b[0],b[1]);
  a = p(-1,1,-1); b = p(-1,1,1);
  g.drawLine(a[0],a[1],b[0],b[1]);
}

function stepCube() {
  rx += 0.1;
  ry += 0.1;
  g.setColor(0);g.fillRect(150,80,320,240);g.setColor(1+cc);cc=(cc+1)%15;
  drawCube(240,160,160);
  // update the whole display
  g.flip();
}

//require("Font6x8").add(Graphics);
//require("Font6x12").add(Graphics);
//require("Font8x12").add(Graphics);
require("Font8x16").add(Graphics);

function info(){
  g.clear();var w=g.getWidth();
  g.setFont("6x8",2);g.setColor(10);
  var s="Espruino "+process.version;
  g.drawString(s,(w-g.stringWidth(s))/2,40);
  if (bpp==1) g.flip();
  g.setFont("6x8",1);g.setColor(14);
  s="RM67162 8 bit mode, 32Mbps SPI with DMA";
  g.drawString(s,(w-g.stringWidth(s))/2,62);
  if (bpp==1) g.flip();
  for (var c=0;c<8;c++){
    g.setColor(c+8);g.fillRect(120+25*c,255,145+25*c,275);
    if (bpp==1) g.flip();
  }
  for ( c=0;c<8;c++) {g.setColor(c);g.fillRect(120+25*c,280,145+25*c,300);
    if (bpp==1) g.flip();
  }
  g.flip();
  return setInterval(function(){
    stepCube();
  },5);
}


var lastmin=-1;
var volts;
function drawClock(){
  var d=Date();
  volts= volts ? (volts+battVolts())/2:battVolts(); // average until shown
  if (d.getMinutes()==lastmin) return;
  d=d.toString().split(' ');
  var min=d[4].substr(3,2);
  var sec=d[4].substr(-2);
  var tm=d[4].substring(0,5);
  var hr=d[4].substr(0,2);
  lastmin=min;
  g.clear();
  var w=g.getWidth();
  g.setColor(15);
  g.setFont("8x16");
  var batt=battInfo(volts);volts=0;// clear average
  g.drawString(batt,(w-g.stringWidth(batt))/2,80);
  //var tm=hr+" "+min;
  g.setFontVector(100);
  g.drawString(tm,4+(w-g.stringWidth(tm))/2,160);
  if(bpp==1) g.flip();
  g.setFontVector(32);
  g.setColor(8+3);
  var dt=d[0]+" "+d[1]+" "+d[2];//+" "+d[3];
  g.drawString(dt,(w-g.stringWidth(dt))/2,280);
  g.flip();
}
function clock(){
  lastmin=-1;
  drawClock();
  return setInterval(function(){
    drawClock();
  },1000);
}


function sleep(){
  g.clear();//g.flip();
  g.off();
  currscr=-1;
  return 0;
}

var screens=[clock,info,randomShapes,randomLines,sleep];
var currscr= -1;
var currint=0;
setWatch(function(){
  if (!g.isOn) g.on();
  currscr++;if (currscr>=screens.length) currscr=0;
  if (currint>0) clearInterval(currint);
  currint=screens[currscr]();
},BTN1,{ repeat:true, edge:'rising',debounce:25 }
);


var sf8=new SPI(); // SPI flash 8MB
D20.write(1);
D21.set();D24.set();//wp,hold (IO2,IO3)
sf8.setup({sck:D25,mosi:D22,miso:D23,mode:0});
//sf8.send([0xab],D20); //wake
//print(sf8.send([0x9f,0,0,0],D20)); // id
sf8.send([0xb9],D20); //put to deep sleep

var sf16=new SPI(); // SPI flash 16MB
D14.write(1);
D16.set();D17.set();//wp,hold (IO2,IO3)
sf16.setup({sck:D19,mosi:D18,miso:D15,mode:0});
//sf16.send([0xab],D14); //wake
//print(sf16.send([0x9f,0,0,0],D14)); // id
sf16.send([0xb9],D14); //put to deep sleep


var i2c=new I2C();
i2c.setup({scl:D10,sda:D9});
// 0x15 touch, 0x0e KXTJ3 accel, 0x38 hr sensor

//i2c.writeTo(0x15,254,0);//touch auto sleep
D29.read(); // touch irq
D28.set(); // touch reset
// put touch to sleep
digitalPulse(D28,1,[5,50]);setTimeout(()=>{i2c.writeTo(0x15,0xa5,3);},100);


/*
NRF.whitelist=[];
NRF.on('connect',function(addr) {
  if (!NRF.whitelist.includes(addr)){
    if (BTN1.read()){ // add to whitelist when button is held while connecting
      NRF.whitelist.push(addr);
      vibrate(1,1,100,0);
    } else
        NRF.disconnect();
  }
  NRF.connection = {};
  NRF.connection.addr = addr;
  NRF.connected=true;
  NRF.setRSSIHandler((rssi)=>{NRF.connection.RSSI=rssi;});
});
NRF.on('disconnect',function(reason) {
  NRF.connected=false;
  NRF.connection = {};
  NRF.lastReason=reason;
});
*/
/* test draw speed
g.clear();var d=Date();g.flip();d=Date().ms-d.ms;
g.fillRect(0,0,239,279);var d=Date();g.flip();d=Date().ms-d.ms;
*/

