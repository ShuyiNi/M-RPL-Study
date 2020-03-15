#include "contiki-net.h"
#include "contiki.h"
#include "random.h"
#include "services/deployment/deployment.h"

#include <inttypes.h>

#include "sys/log.h"
#define LOG_MODULE "App"
#define LOG_LEVEL LOG_LEVEL_INFO

#define UDP_PORT 1234

#define ROOT_ID 1
#define WAIT_TIME (100 * CLOCK_SECOND)
#define SEND_INTERVAL (SIM_PKT_INT * CLOCK_SECOND / 10)

static struct simple_udp_connection udp_conn;

PROCESS(app_process, "App process");
AUTOSTART_PROCESSES(&app_process);

static void udp_rx_callback(struct simple_udp_connection *c,
                            const uip_ipaddr_t *sender_addr,
                            uint16_t sender_port,
                            const uip_ipaddr_t *receiver_addr,
                            uint16_t receiver_port, const uint8_t *data,
                            uint16_t datalen) {
  uint32_t count;
  memcpy(&count, data, sizeof(uint32_t));
  LOG_INFO("Received request %" PRIu32 " from ", count);
  LOG_INFO_6ADDR(sender_addr);
  LOG_INFO_("\n");
}

PROCESS_THREAD(app_process, ev, data) {
  static struct etimer start_timer;
  static struct etimer periodic_timer;
  static uint32_t count;
  static uip_ipaddr_t dest_ipaddr;

  PROCESS_BEGIN();

  LOG_INFO("RPL_WITH_MULTIPATH=%u\n", RPL_WITH_MULTIPATH);
  LOG_INFO("SIM_PKT_INT=%u\n", SIM_PKT_INT);

  /* Initialize UDP connection */
  simple_udp_register(&udp_conn, UDP_PORT, NULL, UDP_PORT, udp_rx_callback);

  if (node_id == ROOT_ID) {
    /* Initialize DAG root */
    NETSTACK_ROUTING.root_start();
  } else {
    /* Wait for RPL to set up */
    etimer_set(&start_timer, WAIT_TIME);
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&start_timer));

    etimer_set(&periodic_timer, random_rand() % SEND_INTERVAL);
    while (1) {
      PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&periodic_timer));

      if (NETSTACK_ROUTING.node_is_reachable() &&
          NETSTACK_ROUTING.get_root_ipaddr(&dest_ipaddr)) {
        /* Send to DAG root */
        LOG_INFO("Sending request %u to ", count);
        LOG_INFO_6ADDR(&dest_ipaddr);
        LOG_INFO_("\n");
        simple_udp_sendto(&udp_conn, &count, sizeof(count), &dest_ipaddr);
        count++;
      } else {
        LOG_INFO("Not reachable yet\n");
      }

      /* Schedule next packet */
      etimer_set(&periodic_timer, SEND_INTERVAL);
    }
  }

  PROCESS_END();
}
