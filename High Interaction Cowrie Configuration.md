# Cowrie Configuration
author: Wenbo Wang    

date: 2023-07-3
- [Cowrie Configuration](#cowrie-configuration)
- [Meduim Interaction Cowrie Configuration](#meduim-interaction-cowrie-configuration)
- [Pre-Condition](#pre-condition)
  - [Step 1: Install system dependencies](#step-1-install-system-dependencies)
  - [Step 2: Create a user account](#step-2-create-a-user-account)
  - [Step 3: Clone source from github and check](#step-3-clone-source-from-github-and-check)
  - [Step 4: Setup Virtual Environment](#step-4-setup-virtual-environment)
  - [Step 5: Install configuration file](#step-5-install-configuration-file)
  - [Step 6: Starting Cowrie](#step-6-starting-cowrie)
  - [Step 7: Listening on port 22 (OPTIONAL)](#step-7-listening-on-port-22-optional)
    - [1. Change the default ssh service port 22](#1-change-the-default-ssh-service-port-22)
    - [2. Utlizing Authbind](#2-utlizing-authbind)
- [High Interaction Cowrie Configuration](#high-interaction-cowrie-configuration)
  - [Installing Backend Pool dependencies](#installing-backend-pool-dependencies)
  - [Using proxy](#using-proxy)
  - [Choosing a Backend](#choosing-a-backend)
  - [Configuring the Proxy](#configuring-the-proxy)
    - [Backend configs](#backend-configs)
    - [Differences](#differences)
    - [Authentication](#authentication)
  - [Backend Pool](#backend-pool)
    - [Authorization](#authorization)
    - [Provided images](#provided-images)
    - [Backend Pool initialisation](#backend-pool-initialisation)
    - [Backend Pool configuration](#backend-pool-configuration)
  - [Analysing snapshots](#analysing-snapshots)
    - [Snapshot](#snapshot)
    - [Getting the a filesystem differences](#getting-the-a-filesystem-differences)
  - [Correct performing log](#correct-performing-log)

# Meduim Interaction Cowrie Configuration
<center>
<img src="http://cdn.kient.club/myOwn/Medium%20Interaction.png" width="30%" ></img>
<br>
<div style="color:orange; border-bottom: 1px solid #d9d9d9;
display: inline-block;
color: #999;
padding: 2px;">Figure1: Meduim Interation Mode</div>
</center>



# Pre-Condition

Prepare a Debian OS based machine or virtual machine before proceeding with all of the following steps. All subsequent operations will be performed on this machine. (Debian Website: https://www.debian.org/)

## Step 1: Install system dependencies

First we install system-wide support for Python virtual environments and other dependencies. Actual Python packages are installed later.

On Debian based systems (last verified on Debian 12):

    `$ sudo apt-get install git python3-virtualenv libssl-dev libffi-dev build-essential libpython3-dev python3-minimal authbind virtualenv`

## Step 2: Create a user account

It’s strongly recommended to run with a dedicated non-root user id:

    `$ sudo adduser --disabled-password cowrie`
    
      Adding user 'cowrie' ...
    
      Adding new group 'cowrie' (1002) ...
    
      Adding new user 'cowrie' (1002) with group 'cowrie' ...
    
      Changing the user information for cowrie
    
      Enter the new value, or press ENTER for the default
    
      Full Name []:
    
      Room Number []:
    
      Work Phone []:
    
      Home Phone []:
    
      Other []:
    
      Is the information correct? [Y/n]

`$ sudo su - cowrie`

## Step 3: Clone source from github and check

    `$ git clone http://github.com/cowrie/cowrie`
    
    Cloning into 'cowrie'...
    
    remote: Counting objects: 2965, done.
    
    remote: Compressing objects: 100% (1025/1025), done.
    
    remote: Total 2965 (delta 1908), reused 2962 (delta 1905), pack-reused 0
    
    Receiving objects: 100% (2965/2965), 3.41 MiB | 2.57 MiB/s, done.
    
    Resolving deltas: 100% (1908/1908), done.
    
    Checking connectivity... done.


`$ cd cowrie`

## Step 4: Setup Virtual Environment


Next you need to create your virtual environment:


    $ pwd
    
    /home/cowrie/cowrie
    
    $ python3 -m venv cowrie-env

  Activate the virtual environment and install packages:

    $ source cowrie-env/bin/activate
    (cowrie-env) $ python -m pip install --upgrade pip
    
    Requirement already satisfied: pip in ./cowrie-env/lib/python3.11/site-packages (23.0.1)
    
    Collecting pip
    
      Downloading pip-23.1.2-py3-none-any.whl (2.1 MB)


          ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.1/2.1 MB 511.5 kB/s eta 0:00:00
    
    Installing collected packages: pip
      
      Attempting uninstall: pip
        
        Found existing installation: pip 23.0.1
        
        Uninstalling pip-23.0.1:
          
          Successfully uninstalled pip-23.0.1
    
    Successfully installed pip-23.1.2


    (cowrie-env) $ python -m pip install --upgrade -r requirements.txt
    
    Successfully installed Automat-22.10.0 appdirs-1.4.4 attrs-23.1.0 bcrypt-4.0.1 certifi-2023.5.7 cffi-1.15.1 charset-normalizer-3.1.0 configparser-5.3.0 constantly-15.1.0 cryptography-41.0.1 hyperlink-21.0.0 idna-3.4 incremental-22.10.0 packaging-23.1 pyasn1-0.5.0 pyasn1_modules-0.3.0 pycparser-2.21 pyopenssl-23.2.0 pyparsing-3.0.9 python-dateutil-2.8.2 requests-2.31.0 service_identity-21.1.0 six-1.16.0 tftpy-0.8.2 treq-22.2.0 twisted-22.10.0 typing-extensions-4.6.3 urllib3-2.0.3 zope.interface-6.0

After the update is successful, you may want to double check that the downloaded package and the version of the package are consistent with  /home/cowrie/cowrie/requirements.txt

## Step 5: Install configuration file 

navigate to the /etc floder

    $ cd etc
    
    $ pwd
    /home/cowrie/cowrie/etc

The configuration for Cowrie is stored in **cowrie.cfg.dist** and **cowrie.cfg (Located in cowrie/etc)**. Both files are read on startup, where entries from cowrie.cfg take precedence. The .dist file can be overwritten by upgrades, cowrie.cfg will not be touched. To run with a standard configuration, there is no need to change anything.

Create a file called cowrie.cfg in /home/cowrie/cowrie/etc

    $ vim cowrie.cfg

When the default configuration needs to be changed, the fields to be modified and the configuration section described need to be found in **cowrie.cfg.dist**. The configuration sections are enclosed in square brackets, for example *[honeypoy], [proxy]* and *[telnet]* etc.

To enable telnet, for example, access cowrie.cfg and input only the following:

    [telnet]
    enabled = true

## Step 6: Starting Cowrie

Start Cowrie with the cowrie command. You can add the cowrie/bin directory to your path if desired. An existing virtual environment is preserved if activated, otherwise Cowrie will attempt to load the environment called “cowrie-env”:

    $ bin/cowrie start
    
    Activating virtualenv "cowrie-env"
    Starting cowrie with extra arguments [] ...

## Step 7: Listening on port 22 (OPTIONAL)

 ### 1. Change the default ssh service port 22

First we need to change the default ssh port from the default port 22 to something else (in this case change it to port 1022).

`$ sudo vi /etc/ssh/sshd_config`

In the sshd_config file find the following line:

    # Port 22

Uncomment (remove the # character), then change 22 to the port number you want. For example, if you want to change the port to 2222, the line should look like this:



    Port 2222


Please ensure that the port number you choose does not conflict with other services, preferably a port number between 1024 and 65535

### 2. Utlizing Authbind

Since the *cowrie* user does not have root access, it cannot listen directly to traffic on ports below 1024. By using authbind, *cowrie* can listen to port 22 with **non-root** privileges.

You can run authbind to listen as non-root on port 22 directly:

1. Installing the authbind 

 `$ sudo apt-get install authbind`
2. Create a configuration file /etc/authbind/byport/22:
   

 `$ sudo touch /etc/authbind/byport/22` 
3. Set permissions: change the ownership and permissions of /etc/authbind/byport/22 to the "cowrie" user and group:

 `$ sudo chown cowrie:cowrie /etc/authbind/byport/22
4. Set the file so that only the owner and members of the user group can read, write and execute it, no other user has any rights. 

 `$ sudo chmod 770 /etc/authbind/byport/22`

Change the listening port to 22 in *cowrie.cfg*:

    [ssh]
    
    listen_endpoints = tcp:22:interface=0.0.0.0

Use to set the *AUTHBIND_ENABLED* environment variable when starting cowrie:

    $ AUTHBIND_ENABLED=yes bin/cowrie start

Turning on cowrie after configuring the above will turn on **medium interactive cowrie**

# High Interaction Cowrie Configuration

<center>
<img src="http://cdn.kient.club/myOwn/Cowrie%20SSH_proxy%20structure.png" width="90%" ></img>
<br>
<div style="color:orange; border-bottom: 1px solid #d9d9d9;
display: inline-block;
color: #999;
padding: 2px;">Figure2: Architecture of Cowrie's High Interaction Mode</div>
</center>

## Installing Backend Pool dependencies

If you want to use the proxy functionality combined with the automatic backend pool, you need to install some dependencies, namely QEMU, libvirt, and their Python interface. In Debian/Ubuntu:

    $sudo apt-get install qemu qemu-system-arm qemu-system-x86 libvirt-dev libvirt-daemon libvirt-daemon-system libvirt-clients nmap

Then install the Python API to run the backend pool:

    $ source cowrie-env/bin/activate
    (cowrie-env) $ python -m pip install libvirt-python

To allow QEMU to use disk images and snapshots, set it to run with the user and group of the user running the pool (usually called ‘cowrie’ too):

`$ sudo vim /etc/libvirt/qemu.conf`

**Search and set both `user` and `group`** fields in `qemu.conf` file to “cowrie”, or the username/group you’ll be running the backend pool with.

    # The user for QEMU processes run by the system instance.It 
    # can be specified as a user name or as a user id.The gemu  
    # driver will try to parse this value first as a name and 
    # then,if the name doesn't exist, as a user id.
    
    # Since a sequence of digits is a valid user name,a leading #plus sign can be used to ensure that a user id will not be interpreted as a user
    # name.
    
    # Some examples of valid values are:
    
    #    user "gemu"            # user "+0"
    #    A user named "qemu"    # Super user (uid=0)
    #    user="100"             #A user named "100"or a user with uid=100
    #
    
    user = "cowrie"
    
    # The group for QEMU processes run by the system instance.It can be
    # specified in a similar way to user.
    group = "cowrie"

## Using proxy

The SSH and Telnet proxies can be used to provide a fully-fledged environment, in contrast to the emulated shell traditionally provided by Cowrie. With a real backend environment where attackers can execute any Unix command, Cowrie becomes a high-interaction honeypot.

To use the proxy, start by changing the backend option to proxy in the [honeypot] section. In the remainder of this guide we will refer to the [proxy] section of the config file.

Open file **cowrie.cfg** and type in the following

    [honeypot]
    EXPERIMENTAL: back-end to user for Cowrie, options: proxy or shell
    (default: shell)
    backend = shell
    #backend = proxy

When choosing option `backend = shell`, the cowrie is mid-interactive. At this point cowrie will completely emulate a fake system, the details of which can be seen in the  *[shell]*  section of cowrie.cfg.dist. 

When a proxy `backend = proxy` is selected, cowrie will enable proxy mode to connect to the real system (or virtual machine) in the backend pool. In other words, when cowrie's proxy mode is enabled, it will have the ability to forward incoming requests to the real backend

## Choosing a Backend

* ###  Simple Backend

<center>
<img src="http://cdn.kient.club/myOwn/High%20Interaction%20-%20%20remote%20simple%20backend.png" width="50%" ></img>
<br>
<div style="color:orange; border-bottom: 1px solid #d9d9d9;
display: inline-block;
color: #999;
padding: 2px;">Figure3: High Interation Mode - Remote Simple backend</div>
</center>
<center>
<img src="http://cdn.kient.club/myOwn/High%20Interaction%20-%20%20local%20simple%20backend.png" width="30%" ></img>
<br>
<div style="color:orange; border-bottom: 1px solid #d9d9d9;
display: inline-block;
color: #999;
padding: 2px;">Figure4: High Interation Mode - Local Simple backend</div>
</center>


Cowrie supports a **simple** backend (i.e., a single real system provided by you).


    [proxy]
    
    # type of backend:
    # - simple: backend machine deployed by you (CAREFUL WITH SECURITY ASPECTS!!), specify hosts and ports below
    backend = simple


 * ### Backend Pool

<center>
<img src="http://cdn.kient.club/myOwn/High%20Interaction%20-%20local%20backend%20pool.png" width="35%" ></img>
<br>
<div style="color:orange; border-bottom: 1px solid #d9d9d9;
display: inline-block;
color: #999;
padding: 2px;">Figure5: High Interation Mode - local backend pool</div>
</center>


What's more, you can also use Cowrie’s backend **pool**, which provides a set of VMs, handling their boot and cleanup, also ensuring that different attackers (different IPs) each see a “fresh” environment, while connections from the same IP get the same VM.

Open file **cowrie.cfg** and type in the following

    [proxy]
    
    # type of backend:
    #   - pool: cowrie-managed pool of virtual machines, configure below
    backend = pool

**VERY IMPORTANT NOTE:** some attacks consist of downloading malicious software or accessing illegal content through insecure machines (such as your honeypot). If you are using your **own backend**, be sure to restrict networking to the Internet on your backend, and ensure other machines on your local network are isolated from the backend machine. The backend pool restricts networking and does its best to ensure total isolation, to the best of Qemu/libvirt (and our own) capabilities. **Be very careful to protect your network and devices!**

## Configuring the Proxy

### Backend configs

If you choose the simple backend, configure the hosts and ports for your backend. 

    [proxy]
    
    backend = simple
    
    # ============================
    # Simple Backend Configuration
    # ============================
    
    backend_ssh_host = localhost
    
    backend_ssh_port = 2022
    
    backend_telnet_host = localhost
    
    backend_telnet_port = 2023


For the backend pool, configure the variables starting with `pool\_`.

When the proxy starts, and regardless whether the backend pool runs on the same machine as the proxy or not, some configurations are sent by the proxy to the pool during runtime.

These are:

* `pool_max_vms`: the number of VMs to be kept running in the pool

* `pool_vm_unused_timeout`: how much time (seconds) a used VM is kept running (so that an attacker that reconnects is served the same VM).

* `apool_share_guests`: what to do if no “pristine” VMs are available (i.e., all have been connected to); if set to true we serve a random one from the used, if false we throw an exception.

<br>    


    [proxy]
    
    backend = pool
    
    # ==========================
    # Pool Backend Configuration
    # ==========================
    
    # generic pool configurable settings
    
    pool_max_vms = 5
    
    pool_vm_unused_timeout = 600
    
    # allow sharing guests between different attackers if no new VMs are available
    
    pool_share_guests = true


The backend pool can be run in the same machine as Cowrie, or on a `remote` one (e.g. Cowrie on a Raspberry Pi, and the pool in a larger machine). In the former case, set pool to `local`; in the later, set pool to remote and specify its host and port, matching with the listen_endpoints of the `[backend_pool]` section.

<center>
<img src="http://cdn.kient.club/myOwn/High%20Interaction%20-%20remote%20backend%20pool.png" width="50%" ></img>
<br>
<div style="color:orange; border-bottom: 1px solid #d9d9d9;
display: inline-block;
color: #999;
padding: 2px;">Figure6: High Interation Mode - remote backend pool</div>
</center>

    # Where to deploy the backend pool (only if backend = pool)
    #  - "local": same machine as the proxy
    #  - "remote": set host and port of the pool below
    
    pool = local
    
    # Remote pool configurations (used with pool=remote)
    
    pool_host = 192.168.1.40
    pool_port = 6415

### Differences
* Simple Backend
  
    When using a simple backend, the proxy only provides forwarding. In other words, traffic sent to cowrie is forwarded through the proxy directly to the backend system. As a result, residual traces between different attackers contaminate each other. The original system image is also altered and a copy of the original snapshot of the system is not retained.
* Backend Pool
  
    Instead, with a backend pool, cowrie uses libvirt to manage all the VMs in the pool. For example, creating, destroying, saving snapshots, and assigning which VMs to attackers. In addition, to ensure the authenticity of high interactions, cowrie keeps track of different attackers (different IPs). When there is an attack from the same IP as before, it allocates its VMs that match the target of the last attack.

### Authentication

Regardless of the used type of backend, Cowrie will need credentials to access the machine. These can be of any account on it, as long as it supports password authentication.

Note that these are totally independent of the credentials attackers can use (as set in `userdb`). `userdb` credentials are the ones attackers may use to connect to Cowrie, while `backend_user` and `backend_pass` are used to connect Cowrie to the backend.
<center>
<img src="http://cdn.kient.club/myOwn/High%20Interaction%20-Authentication.png" width="80%" ></img>
<br>
<div style="color:orange; border-bottom: 1px solid #d9d9d9;
display: inline-block;
color: #999;
padding: 2px;">Figure7: High Interation Mode - Authentication</div>
</center>

**cowrie.cfg :**

    # ===============================
    # Proxy Configurations
    # ===============================
    
    # real credentials to log into backend
    
    backend_user = root
    
    backend_pass = root
**userdb.txt :** 

    # Example userdb.txt 
    # This file may be copied to etc/userdb.txt.
    # If etc/userdb.txt is not present, built-in defaults will be used.
    #
    # ':' separated fields, file is processed line for line
    # processing will stop on first match
    # 
    # Field #1 contains the username
    # Field #2 is currently unused
    # Field #3 contains the password 
    # '*' for any username or password
    # '!' at the start of a password will not grant this password access
    # '/' can be used to write a regular expression 
    #
    root:x:!root
    root:x:!123456
    root:x:!/honeypot/i
    root:x:*
    tomcat:x:*
    oracle:x:*
    *:x:somepassword
    *:x:*

## Backend Pool

The Backend Pool manages a set of dynamic backend virtual machines to be used by Cowrie’s proxy. The pool keeps a set of VMs running at all times, ensuring different attackers each see a “pristine” VM, while repeated connections from the same IP are served with the same VM, thus ensuring a consistent view to the attacker. Furthermore, VMs in the pool have their networking capabilities restricted by default: some attacks consist of downloading malicious software or accessing illegal content through insecure machines (such as your honeypot). Therefore, we limit any access to the Internet via a network filter, which you can configure as you see fit.

The VMs in the backend pool, and all infrastructure (snapshots, networking and filtering) are backed-up by Qemu/libvirt. We provide two example VM images (for Ubuntu Server 18.04 and OpenWRT 18.06.4) whose configurations are already set and ready to be deployed. Further below in this guide we’ll discuss how to create your own images and customise libvirt’s XML configuration files.

First of all, install the needed dependencies for the pool, as explained in the installation steps.

### Authorization

Add your cowrie user to the `libvirt` group to ensure you have permission to run the VMs on the backend server

    sudo usermod -aG libvirt "COWRIE_USER_HERE"
or

    sudo setfacl -m user:$USER:rw /var/run/libvirt/libvirt-sock    

### Provided images

To allow for a simple setup, we provide two VM images to use with the backend pool: Ubuntu 18.04 and OpenWRT. You can download them below, and then edit cowrie.cfg’s guest_image_path to match the path of the images. In the case of OpenWRT you will need two different files. Note that a separate set of configs is provided for each image in the default configuration. Choose the one you want to use and comment the other as needed.

* Ubuntu 18.04.<https://drive.google.com/open?id=1ZNE57lzaGWR427XxynqUVJ_2anTKmFmh>

* OpenWRT disk image.<https://drive.google.com/open?id=1oBAJc3FX82AkrIwv_GV0uO5R0SMl_i9Q>

* OpenWRT kernel image.<https://drive.google.com/open?id=17-UARwAd0aNB4Ogc4GvO2GsUSOSg0aaD>

### Backend Pool initialisation

Depending on the machine that will be running the backend pool, initialisation times for VMs can vary greatly. If the pool is correctly configured, you will get the PoolServerFactory starting on 6415 message on your log.

After a while, VMs will start to boot and, when ready to be used, a message of the form Guest 0 ready for connections @ 192.168.150.68! (boot 17s) will appear for each VM. Before VMs are ready, SSH and Telnet connections from attackers will be dropped by Cowrie.

### Backend Pool configuration

In this section we’ll discuss the `[backend_pool]` section of the configuration file.

The backend pool can be run in the same machine as the rest of Cowrie, or in a separate one. In the former case, you’d be running Cowrie with

    [backend_pool]
    
    # enable this to solely run the pool, regardless of other configurations (disables SSH and Telnet)
    
    pool_only = false
    
    [proxy]
    
    backend = pool
    
    pool = local

If you want to deploy the backend pool in a different machine, then you’ll need to invert the configuration: the pool machine has `pool_only = true` (SSH and Telnet are disabled), and the proxy machine has `pool = remote`.

Note: The communication protocol used between the proxy and the backend pool is unencrypted. Although no sensitive data should be passed, we recommend you to only use private or local interfaces for listening when setting up `listen_endpoints`.
## Analysing snapshots 

### Snapshot
VMs running in the pool are based on a base image that is kept unchanged. When booting, each VM creates a snaphost that keeps track of differences between the base image and snapshot. If you want to analyse snapshots and see any changes made in the VMs, set `save_snapshots` to true. If set to true be mindful of space concerns, each new VM will take at least ~20MB in storage.

**cowrie.cfg :**

    # guest snapshots
    save_snapshots = false
    snapshot_path = ${honeypot:state_path}/snapshots

One interesting aspect of Cowrie is the capability to analyse any downloaded malware and content into the honeypot. The snapshot mechanism can be leveraged to analyse any download and any change performed against the base image, to determine which files have been changed.

This guide shows how that can be achieved by leveraging using the `libguestfs-tools` package.

    sudo apt install libguestfs-tools
### Getting the a filesystem differences
The first step is getting the differences between each VM that was used and the base image provided. The tool we’ll be using is `virt-diff`, which provides a similar syntax to that of Unix’s `diff`.

    ~# sudo virt-diff -a /home/cowrie/cowrie-imgs/ubuntu18.04-minimal.qcow2      -A /home/cowrie/cowrie/var/lib/cowrie/snapshots/snapshot-ubuntu18.04-274a2092ea2c406c86bc3a40716aff68.qcow2 
    > /home/cowrie/cowrie-imgs/differ/diff.txt
The output will contain all changed files and their contents, which can easily become longer. The following command outputs the names of the changed files and ignores the system cache and temporary files for ease of reading.

    ~# grep -aE "^\+ |^- |^= " /home/cowrie/cowrie-imgs/differ/diff.txt 
    | grep -aEv "/tmp/systemd|/var/log|/var/lib|/var/cache"
    
    = - 0644       1024 /boot/grub/grubenv

## Correct performing log
The local backend pool is now used as the backend of the high interaction cowrie has been configured, cowrie and backend pool can be connected. 

    $ ssh root@164.155.129.69:2222
    
    Connecting to 164.155.129.69:2222...
    Connection established.
<br>    

    2023-08-14T15:14:33.922539Z [-] Python Version 3.8.10 (default, May 26 2023, 14:05:08) [GCC 9.4.0]
    2023-08-14T15:14:33.922645Z [-] Twisted Version 22.10.0
    2023-08-14T15:14:33.922677Z [-] Cowrie Version 2.5.0
    2023-08-14T15:14:33.924344Z [-] Loaded output engine: jsonlog
    2023-08-14T15:14:33.925277Z [cowrie.pool_interface.client.PoolClientFactory#info] Starting factory <cowrie.pool_interface.client.PoolClientFactory object at 0x7fafc58c1e50>
    2023-08-14T15:14:33.926870Z [twisted.scripts._twistd_unix.UnixAppLogger#info] twistd 22.10.0 (/home/cowrie/cowrie/cowrie-env/bin/python 3.8.10) starting up.
    2023-08-14T15:14:33.927002Z [twisted.scripts._twistd_unix.UnixAppLogger#info] reactor class: twisted.internet.epollreactor.EPollReactor.
    2023-08-14T15:14:33.939078Z [-] PoolServerFactory starting on 6415
    2023-08-14T15:14:33.940785Z [backend_pool.pool_server.PoolServerFactory#info] Starting factory <backend_pool.pool_server.PoolServerFactory object at 0x7fafc58c1ca0>
    2023-08-14T15:14:33.982662Z [-] Connection to QEMU established
    2023-08-14T15:14:33.984320Z [-] Could not get domain list
    2023-08-14T15:14:34.211933Z [backend_pool.pool_server.PoolServerFactory] Received connection from 127.0.0.1:51830
    2023-08-14T15:14:34.214195Z [Uninitialized] Initialising pool with Cowrie settings...
    2023-08-14T15:14:34.218567Z [PoolClient,client] VM pool fully initialised
    2023-08-14T15:14:34.220147Z [PoolClient,client] CowrieSSHFactory starting on 2222
    2023-08-14T15:14:34.220351Z [cowrie.ssh.factory.CowrieSSHFactory#info] Starting factory <cowrie.ssh.factory.CowrieSSHFactory object at 0x7fafc5826d00>
    2023-08-14T15:14:34.289935Z [PoolClient,client] Ready to accept SSH connections
    2023-08-14T15:14:36.248802Z [-] Guest cowrie-ubuntu18.04_051323fbe45b44eeb488e353bc57ce8a has booted
    2023-08-14T15:14:46.989185Z [-] Guest cowrie-ubuntu18.04_b10d1015b294468e924aa8a3385bd82b has booted
    2023-08-14T15:14:51.466751Z [-] Guest cowrie-ubuntu18.04_e04256ee2800448b87ef83676ad65f2c has booted
    2023-08-14T15:15:03.085295Z [-] Guest 0 ready for connections @ 192.168.150.42! (boot 26s)
    2023-08-14T15:15:11.687175Z [-] Guest 1 ready for connections @ 192.168.150.240! (boot 24s)
    2023-08-14T15:15:11.746686Z [-] Guest 2 ready for connections @ 192.168.150.117! (boot 20s)
    2023-08-14T15:15:25.978630Z [cowrie.ssh.factory.CowrieSSHFactory] New connection: 118.181.163.10:57182 (10.0.85.2:2222) [session: df97127f39ad]
    2023-08-14T15:15:25.981480Z [FrontendSSHTransport,0,118.181.163.10] Remote SSH version: SSH-2.0-nsssh2_7.0.0031 NetSarang Computer, Inc.
    2023-08-14T15:15:25.983722Z [backend_pool.pool_server.PoolServerFactory] Received connection from 127.0.0.1:55140
    2023-08-14T15:15:25.984454Z [Uninitialized] Connected to backend pool
    2023-08-14T15:15:25.985014Z [PoolServer,1,127.0.0.1] Requesting a VM for attacker @ 118.181.163.10
    2023-08-14T15:15:25.985314Z [PoolServer,1,127.0.0.1] Providing VM id 0
    2023-08-14T15:15:25.985823Z [PoolClient,client] Got backend data from pool: 192.168.150.42:22
    2023-08-14T15:15:25.986002Z [PoolClient,client] Snapshot file: /home/cowrie/cowrie/var/lib/cowrie/snapshots/snapshot-ubuntu18.04-051323fbe45b44eeb488e353bc57ce8a.qcow2
    2023-08-14T15:15:25.986392Z [cowrie.ssh_proxy.client_transport.BackendSSHFactory#info] Starting factory <cowrie.ssh_proxy.client_transport.BackendSSHFactory object at 0x7fafc1cc99a0>
    2023-08-14T15:15:25.988675Z [Uninitialized] Connected to SSH backend at b'192.168.150.42'
    2023-08-14T15:15:25.989178Z [Uninitialized] Connected to honeypot backend
    2023-08-14T15:15:25.997107Z [cowrie.ssh_proxy.client_transport.BackendSSHTransport#debug] kex alg=b'curve25519-sha256' key alg=b'ecdsa-sha2-nistp256'
    2023-08-14T15:15:25.997419Z [cowrie.ssh_proxy.client_transport.BackendSSHTransport#debug] outgoing: b'aes256-ctr' b'hmac-sha2-512' b'none'
    2023-08-14T15:15:25.997559Z [cowrie.ssh_proxy.client_transport.BackendSSHTransport#debug] incoming: b'aes256-ctr' b'hmac-sha2-512' b'none'
    2023-08-14T15:15:26.010057Z [cowrie.ssh_proxy.client_transport.BackendSSHTransport#debug] NEW KEYS
    2023-08-14T15:15:26.010394Z [BackendSSHTransport,client] Backend Connection Secured
    2023-08-14T15:15:26.010932Z [BackendSSHTransport,client] Connection to client not ready, buffering packet from backend
    2023-08-14T15:15:26.157272Z [FrontendSSHTransport,0,118.181.163.10] SSH client hassh fingerprint: 4b1924559bb5e98c572916eec086ee19
    2023-08-14T15:15:26.164622Z [cowrie.ssh_proxy.server_transport.FrontendSSHTransport#debug] kex alg=b'curve25519-sha256@libssh.org' key alg=b'ssh-rsa'
    2023-08-14T15:15:26.164815Z [cowrie.ssh_proxy.server_transport.FrontendSSHTransport#debug] outgoing: b'aes128-ctr' b'hmac-sha2-256' b'none'
    2023-08-14T15:15:26.164925Z [cowrie.ssh_proxy.server_transport.FrontendSSHTransport#debug] incoming: b'aes128-ctr' b'hmac-sha2-256' b'none'
    2023-08-14T15:15:26.869254Z [cowrie.ssh_proxy.server_transport.FrontendSSHTransport#debug] NEW KEYS
    2023-08-14T15:15:26.869938Z [cowrie.ssh_proxy.server_transport.FrontendSSHTransport#debug] starting service b'ssh-userauth'
    2023-08-14T15:15:27.039923Z [cowrie.ssh_proxy.userauth.ProxySSHAuthServer#debug] b'jack' trying auth b'none'
    2023-08-14T15:15:31.084136Z [cowrie.ssh_proxy.userauth.ProxySSHAuthServer#debug] b'jack' trying auth b'password'
    2023-08-14T15:15:31.097680Z [FrontendSSHTransport,0,118.181.163.10] login attempt [b'jack'/b'asdfg'] succeeded
    2023-08-14T15:15:31.099229Z [FrontendSSHTransport,0,118.181.163.10] Initialized emulated server as architecture: linux-x64-lsb
    2023-08-14T15:15:31.100659Z [FrontendSSHTransport,0,118.181.163.10] Will auth with backend: root/root
    2023-08-14T15:15:31.269648Z [FrontendSSHTransport,0,118.181.163.10] got channel b'session' request
    2023-08-14T15:15:31.855188Z [FrontendSSHTransport,0,118.181.163.10] [SSH] Unknown Channel Request Type Detected - x11-req
    2023-08-14T15:15:42.993771Z [cowrie.ssh_proxy.server_transport.FrontendSSHTransport#info] connection lost
    2023-08-14T15:15:42.994506Z [FrontendSSHTransport,0,118.181.163.10] Connection lost after 17 seconds
    2023-08-14T15:15:42.995410Z [BackendSSHTransport,client] Lost connection with the pool backend: id 0
    2023-08-14T15:15:42.995649Z [cowrie.ssh_proxy.client_transport.BackendSSHFactory#info] Stopping factory <cowrie.ssh_proxy.client_transport.BackendSSHFactory object at 0x7fafc1cc99a0>
    2023-08-14T15:15:42.996151Z [PoolServer,1,127.0.0.1] Freeing VM 0
    2023-08-14T15:38:52.216697Z [cowrie.ssh.factory.CowrieSSHFactory] New connection: 71.6.134.235:50896 (10.0.85.2:2222) [session: 0f3d46946986]
    2023-08-14T15:38:52.220559Z [FrontendSSHTransport,1,71.6.134.235] Remote SSH version: GET / HTTP/1.1
    2023-08-14T15:38:52.221326Z [FrontendSSHTransport,1,71.6.134.235] Bad protocol version identification: b'GET / HTTP/1.1'
    2023-08-14T15:38:52.222517Z [cowrie.ssh_proxy.server_transport.FrontendSSHTransport#info] connection lost





