TIMEOUT(720000); /* Time out after 12 minutes */

while(true) {
  log.log(time + "\t" + "ID:" + id + "\t"+ msg + "\n");
  YIELD();
}
