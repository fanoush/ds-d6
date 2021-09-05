#include "jsinteractive.h"
#include "jsdevices.h"
#include "jshardware.h"

/*JSON{
  "type" : "init",
  "generate" : "jswrap_id130_init"
}*/
void jswrap_id130_init() {
  // set pin 6 as input disconnected with internal pulldown, needed for touch button on pin 7 to work
  // could be also set as output with value 0 but this may draw less power(?)
  // this needs to be done here in init to get BTN1 working at startup time to possibly allow skipping .bootcde
  NRF_GPIO->PIN_CNF[6]=6;
}

/*xxJSON{
  "type" : "kill",
  "generate" : "jswrap_id130_kill"
}*/
//void jswrap_id130_kill() {
//}
