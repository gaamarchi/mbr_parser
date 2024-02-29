# Quick Start
clone the repo  
```
git clone https://github.com/gaamarchi/mbr_parser.git
```
enter on dir
```
cd mbr_parser
```
run script  
  With shebang
  ```
  chmod +x mbr_parser.py
  ```
  
  ```
  mbr_parser.py -f mbr_file
  ```


  Without shebang
 ```
  python3 mbr_parser.py -f mbr_file
  ```

# What is MBR

Master Boot Record is the information in the first sector of a disk, it is old form to initialize a disk and armazem partitions info  
the first 446 bytes are the bootloader. this code is responsible to load the OS in the disk.  
The other 64 bytes are the partitions table, the mbr support max of 4 partitions, each with 16 bytes  
the last 2 bytes are reserved to indicate whether the mbr is valid
