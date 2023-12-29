from serial import Serial
from time import sleep
from subprocess import run

# how to use:
#   replace the old.bin files in the binFiles folder with your own .bin files and the names should be "bootloader.bin", "boot_app0.bin", "partitions.bin", "upload.bin".
#   run the program

bootloader  = "binFiles/bootloader.bin"
partitions  = "binFiles/partitions.bin"
boot_app    = "binFiles/boot_app0.bin"
firmware    = "binFiles/firmware.bin"

esptool = "esptool.exe"

microController = "esp32"
COMport = "COM16"
baudrate = "460800"

upload_command = \
[
    esptool,                  
    "--chip", microController,
    "--port", COMport, 
    "--baud", baudrate, 
    "--before", "default_reset", #before upload
    "--after", "hard_reset",     #after upload
    
    "write_flash", 
    "-z", 
    "--flash_mode", "dio", #this mode makes GPIO 9/10 available (other modes use 9/10 for SPI flashing)
    "--flash_freq", "80m", #clock frequency of the flash
    "--flash_size", "4MB", # Size of the SPI flash, given in megabytes.
        "0x1000",  bootloader, 
        "0x8000",  partitions,            
        "0xe000",  boot_app, 
        "0x10000", firmware,
]

try:
    Serial(COMport, baudrate=int(baudrate)).close()
except:
    print("[connection_error] cant connect to COMPort: ", COMport)
    exit()
    
sleep(1)
result = run(upload_command, capture_output=True, text=True)

if result.returncode == 0:
    print("[upload_succes]")
else:
    print("[upload_error]", end=" ")
    print(result.stdout)