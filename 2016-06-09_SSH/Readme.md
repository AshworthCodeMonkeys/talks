# SSH & Key Management

## SSH (Secure Shell) :metal:

### SSH server

- We will only talk about client side of things, but before starting you must change some of your default `sshd_config` options to the following if you are enabling remote logins on your system. ***Please illuminate on further security measures, we can spare 5 minutes to it during discussions***

```
PermitRootLogin no
PasswordAuthentication no
ChallengeResponseAuthentication no
```

### SSH Client

- Usage is fairly simple

```bash
$ ssh user@server.domain
```

## SSH :key:

- You might want to create one and here's how you can do it

```bash
$ ssh-keygen -C "$(whoami)@$(hostname)-$(date -I)"
```

- If you are into different algorithms, there are options like **DSA** and **ECDSA** and you can do it using `ssh-keygen -t ecdsa`

- ***Please use password to encrypt your key***

- Copy your key to the remote machine

```bash
$ ssh-copy-id user@server.domain
```

- If you have multiple keys for multiple servers :thumbsup: you can specify it like this

```bash
$ ssh-copy-id -i ~/.ssh/id_rsa_server2 user@server2.domain
```

## Automatically :unlock: your :key: on login

- This step will differ based on what you choose
  - Use `ssh-agent`
  - Use PAM to unlock your key for you when you login *Remember your key password and login password should be same for this*
  - If you're in Ubuntu, use `seahorse` (the thing which will ask you to auto unlock when you log in)
  - :apple: will also have its own stuff but I don't know about it

# SSH Config and Tunelling

## Example config file

```
Host *
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 600
Host xyz
    HostName xyz.domain
    User user
    IdentityFile ~/.ssh/id_rsa_xyz
```    

## Tunnelling

- If you have to login via a gateway, you would have to login to the gateway and then login in your intended server

![img](http://i.imgur.com/MqSTNo9.png)

- How to do it automatically from `.ssh/config`?

```
Host gateway
  HostName gateway.server
  User user
  IdentityFile ~/.ssh/id_rsa
  ForwardX11 yes
Host secured_server
  HostName secured.server
  User user
  ProxyCommand ssh -W %h:%p gateway
  IdentityFile ~/.ssh/id_rsa
```

Now, when you want to connect to the secured_server

```
$ ssh secured_server
```

## SOCKS tunnel

- Get a VPN to avoid using your workstation for SOCKS tunnel. They are dirt cheap now a days...

- Lets say you want to connect to the internet but you are not connected to a secured network (e.g. :coffee:, central WiFi, random hackathon where you are overly paranoid)

```
$ ssh -TND 4711 server
```

- Now, change your proxy settings to point to `SOCKS5` and use the above mentioned `4711` port

# SCP, Rsync

- Do not use `scp`, use `rsync` instead (you know my allegiance)
- If you still want to use `scp`, stands for Secure Copy

```
$ scp user@server.domain:/path/to/file.ext /path/to/store/
```

- Things get interesting when you use `rsync`

![img](https://imgs.xkcd.com/comics/tar.png)

- `rsync` must be installed on both systems, by default it doesn't use encryption

```
$ rsync --avzP user@server.domain:/path/to/file.ext /path/to/store/
```

- Maybe, you want to use `rsync` over `ssh` by the following command

```
$ rsync --avzP -e ssh user@server.domain:/path/to/file.ext /path/to/store/
```

- ***Remember, if the directory is not present*** `rsync` ***creates it for you but*** `scp` ***will throw an error***

# SSHFS

- Mount your remote path to a local folder. Also, if you have set up stuff in your ssh config, you can use just the alias of the host. *It also mounts through a SSH tunnel, so make sure your config has necessary proxy commands for it*

```
$ sshfs user@server.domain:/remote/path /local/path -C -o idmap=user
```

- Unmount it using the following commands

```
$ fusermount -u /local/path
```

- If you want a GUI interface, use [`sftpman`](https://github.com/spantaleev/sftpman)

![img](https://raw.githubusercontent.com/spantaleev/sftpman-gtk/master/sftpman-gui.png)
