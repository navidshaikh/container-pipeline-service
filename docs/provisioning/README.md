This will allow you to bring up a single or multi-node setup of the Container Pipeline Service.

We use Ansible Playbooks in order to provision the service. As long as your OS is accesible over SSH, you can set up the host(s):

```sh
$ git clone https://github.com/CentOS/container-pipeline-service/
$ cd container-pipeline-service/provisions

# Copy sample hosts file and edit as needed
$ cp hosts.sample hosts
```

You can either have this span multiple-hosts or you can have an all-in-one setup by using the same host value in the `hosts` file.

**An SSL certificate is required on the host running the registry:**

Replace `registry.domain.com` with your own.

```bash
$ export REGISTRY=registry.domain.com
$ cd /etc/pki/tls/
$ openssl genrsa -out private/$REGISTRY.key 2048
$ openssl req -x509 -days 366 -new -key private/$REGISTRY.key -out certs/$REGISTRY.pem
```

**Provision using Ansible:**

```sh
# Provision the hosts. This assumes that you have added the usernames,
# passwords or private keys used to access the hosts in the hosts file
$ ansible-playbook -i hosts main.yml
```

