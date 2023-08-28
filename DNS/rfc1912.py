from jinja2 import Template

rfc1912FileData = """
// named.rfc1912.zones:
//
// Provided by Red Hat caching-nameserver package 
//
// ISC BIND named zone configuration for zones recommended by
// RFC 1912 section 4.1 : localhost TLDs and address zones
// and http://www.ietf.org/internet-drafts/draft-ietf-dnsop-default-local-zones-02.txt
// (c)2007 R W Franks
// 
// See /usr/share/doc/bind*/sample/ for example named configuration files.
//

zone "localhost.localdomain" IN {
	type master;
	file "named.localhost";
	allow-update { none; };
};

zone "localhost" IN {
	type master;
	file "named.localhost";
	allow-update { none; };
};

zone "1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa" IN {
	type master;
	file "named.loopback";
	allow-update { none; };
};

zone "1.0.0.127.in-addr.arpa" IN {
	type master;
	file "named.loopback";
	allow-update { none; };
};

zone "0.in-addr.arpa" IN {
	type master;
	file "named.empty";
	allow-update { none; };
};

zone "{{forZone}}" IN {
        type master;
        file "{{forZone}}.for";
        allow-update { none; };
};

zone "{{revZone}}.in-addr.arpa" IN {
        type master;
        file "{{forZone}}.rev";
        allow-update { none; };
};

"""
def rfc1912Conf(forZone=None, revZone=None):
    if forZone and revZone:
        try:
            template = Template(rfc1912FileData)
            config = template.render(forZone=forZone, revZone=revZone)
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
    forZone = input("Enter Forward Zone Name Ex: example.com: ")
    revZone = input("Enter Reverse IP 3 octet Ex: 100.168.192: ")

    rfc1912Conf(forZone=forZone, revZone=revZone)