TIMEOUT(100000); /* Time out after 100 seconds */

while(true) {
  log.log(time + "\t" + "ID:" + id + "\t"+ msg + "\n");
  YIELD();
}
