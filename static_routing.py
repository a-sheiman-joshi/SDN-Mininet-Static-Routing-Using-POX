from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

def install_rules(event):
    dpid = event.connection.dpid
    msg = of.ofp_flow_mod()

    # Switch 1
    if dpid == 1:
        # h1 -> s2
        msg.match.in_port = 1
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)

        # reverse
        msg = of.ofp_flow_mod()
        msg.match.in_port = 2
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)

    # Switch 2
    elif dpid == 2:
        # s1 -> h2
        msg.match.in_port = 1
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)

        # reverse
        msg = of.ofp_flow_mod()
        msg.match.in_port = 2
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)

def _handle_ConnectionUp(event):
    log.info("Switch %s connected", event.connection.dpid)
    install_rules(event)

def launch():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
