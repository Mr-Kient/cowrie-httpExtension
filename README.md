# Cowrie-httpExtension

This project aims to provide Cowire with an HTTP proxy service to break through existing SSH and Telnet service limitations

![](http://cdn.kient.club/myOwn/arch%20%E6%8B%B7%E8%B4%9D_2.jpg)

## Cowrie Deployment and High Interaction Mode Configuration
1. follow the document`High Interaction Cowrie Configuration.md`

2. copy `Cowrie_cfg/cowrie.cfg` to `cowrie/cowrie/etc`, this is an example of configuration file, you can feel free to edit it

3. > [!NOTE]
   >
   > * Ensure that all required dependencies are installed correctly
   >
   > * Remember to change the image file path field `guest_image_path = /home/cowrie/cowrie-imgs/Metasploitable2.qcow2`

## Change backend Virtual Machine Images

1. Download source of Metasploitable2 in *qcow2* format: https://sourceforge.net/projects/metasploitable/files/Metasploitable2/

2. copy `/Cowrie_cfg/Metasploitable2_cowrie.xml` to `cowrie/cowrie/share/cowrie/pool_configs`

## Define a New Virtual Network

```sh
virsh net-list # check all existed internet
```

Create a vbr1.xml to establish a network for specific vm

```xml
<network>
    <name>{network_name}</name>
    <forward mode='nat'/>
    <bridge name='{iface_name}' stp='on' delay='0'/>
    <ip address='{default_gateway}' netmask='255.255.255.0'>
        <dhcp>
            <range start='{dhcp_range_start}' end='{dhcp_range_end}'/>
            {hosts}
        </dhcp>
    </ip>
</network>

<!-- an example -->
<network>
    <name>vbr1</name>
    <forward mode='nat'/>
    <bridge name='vbr1' stp='on' delay='0'/>
    <ip address='163.114.104.1' netmask='255.255.255.0'>
        <dhcp>
            <range start='163.114.104.2' end='163.114.104.254'/>
            <!-- Add any specific hosts here if needed -->
        </dhcp>
    </ip>
</network>
```

Create `vbr1` network and start it

```sh
virsh net-define vbr1.xml
virsh net-start vbr1
```

## Install a static backend exclusive to the HTTP service

1. `$virsh define ‘Metasploitable2_2.xml’`

   > [!NOTE]
   >
   > Remember to change the image file path field `<source file='/dev/exdisk/Metasploitable2.qcow2'/>`

2. virsh start Meta2

3. Check vm's IP

   ```sh
   $virsh net-list
   $virsh net-info vbr1
   $virsh net-dhcp-leases vbr1
   ```

## Start the HTTP Reverse Proxy Service

1. change  the variable `TARGET_SERVER_IP` in the `/twisted/HTTPProxyFactory.py`

2. Run the proxy in back `$nohup python3 HTTPProxyFactory.py &`

3. How to terminate it?

   ```sh
   ps aux | grep HTTPProxyFactory.py
   kill <PID>
   ```

## Establish Inbound & Outbound Handler

1. install netfilterqueue and test

   ```python
   '''
   test.py
   
   such a running result does not report an error, 
   which means the installation is successful.
   '''
   from netfilterqueue import NetfilterQueue
   
   def print_and_accept(pkt):
   		pkt.accept()
   nfqueue = NetfilterQueue()
   nfqueue.bind(1, print_and_accept)
   try:
   		nfqueue.run()
   except KeyboardInterrupt:
   		print('')
   nfqueue.unbind()
   ```

2. View the iptables rules that inbound and outbound virtual machine traffic passes through

   ```sh
   iptables -t <tableName> -L
   ```

3. Start the outbound and inbound handlers	

   ```sh
   $ nohup python3 .../http/in&outbound_handler/handler_in.py &
   $ nohup python3 .../http/in&outbound_handler/handler_out.py &
   ```

4. Establish iptables rules binding to netfilterqueues

   * Outbound (assume vm's ip is 163.114.104.0/24)

   ```sh
   sudo iptables -I LIBVIRT_FWO -i virbr1 -s 163.114.104.0/24 -p tcp -j NFQUEUE --queue-num 1
   sudo iptables -D LIBVIRT_FWO -i virbr1 -s 163.114.104.0/24 -p tcp -j NFQUEUE --queue-num 1
   ```

   * Inbound

   ```sh
   sudo iptables -I LIBVIRT_FWI -o virbr1 -d 163.114.104.0/24 -m conntrack --ctstate RELATED,ESTABLISHED -j NFQUEUE --queue-num 2
   sudo iptables -D LIBVIRT_FWI -o virbr1 -d 163.114.104.0/24 -m conntrack --ctstate RELATED,ESTABLISHED -j NFQUEUE --queue-num 2
   ```

   

