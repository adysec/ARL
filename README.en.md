[🇨🇳 简体中文](README.md) | [🇺🇸 English](README.en.md)

## ARL (Asset Reconnaissance Lighthouse) Asset Reconnaissance System

<a href="https://github.com/adysec/ARL/stargazers"><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/adysec/ARL?color=yellow&logo=riseup&logoColor=yellow&style=flat-square"></a>
<a href="https://github.com/adysec/ARL/network/members"><img alt="GitHub forks" src="https://img.shields.io/github/forks/adysec/ARL?color=orange&style=flat-square"></a>
<a href="https://github.com/adysec/ARL/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/adysec/ARL?color=red&style=flat-square"></a>

Backup project of the **ARL Asset Reconnaissance Lighthouse** system – **successfully running**.

---

### Overview

ARL is designed to quickly discover internet assets associated with a given target and to build a basic asset information database.  
It helps blue-team security engineers and penetration testers efficiently enumerate and search assets, and identify weak points and attack surfaces.

After the original ARL repository was deleted, this backup project reuses components such as `ARL-NPoC`, `arl_files`, etc.  
However, those projects no longer run out of the box. Most users previously ran ARL via Docker, but the original Docker images were also removed and can no longer be pulled, so the installation scripts and runtime environment had to be modified and debugged.

---

### Changes

1. **Use newer base images** – Updated to run on **CentOS 8** (the CentOS 7 inside the original Docker image cannot properly start `systemctl`).
2. **Single-container Docker mode** – Switched to a **single Docker image** runtime; no need to install `docker-compose` (for most people with a single server, strict front–back separation is unnecessary).
3. **CentOS repo via Cloudflare proxy** – Changed CentOS package repositories to use a Cloudflare mirror (official repos are extremely slow from home networks).
4. **PIP source via Cloudflare proxy** – Changed Python package source to a Cloudflare proxy (domestic servers often cannot reach the official PyPI).
5. **Integrated fingerprint libraries** – Added fingerprint data from multiple projects:  
   - `eHole` `1017`  
   - `ehole_magic` `24981`  
   - `EHole_magic_magic` `25715`  
   - `FingerprintHub` `2839`  
   - `dismap` `4598`  
   After deduplication, there are **`21545`** fingerprints.  
   You can update them manually using ARL’s exported format. New fingerprints can be submitted via issues, or you can directly modify the JSON file and reinstall via source inside the Docker container.  
   > Note: The **quick Docker install** does **not** include the `ehole_magic`-related fingerprints; after deduplication there are 5k+ entries, which can be updated manually.
6. **Use latest Nmap** – Nmap is upgraded to the latest version (if `yum` can install a newer version, there is no need to install an old one via RPM).
7. **Use latest Nuclei** – Nuclei is automatically updated daily via GitHub Actions.
8. **Tools moved under `tools/`** – `ARL-NPoC`, `arl_files`, `geoip` have all been moved into the `tools` directory (creating many separate repos is inconvenient; they are updated daily via GitHub Actions).
9. **Fix execution permissions** – Added executable permissions for tools (the original install script had issues; some tools weren’t executable and tasks would appear as `error`).
10. **Increase DB connection timeout** – Database connection timeout increased (many forks do this; in practice, the improvement is not obvious—original ARL still manages to run on 1C1G).
11. **Remove domain/IP segment limits** – Domain and IP range limitations were removed, and the `12000ms timeout` issue has been resolved (no one wants artificial limits on their own tools).
12. **Increase tool concurrency** – Concurrency for tools has been increased (most deployments run on cloud servers with enough performance; already tested).  
    > If you frequently experience timeouts after submitting a large number of tasks, please reduce concurrency via `arl-worker.service`.
13. **Use Cloudflare proxy for Docker Hub** – Docker’s official registry is currently unavailable from mainland networks for obvious reasons; a Cloudflare proxy is used instead.

---

### System Requirements

It is recommended to run ARL using **“source installation inside Docker”**.  

Suggested minimum server configuration:

- **CPU**: 4 vCPUs  
- **Memory**: 8 GB  
- **Bandwidth**: 10 Mbps  

Because automatic asset discovery involves a large volume of outbound traffic, using a cloud server usually provides a much better experience.

---

### Docker Installation (Quick Start)

```bash
docker run --privileged -it -d -p 5003:5003 --name=arl --restart=always docker.adysec.com/adysec/arl /usr/sbin/init
docker exec -it arl bash

# Run inside the container. The uploaded Docker image hides the hard-coded DB password,
# so you MUST reset credentials here.

rabbitmqctl start_app
# It is recommended to wait a bit before executing the following commands, otherwise errors may occur.
rabbitmqctl add_user arl arlpassword
rabbitmqctl add_vhost arlv2host
rabbitmqctl set_user_tags arl arltag
rabbitmqctl set_permissions -p arlv2host arl ".*" ".*" ".*"

cd /etc/systemd/system && systemctl restart arl*
exit
```

If you encounter MongoDB issues causing `timeout of 12000ms exceeded`, try adding the following mount when starting Docker:

```bash
-v /sys/fs/cgroup:/sys/fs/cgroup
```

---

### Source Installation Inside Docker (Latest Version, Requires Overseas Network)

> This method requires the Docker container to have **stable access to external (overseas) networks**.

```bash
docker run --privileged -it -d -p 5003:5003 --name=arl --restart=always docker.adysec.com/library/centos /usr/sbin/init
docker exec -it arl bash

# Inside the container, install ARL from source
curl https://raw.githubusercontent.com/adysec/ARL/master/misc/setup-arl.sh > install.sh
bash install.sh
exit
```

After execution inside the container, you can simply `exit` to leave.

On Ubuntu, you can install the Docker dependencies like this:

```bash
apt-get install docker.io docker-compose -y
```

---

### Source Installation (On Host)

The original ARL only supported **CentOS 7**; here it has been updated to **CentOS 8 only** (`centos:latest`).

If you install in another directory, you can create symbolic links as needed.  
The installation will create four services:

- `arl-web`  
- `arl-worker`  
- `arl-worker-github`  
- `arl-scheduler`

```bash
wget https://raw.githubusercontent.com/adysec/ARL/master/misc/setup-arl.sh
chmod +x setup-arl.sh
./setup-arl.sh
```

---

### DNS Brute-Force Optimization

Install `smartdns` on the **host machine** (example below is for Ubuntu):

```bash
apt install smartdns -y
curl https://github.com/adysec/ARL/raw/master/tools/smartdns.conf > /etc/smartdns/smartdns.conf
systemctl restart smartdns

docker exec -it arl bash
# Run inside the container
tee /etc/resolv.conf <<"EOF"
nameserver <HOST_IP_HERE>
nameserver 180.76.76.76
nameserver 4.2.2.1
nameserver 1.1.1.1
EOF
```

Replace `<HOST_IP_HERE>` with the IP address of your host (where `smartdns` is running).

---

### Check Service Status

```bash
systemctl status arl-web
systemctl status arl-worker
systemctl status arl-worker-github
systemctl status arl-scheduler
```

---

### ARL Maintenance / Modifications

```bash
# One-click remove (stop and delete container)
docker stop arl && docker rm arl

# Delete image
docker rmi arl

# Modify PoC – PoC directory: /opt/ARL-NPoC
docker exec -it arl bash
systemctl restart arl*

# Modify fingerprints – JSON path: /opt/ARL/tools/<fingerprint_data>.json
docker exec -it arl bash
cd /opt/ARL && python3.6 tools/add_finger.py
```

---

### Features

1. Domain asset discovery and aggregation  
2. IP / IP segment asset aggregation  
3. Port scanning and service identification  
4. Web site fingerprint identification  
5. Asset grouping and search  
6. Task policy configuration  
7. Scheduled and periodic tasks  
8. GitHub keyword monitoring  
9. Domain / IP asset monitoring  
10. Site change monitoring  
11. Detection of file leaks and similar risks  
12. Nuclei PoC integration  
13. [WebInfoHunter](https://tophanttechnology.github.io/ARL-doc/function_desc/web_info_hunter/) integration and monitoring  

---

### Screenshots

1. **Login page**  
   Default port: `5003` (HTTPS)  
   Default username/password: `admin / arlpass`  
   ![Login Page](./image/login.png)

2. **Task page**  
   ![Task Page](./image/task.png)

3. **Subdomain page**  
   ![Subdomain Page](./image/domain.png)

4. **Site page**  
   ![Site Page](./image/site.png)

5. **Asset monitoring page**  
   ![Asset Monitoring Page](./image/monitor.png)  
   For more details, see:  
   [Asset grouping and monitoring usage guide](https://github.com/TophantTechnology/ARL/wiki/%E8%B5%84%E4%BA%A7%E5%88%86%E7%BB%84%E5%92%8C%E7%9B%91%E6%8E%A7%E5%8A%9F%E8%83%BD%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E)

6. **Policy page**  
   ![Policy Configuration Page](./image/policy.png)

7. **Filter sites and dispatch tasks**  
   ![Filter Sites and Dispatch Tasks](./image/scan.png)  
   For more details, see:  
   [2.3 – New feature details](https://github.com/TophantTechnology/ARL/wiki/ARL-2.3-%E6%96%B0%E6%B7%BB%E5%8A%A0%E5%8A%9F%E8%83%BD%E8%AF%A6%E7%BB%86%E8%AF%B4%E6%98%8E)

8. **Scheduled tasks**  
   ![Scheduled Tasks](./image/task_scheduler.png)  
   For more details, see:  
   [2.4.1 – New feature details](https://github.com/TophantTechnology/ARL/wiki/ARL-2.4.1-%E6%96%B0%E6%B7%BB%E5%8A%9F%E8%83%BD%E8%AF%A6%E7%BB%86%E8%AF%B4%E6%98%8E)

9. **GitHub monitoring tasks**  
   ![GitHub Monitoring Tasks](./image/github_monitor.png)

---

### Task Options Description

| #  | Option                     | Description                                                                                         |
|----|----------------------------|-----------------------------------------------------------------------------------------------------|
| 1  | Task Name                  | Name of the task                                                                                    |
| 2  | Task Targets               | Targets of the task; supports IP, IP ranges and domains. Multiple targets can be submitted at once |
| 3  | Domain Brute-Force Level   | Dictionary size for domain brute-force. **Large**: commonly used ~20k entries. **Test**: only a few entries, used to verify functionality |
| 4  | Port Scan Type             | **ALL**: all ports; **TOP1000**: top 1000 common ports; **TOP100**: top 100 ports; **Test**: only a few ports |
| 5  | Enable Domain Brute-Force  | Whether to perform subdomain brute-force                                                            |
| 6  | Smart DNS Dictionary       | Generate brute-force dictionaries based on existing domains                                         |
| 7  | Domain Query Plugins       | Supported data sources (currently 13), such as `alienvault`, `certspotter`, `crtsh`, `fofa`, `hunter`, etc. |
| 8  | ARL History Query          | Query historical ARL task results and reuse them in the current task                               |
| 9  | Port Scanning              | Whether to perform port scanning. If disabled, only ports 80 and 443 will be probed for sites      |
| 10 | Service Identification     | Whether to perform service fingerprinting (may be blocked by firewalls, resulting in empty results)|
| 11 | OS Identification          | Whether to perform OS fingerprinting (may be blocked by firewalls, resulting in empty results)      |
| 12 | SSL Certificate Collection | Retrieve SSL certificates on the scanned ports                                                      |
| 13 | Skip CDN                   | For IPs identified as CDN, ports will not be scanned; ports 80 and 443 are assumed open            |
| 14 | Site Fingerprinting        | Perform fingerprint detection on sites                                                              |
| 15 | Search Engine Integration  | Use search engines to crawl URLs and subdomains related to the targets                             |
| 16 | Site Crawler               | Use a static crawler to crawl URLs for each site                                                   |
| 17 | Site Screenshot            | Take screenshots of site homepages                                                                  |
| 18 | File Leak Detection        | Detect file leaks on sites (may be blocked by WAF)                                                 |
| 19 | Host Collision             | Detect misconfigured virtual hosts (VHost)                                                          |
| 20 | Nuclei Integration         | Use Nuclei with default PoCs to scan sites (likely to be blocked by WAF—use with caution)          |
| 21 | WIH Integration            | Use WebInfoHunter (WIH) to extract domains, AK/SK and other info from JavaScript                   |
| 22 | WIH Monitoring Tasks       | Periodically call WebInfoHunter on sites within asset groups to monitor JS and related information |

---

### FAQ

Please refer to the official [FAQ](https://tophanttechnology.github.io/ARL-doc/faq/).

