# SDN-Mininet-Static-Routing-Using-POX
This project demonstrates static routing using an SDN controller with POX and Mininet. Flow rules are manually installed in switches to define a fixed path between hosts. Packets follow this predefined route, ensuring deterministic behavior. Connectivity and flow tables are verified to confirm correct routing.

# Static Routing using SDN Controller (POX)

## 📌 Project Overview

This project demonstrates **Static Routing using Software Defined Networking (SDN)** with a **POX controller** and **Mininet emulator**.

In this setup, routing paths are **manually defined** and enforced using **controller-installed flow rules**. The switches do not make independent decisions—they simply follow instructions from the controller.

---

## 🧠 Objective

* Implement static routing using an SDN controller
* Install flow rules manually in switches
* Validate packet delivery between hosts
* Demonstrate deterministic (fixed) routing behavior
* Perform regression testing to ensure path consistency

---

## 🏗️ Network Topology

```
h1 ── s1 ── s2 ── h2
```

* **h1, h2** → Hosts (end devices)
* **s1, s2** → OpenFlow switches
* **Controller (POX)** → Controls routing logic

---

## ⚙️ Tools & Technologies

* **Mininet** – Network emulator
* **POX Controller** – SDN controller (Python-based)
* **OpenFlow 1.0** – Communication protocol

---

## 🚀 Setup Instructions

### 1. Install Mininet

```bash
sudo apt update
sudo apt install mininet
```

### 2. Install POX

```bash
cd ~
git clone https://github.com/noxrepo/pox.git
cd pox
```

---

## 🧑‍💻 Controller Implementation

Create a file `static_routing.py` inside the POX directory:

```python
from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

def install_rules(event):
    dpid = event.connection.dpid
    msg = of.ofp_flow_mod()

    if dpid == 1:
        msg.match.in_port = 1
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.match.in_port = 2
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)

    elif dpid == 2:
        msg.match.in_port = 1
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.match.in_port = 2
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)

def _handle_ConnectionUp(event):
    log.info("Switch %s connected", event.connection.dpid)
    install_rules(event)

def launch():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
```

---

## ▶️ Running the Project

### Step 1: Start Controller

```bash
cd ~/pox
./pox.py log.level --DEBUG static_routing
```

---

### Step 2: Start Mininet (New Terminal)

```bash
sudo mn --topo linear,2 --controller=remote,ip=127.0.0.1,port=6633 --switch ovsk,protocols=OpenFlow10
```

---

## ✅ Testing & Validation

### Show Nodes

```bash
nodes
```

### Show Links

```bash
links
```

### Test Connectivity

```bash
pingall
```

Expected Output:

```
0% packet loss
```

---

## 🔍 Flow Rule Verification

```bash
sudo ovs-ofctl dump-flows s1
sudo ovs-ofctl dump-flows s2
```

---

## 🔁 Regression Test

1. Delete flow rules:

```bash
sudo ovs-ofctl del-flows s1
```

2. Restart controller

3. Re-run Mininet

👉 The same routing path should be restored

---

## 🧠 Key Concepts Demonstrated

* **Centralized Control (SDN)**
* **Separation of Control & Data Plane**
* **Static Routing (Deterministic Path)**
* **Flow Rule Installation using OpenFlow**

---

## ⚠️ Limitations

* No dynamic routing
* No fault tolerance
* Not scalable for large networks

---

## 💡 Future Enhancements

* Implement dynamic routing (e.g., Dijkstra algorithm)
* Add link failure detection
* Introduce load balancing
* Visualize traffic using Wireshark

---

## 🎯 Conclusion

This project successfully demonstrates how an SDN controller can enforce **static routing paths** by installing predefined flow rules in switches, ensuring predictable and controlled network behavior.

---

## 👨‍💻 Author

* Name: A Sheiman Joshi
* Course: BTech CSE
* Project: Static Routing using SDN Controller
