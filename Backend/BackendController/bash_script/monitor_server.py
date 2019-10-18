#!/usr/bin/env python3
import socket, time, json, datetime, platform, psutil, requests, pprint, uuid, sys

server_id = sys.argv[1]


def main():
    # Hostname Info
    hostname = socket.gethostname()
    #print("Hostname:", hostname)

    # CPU Info
    cpu_count = psutil.cpu_count()
    cpu_usage = psutil.cpu_percent(interval=1)
    #print("CPU:\n\tCount:", cpu_count, "\n\tUsage:", cpu_usage)

    # Memory Info
    
    memory_stats = psutil.virtual_memory()
    
    memory_total = memory_stats.total / (1024.0 ** 3)
    memory_used = memory_stats.used / (1024.0 ** 3)
    memory_used_percent = memory_stats.percent
    #print("Memory:\n\tPercent:", memory_used_percent, "\n\tTotal:", memory_total / 1e+6, "MB", "\n\tUsed:", memory_used / 1e+6, "MB")
    storage_total = 0
    storage_used = 0
    # Disk Info
    disk_info = psutil.disk_partitions()
    #print("Disks:")
    disks = []
    for x in disk_info:
        # Try fixes issues with connected 'disk' such as CD-ROMS, Phones, etc.
        try:
            disk = {
                "name" : x.device, 
                "mount_point" : x.mountpoint, 
                "type" : x.fstype, 
                "total_size" : psutil.disk_usage(x.mountpoint).total / (1024.0 ** 3), 
                "used_size" : psutil.virtual_memory(x.mountpoint).used / (1024.0 ** 3), 
                "percent_used" : psutil.disk_usage(x.mountpoint).percent
            }

            storage_total = storage_total+psutil.disk_usage(x.mountpoint).total
            storage_used = storage_used+psutil.disk_usage(x.mountpoint).used

            disks.append(disk)

            #print("\tDisk name",disk["name"], "\tMount Point:", disk["mount_point"], "\tType",disk["type"], "\tSize:", disk["total_size"] / 1e+9,"\tUsage:", disk["used_size"] / 1e+9, "\tPercent Used:", disk["percent_used"])
        except:
            print("")

    # Bandwidth Info 
    network_stats = get_bandwidth()
    #print("Network:\n\tTraffic in:",network_stats["traffic_in"] / 1e+6,"\n\tTraffic out:",network_stats["traffic_out"] / 1e+6)

    # Network Info
    nics = []
    print("NICs:")
    for name, snic_array in psutil.net_if_addrs().items():
        # Create NIC object
        nic = {
            "name": "sd",
            "mac": "",
            "address": "",
            "address6": "",
            "netmask": ""
        }
        # Get NiC values
        for snic in snic_array:
            if snic.family == -1:
                nic["mac"] = snic.address
            elif snic.family == 2:
                nic["address"] = snic.address
                nic["netmask"] = snic.netmask
            elif snic.family == 23:
                nic["address6"] = snic.address
        nics.append(nic)
        #print("\tNIC:",nic["name"], "\tMAC:", nic["mac"], "\tIPv4 Address:",nic["address"], "\tIPv4 Subnet:", nic["netmask"], "\tIPv6 Address:", nic["address6"])
    
    # Platform Info
    system = {
        "name" : platform.system(),
        "version" : platform.release()
    }
    #print("OS:\n\t",system["name"],system["version"])

    # Time Info
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")
    uptime = int(time.time() - psutil.boot_time())
    #print("System Uptime:\n\t",uptime)

    # System UUID
    sys_uuid = uuid.getnode()
	
    # Set Machine Info
    machine = {
    	"hostname" : hostname,
		"uuid" : sys_uuid,
        "system" : system,
        "uptime" : uptime,
    	"cpu_count" : cpu_count,
    	"cpu_usage" : cpu_usage,
    	"memory_total" : memory_total,
    	"memory_used" : memory_used,
    	"memory_used_percent" : memory_used_percent,
    	"drives" : disks,
        "storage_total" : storage_total,
        "storage_used" : storage_used,
    	"network_up" : network_stats["traffic_out"],
    	"network_down" : network_stats["traffic_in"],
        "network_cards": nics,
        "timestamp" : timestamp
    }

    data = json.dumps(machine)
    #print("\nData:")
    ##pprint.pprint(machine, indent=4)

    send_data(data)

def get_bandwidth():
    # Get net in/out
    net1_out = psutil.net_io_counters().bytes_sent
    net1_in = psutil.net_io_counters().bytes_recv

    time.sleep(1)

    # Get new net in/out
    net2_out = psutil.net_io_counters().bytes_sent
    net2_in = psutil.net_io_counters().bytes_recv

    # Compare and get current speed
    if net1_in > net2_in:
        current_in = 0
    else:
        current_in = net2_in - net1_in
    
    if net1_out > net2_out:
        current_out = 0
    else:
        current_out = net2_out - net1_out
    
    network = {"traffic_in" : current_in, "traffic_out" : current_out}
    return network

def send_data(data):
    # Attempt to send data up to 30 times
    try:
        endpoint = "http://127.0.0.1:8000/wpanel/"+ str(server_id) +"/api"
        
        requests.post(url = endpoint, data = json.loads(data))
    except:
        pass
while True:
    main()
    print("-----------------------------------------------------------------")
    time.sleep(5)