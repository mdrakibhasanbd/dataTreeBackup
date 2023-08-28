
from jinja2 import Template
namedFileData = """
//
// named.conf
//
// Provided by Red Hat bind package to configure the ISC BIND named(8) DNS
// server as a caching only nameserver (as a localhost DNS resolver only).
//
// See /usr/share/doc/bind*/sample/ for example named configuration files.
//
// See the BIND Administrator's Reference Manual (ARM) for details about the
// configuration located in /usr/share/doc/bind-{version}/Bv9ARM.html

options {
	listen-on port 53 { 127.0.0.1; {{hostIp}}; };
	listen-on-v6 port 53 { ::1; };
	directory 	"/var/named";
	dump-file 	"/var/named/data/cache_dump.db";
	statistics-file "/var/named/data/named_stats.txt";
	memstatistics-file "/var/named/data/named_mem_stats.txt";
	recursing-file  "/var/named/data/named.recursing";
	secroots-file   "/var/named/data/named.secroots";
	allow-query     { localhost; {{allow_query}}; };

	/* 
	 - If you are building an AUTHORITATIVE DNS server, do NOT enable recursion.
	 - If you are building a RECURSIVE (caching) DNS server, you need to enable 
	   recursion. 
	 - If your recursive DNS server has a public IP address, you MUST enable access 
	   control to limit queries to your legitimate users. Failing to do so will
	   cause your server to become part of large scale DNS amplification 
	   attacks. Implementing BCP38 within your network would greatly
	   reduce such attack surface 
	*/
	recursion yes;

	dnssec-enable yes;
	dnssec-validation no;

	/* Path to ISC DLV key */
	bindkeys-file "/etc/named.root.key";

	managed-keys-directory "/var/named/dynamic";

	pid-file "/run/named/named.pid";
	session-keyfile "/run/named/session.key";
};

logging {
        channel default_debug {
                file "data/named.run";
                severity dynamic;
        };
};

zone "." IN {
	type hint;
	file "named.ca";
};

include "/etc/named.rfc1912.zones";
include "/etc/named.root.key";
"""


def nameConf(hostIp=None, allow_query=None):
    if not hostIp:
        hostIp = "any"
    if not allow_query:
        allow_query = "any"

    try:
        template = Template(namedFileData)
        config = template.render(hostIp=hostIp, allow_query=allow_query)
        print(config)
        filename = "named.conf"
        # Uncomment the following block after ensuring you have the necessary permissions.
        # with open("/etc/named.conf", "w", encoding='utf-8') as f:
        #     f.write(config)
        print(f"File '{filename}' edited successfully.")
    except PermissionError:
        print("Error: Permission denied. Please run the program as a root user.")
    except Exception as e:
        print(f"Error creating the file: {e}")

if __name__ == "__main__":
    hostIp = input("Enter Host Machine IP Address: ")
    allow_query = input("Enter Allow_query Subnet Ex: 192.168.0.0/24 : ")

    nameConf(hostIp=hostIp, allow_query=allow_query)
