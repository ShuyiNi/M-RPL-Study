TIMEOUT(300000); /* Time out after 5 minutes */

while(true) {
  log.log(time + " " + "node-" + id + " "+ msg + "\n");
  YIELD();
}
