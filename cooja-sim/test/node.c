#include "contiki.h"
#include "contiki-net.h"
#include "services/deployment/deployment.h"
#include "net/routing/routing.h"
#include "random.h"
#include "net/netstack.h"
#include "net/ipv6/simple-udp.h"

#include <inttypes.h>

#include "sys/log.h"
#define LOG_MODULE "App"
#define LOG_LEVEL LOG_LEVEL_INFO

#define UDP_PORT 8214
#define SEND_INTERVAL (CLOCK_SECOND)

static struct simple_udp_connection udp_conn;

PROCESS(app_process, "App process");
AUTOSTART_PROCESSES(&app_process);


static void
udp_rx_callback(struct simple_udp_connection *c,
         const uip_ipaddr_t *sender_addr,
         uint16_t sender_port,
         const uip_ipaddr_t *receiver_addr,
         uint16_t receiver_port,
         const uint8_t *data,
         uint16_t datalen)
{
  LOG_INFO("Received response '%.*s' from ", datalen, (char *) data);
  LOG_INFO_6ADDR(sender_addr);
  LOG_INFO_("\n");
}


PROCESS_THREAD(app_process, ev, data)
{
  static struct etimer periodic_timer;
  static unsigned count;
  static char str[32];
  static uip_ipaddr_t dest_ipaddr;

  PROCESS_BEGIN();

  /* Initialize UDP connection */
  simple_udp_register(&udp_conn, UDP_PORT, NULL,
                      UDP_PORT, udp_rx_callback);

  if(node_id == ROOT_ID) {

    /* Initialize DAG root */
    NETSTACK_ROUTING.root_start();

  } else {

    etimer_set(&periodic_timer, random_rand() % SEND_INTERVAL);
    while(1) {
      PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&periodic_timer));

      if(NETSTACK_ROUTING.node_is_reachable() && NETSTACK_ROUTING.get_root_ipaddr(&dest_ipaddr)) {
        /* Send to DAG root */
        LOG_INFO("Sending request %u to ", count);
        LOG_INFO_6ADDR(&dest_ipaddr);
        LOG_INFO_("\n");
        snprintf(str, sizeof(str), "hello %d", count);
        simple_udp_sendto(&udp_conn, str, strlen(str), &dest_ipaddr);
        count++;
      } else {
        LOG_INFO("Not reachable yet\n");
      }

      /* Add some jitter */
      etimer_set(&periodic_timer, SEND_INTERVAL
        - CLOCK_SECOND + (random_rand() % (2 * CLOCK_SECOND)));
    }

  }

  PROCESS_END();
}
