#include "contiki.h"
#include "contiki-net.h"

#include "sys/log.h"
#define LOG_MODULE "App"
#define LOG_LEVEL LOG_LEVEL_INFO

#define UDP_PORT 1234

static struct simple_udp_connection udp_conn;

PROCESS(app_process, "App process");
AUTOSTART_PROCESSES(&app_process);

PROCESS_THREAD(app_process, ev, data) {
  PROCESS_BEGIN();

  /* Initialize UDP connection */
  simple_udp_register(&udp_conn, UDP_PORT, NULL, UDP_PORT, NULL);

  PROCESS_END();
}
