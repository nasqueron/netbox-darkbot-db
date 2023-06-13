#!/usr/bin/env python3

#   -------------------------------------------------------------
#   Darkbot NetBox database
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Project:        Nasqueron
#   Description:    Reads queries from NetBox database (in CSV)
#                   Write Darkbot .db database
#   License:        BSD-2-Clause
#   -------------------------------------------------------------


import csv
import sys


#   -------------------------------------------------------------
#   Rows to darkbot
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def print_reverse(rows, skip_first=False):
    """List of lists [address, dns_name, description, status] into Darkbot entries"""
    all_entries = {}
    for address, dns_name, description, status in rows:
        if skip_first:
            skip_first = False
            continue

        if dns_name == "":
            continue

        entry = clean_ip(address)

        if status != "active":
            entry += f" [{status}]"

        if dns_name not in all_entries:
            all_entries[dns_name] = []
        all_entries[dns_name].append(entry)

    for dns_name, entries in all_entries.items():
        line = f"{dns_name} "
        line += " / ".join(entries)

        print(line)


def print_ips(rows, skip_first=False):
    """List of lists [address, dns_name, description, status] into Darkbot entries"""
    for address, dns_name, description, status in rows:
        if skip_first:
            skip_first = False
            continue

        line = clean_ip(address) + " "

        stack = []

        if not is_clean_ip(address):
            stack.append(address)

        if dns_name != "":
            stack.append(dns_name)

        if description != "":
            stack.append(description)

        if len(stack) > 0:
            line += " / ".join(stack)
        else:
            line += "Undocumented IP on NetBox"

        if status != "active":
            line += f" [{status}]"

        print(line)


def clean_ip(ip):
    return ip.split("/")[0]


def is_clean_ip(ip):
    return "/" not in ip


#   -------------------------------------------------------------
#   Application entry point
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def run(content_type, ips_file):
    """CSV to darkbot database"""
    with open(ips_file) as fd:
        rows = [row for row in csv.reader(fd)]

    if content_type == "ips":
        print_ips(rows, True)
    elif content_type == "reverse":
        print_reverse(rows, True)
    else:
        print(f"Unknown content type: {content_type}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    argc = len(sys.argv)

    if argc < 3:
        print(f"Usage: {sys.argv[0]} <content type> <Netbox CSV file>", file=sys.stderr)
        print("Supported content types are: ips, reverse", file=sys.stderr)
        sys.exit(1)

    run(sys.argv[1], sys.argv[2])
