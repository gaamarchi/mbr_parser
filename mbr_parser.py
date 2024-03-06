#!/bin/python3
import binascii
import socket
import argparse


def b(x):
    return x * 2


def convert_to_hex(file_path):
    with open(file_path, "rb") as f:
        content = f.read()
    return binascii.hexlify(content)


def have_boot_signature(content) -> bool:
    return hex_content[-b(2) :].decode() == "55aa"


def remove_unless_bytes(contet):
    return hex_content[b(446) : -b(2)]


def it_is_bootable(content):
    return content[: b(1)].decode() == "80"


def have_n_bytes(content, n):
    return len(content) == b(n)


def get_partition(clean_content):
    partition = []
    for i in range(4):
        init = i * b(16)
        end = init + b(16)
        partition.append(clean_content[init:end])

    return partition


def have_info(partition):
    # Use a função
    return set(partition) != {48}


def big_endian_to_little_endian(content, n):
    return socket.ntohl(int(content[b(n) : b(n + 4)].decode(), 16))


def file_system(partition):
    files_dict = {
        "00": "empty",
        "01": "FAT12",
        "04": "FAT16",
        "07": "NTFS",
        "83": "Linux",
        "a8": "MACOSX",
        "fb": "VMWARE_FILE_SYSTEM",
        "fc": "VMWARE_SWAP",
    }
    return files_dict.get(partition[b(4) : b(5)].decode(), "Unknown")


def calculate_size(partition):
    return big_endian_to_little_endian(partition, 12) * 512


argparse = argparse.ArgumentParser()
argparse.add_argument("-f", "--file", help="file to be parsed")
args = argparse.parse_args()


hex_content = convert_to_hex(args.file)
if not have_boot_signature(hex_content) or not have_n_bytes(hex_content, 512):
    print("Invalid MBR")
    exit(1)
clean_content = remove_unless_bytes(hex_content)

partitions = get_partition(clean_content)
for i in range(4):
    if have_info(partitions[i]):
        print(f"partition {i+1}")
        print(
            " ".join(
                partitions[i].decode()[j : j + 2]
                for j in range(0, len(partitions[i].decode()), 2)
            )
        )
        print("     is bootable [1byte]:", it_is_bootable(partitions[i]))
        print("     file system [5byte]:", file_system(partitions[i]))
        print(
            "     start sector [9-12byte]:",
            big_endian_to_little_endian(partitions[i], 8),
        )
        print(
            "     size in [13-16byte]: {:.4f} KB".format(
                calculate_size(partitions[i]) / 1024
            )
        )
        print(
            "     size in [13-16byte]: {:.4f} MB".format(
                calculate_size(partitions[i]) / 1024 / 1024
            )
        )
        print(
            "     size in [13-16byte]: {:.4f} GB".format(
                calculate_size(partitions[i]) / 1024 / 1024 / 1024
            )
        )
    else:
        print(f"partition {i+1} is empty")
