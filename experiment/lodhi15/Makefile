CONTIKI_PROJECT = node
all: $(CONTIKI_PROJECT)

# Configure simulation parameters
CFLAGS += -DRPL_CONF_WITH_MULTIPATH=1
CFLAGS += -DSIM_N_SRC=14
CFLAGS += -DSIM_PKT_INT=5

# Configure netstack
MAKE_MAC = MAKE_MAC_CSMA
MAKE_NET = MAKE_NET_IPV6
MAKE_ROUTING = MAKE_ROUTING_RPL_LITE

CONTIKI = ../../contiki-ng
include $(CONTIKI)/Makefile.include
