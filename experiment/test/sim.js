TIMEOUT(100000); /* Time out after 100 s */

while(true) {
  log.log(time + "\t" + "ID:" + id + "\t"+ msg + "\n");
  YIELD();
}
