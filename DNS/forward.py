
forwardZoneFile = """
$TTL 1D
$ORIGIN aoneonlinebd.net.
@	IN SOA	ns1.aoneonlinebd.net. root.aoneonlinebd.net. (
					0	; serial
					1D	; refresh
					1H	; retry
					1W	; expire
					3H )	; minimum
@	IN	NS	ns1.aoneonlinebd.net.
@	IN	A	192.168.100.100
ns1	IN	A	192.168.100.100
router1	IN	A	103.175.130.1

"""