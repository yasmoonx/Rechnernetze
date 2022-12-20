# Wiresharkfilter: ip.src == 141.37.168.26 || ip.dst == 141.37.168.26 || udp.port == 1
#
# 2.
# 3. TCP Socket 7 liefert keine Antwort auf das Skript, da wir keine Nachricht schicken sondern nur eine Verbindung
#    aufbauen.
#    UDP Socket 7 liefert den Inhalt der gesandten Nachricht zurück.
