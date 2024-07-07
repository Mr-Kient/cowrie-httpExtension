2023-07-19T10:54:38.338718Z [cowrie.ssh.factory.CowrieSSHFactory] **`New connection: 2.57.122.150:36496 (10.0.85.2:2222)`**[session: c996f4676594]

2023-07-19T10:54:38.343272Z [FrontendSSHTransport,12,2.57.122.150] Remote SSH version: SSH-2.0-Go

2023-07-19T10:54:38.344810Z [backend_pool.pool_server.PoolServerFactory] Received connection from 127.0.0.1:36302

2023-07-19T10:54:38.345416Z [Uninitialized] Connected to backend pool

2023-07-19T10:54:38.345892Z [PoolServer,13,127.0.0.1] **`Requesting a VM for attacker @ 2.57.122.150`**

2023-07-19T10:54:38.346102Z [PoolServer,13,127.0.0.1] **`Providing VM id 0`**

2023-07-19T10:54:38.346474Z [PoolClient,client] Got backend data from pool: 192.168.150.198:22

2023-07-19T10:54:38.346652Z [PoolClient,client] **`Snapshot file: /home/cowrie/cowrie/var/lib/cowrie/snapshots/snapshot-ubuntu18.04-ae5a43e18c6145f0b9beb121d0b0d4e9.qcow2`**

2023-07-19T10:54:38.346903Z [cowrie.ssh_proxy.client_transport.BackendSSHFactory#info] Starting factory <cowrie.ssh_proxy.client_transport.BackendSSHFactory object at 0x7fea0f8ba6d0>

2023-07-19T10:54:38.347855Z [Uninitialized] Connected to SSH backend at b'192.168.150.198'

2023-07-19T10:54:38.348161Z [Uninitialized] Connected to honeypot backend

2023-07-19T10:54:38.360959Z [cowrie.ssh_proxy.client_transport.BackendSSHTransport#debug] kex alg=b'curve25519-sha256' key alg=b'ecdsa-sha2-nistp256'

2023-07-19T10:54:38.361282Z [cowrie.ssh_proxy.client_transport.BackendSSHTransport#debug] outgoing: b'aes256-ctr' b'hmac-sha2-512' b'none'

2023-07-19T10:54:38.361424Z [cowrie.ssh_proxy.client_transport.BackendSSHTransport#debug] incoming: b'aes256-ctr' b'hmac-sha2-512' b'none'

2023-07-19T10:54:38.385882Z [cowrie.ssh_proxy.client_transport.BackendSSHTransport#debug] NEW KEYS

2023-07-19T10:54:38.386150Z [BackendSSHTransport,client] Backend Connection Secured

2023-07-19T10:54:38.386969Z [BackendSSHTransport,client] Connection to client not ready, buffering packet from backend

2023-07-19T10:54:38.519801Z [FrontendSSHTransport,12,2.57.122.150] SSH client hassh fingerprint: f301c693783020f3e7e575670465572c

2023-07-19T10:54:38.521350Z [cowrie.ssh_proxy.server_transport.FrontendSSHTransport#debug] kex alg=b'curve25519-sha256' key alg=b'ecdsa-sha2-nistp256'

2023-07-19T10:54:38.521488Z [cowrie.ssh_proxy.server_transport.FrontendSSHTransport#debug] outgoing: b'aes128-ctr' b'hmac-sha2-256' b'none'

2023-07-19T10:54:38.521610Z [cowrie.ssh_proxy.server_transport.FrontendSSHTransport#debug] incoming: b'aes128-ctr' b'hmac-sha2-256' b'none'

2023-07-19T10:54:38.698333Z [cowrie.ssh_proxy.server_transport.FrontendSSHTransport#debug] NEW KEYS

2023-07-19T10:54:38.699126Z [cowrie.ssh_proxy.server_transport.FrontendSSHTransport#debug] starting service b'ssh-userauth'

2023-07-19T10:54:38.877671Z [cowrie.ssh_proxy.userauth.
ProxySSHAuthServer#debug] b'root' trying auth b'none'

2023-07-19T10:54:39.059011Z [cowrie.ssh_proxy.userauth.ProxySSHAuthServer#debug] b'root' trying auth b'password'

2023-07-19T10:54:39.060759Z [FrontendSSHTransport,12,2.57.122.150] **`login attempt [b'root'/b'P@ssw0rd123!'] succeeded`**

2023-07-19T10:54:39.061695Z [FrontendSSHTransport,12,2.57.122.150] Initialized emulated server as architecture: linux-x64-lsb

2023-07-19T10:54:39.062577Z [FrontendSSHTransport,12,2.57.122.150] Will auth with backend: root/root

2023-07-19T10:54:39.243733Z [FrontendSSHTransport,12,2.57.122.150] got channel b'session' request

2023-07-19T10:54:39.601704Z [cowrie.ssh_proxy.server_transport.FrontendSSHTransport#info] connection lost

2023-07-19T10:54:39.602136Z [FrontendSSHTransport,12,2.57.122.150] Connection lost after 1 seconds