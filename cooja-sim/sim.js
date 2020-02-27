TIMEOUT(600000); /* Time out after 10 minutes */

while(true) {
  log.log(time + "\t" + "ID:" + id + "\t"+ msg + "\n");
  YIELD();
}
