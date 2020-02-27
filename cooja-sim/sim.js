TIMEOUT(300000); /* Time out after 5 minutes */

while(true) {
  log.log(time + "\t" + "ID:" + id + "\t"+ msg + "\n");
  YIELD();
}
