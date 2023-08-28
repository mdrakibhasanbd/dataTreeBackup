reversedZoneFile = """
$TTL 1D
$ORIGIN 100.168.192.in-addr.arpa.
@	IN SOA	ns1.aoneonlinebd.net. root.aoneonlinebd.net. (
					0	; serial
					1D	; refresh
					1H	; retry
					1W	; expire
					3H )	; minimum
	IN	NS	ns1.aoneonlinebd.net.
100 	IN 	PTR 	ns1.aoneonlinebd.net.
"""