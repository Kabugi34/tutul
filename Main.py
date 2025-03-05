import os
import argparse
import time
from termcolor import colored
import json


def display_banner():
    banner = """
    
▄▄▄█████▓ █    ██ ▄▄▄█████▓ █    ██  ██▓    
▓  ██▒ ▓▒ ██  ▓██▒▓  ██▒ ▓▒ ██  ▓██▒▓██▒    
▒ ▓██░ ▒░▓██  ▒██░▒ ▓██░ ▒░▓██  ▒██░▒██░    
░ ▓██▓ ░ ▓▓█  ░██░░ ▓██▓ ░ ▓▓█  ░██░▒██░    
  ▒██▒ ░ ▒▒█████▓   ▒██▒ ░ ▒▒█████▓ ░██████▒
  ▒ ░░   ░▒▓▒ ▒ ▒   ▒ ░░   ░▒▓▒ ▒ ▒ ░ ▒░▓  ░
    ░    ░░▒░ ░ ░     ░    ░░▒░ ░ ░ ░ ░ ▒  ░
  ░       ░░░ ░ ░   ░       ░░░ ░ ░   ░ ░   
            ░                 ░         ░  ░
                                                    
    """
    print(colored(banner, color='cyan'))
display_banner()

def init_parser():
    parser = argparse.ArgumentParser(
        prog="Tutul",
        description="A python tool to parse images in pdf and transform to text, csv, or json",
        usage="tutul [-h] [-f] --csv --json --text --out"
    )

    parser.add_argument("-c", "--csv", action="store_true", help="Output in CSV format")
    parser.add_argument("-j", "--json", action="store_true", help="Output in JSON format")
    parser.add_argument("-t", "--text", action="store_true", help="Output in text format")
    parser.add_argument("-o", "--out", help="Enter the name of the file to write to")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true")
    group.add_argument("-q", "--quiet", action="store_true")
    
    return parser

def parse_arguments(parser):
    return parser.parse_args()

def determine_output_formats(args):
    output_formats = []
    if args.csv:
        output_formats.append("CSV")
    if args.json:
        output_formats.append("JSON")
    if args.text:
        output_formats.append("Text")
    return output_formats

def handle_output(args, output_formats):
    if not output_formats:
        print("No output format selected. Please choose at least one format (--csv, --json, or --text).", flush=True)
        
        exit()
    
    if args.quiet:
        print(", ".join(output_formats) if output_formats else "No output format selected", flush=True)
    elif args.verbose:
        print(f'''
              {colored('[+]', color='green')} Verbose flag is on
              Selected output formats: {", ".join(output_formats) if output_formats else "None"}
              {'--------' * 20}
              ''', flush=True)
    else:
        print(f"Selected output formats: {', '.join(output_formats) if output_formats else 'None'}", flush=True)

def write_to_file(args, output_formats):
    if args.out:
        with open(args.out, 'w') as file:
            if args.csv:
                file.write("This is CSV content.\n")
            if args.json:
                file.write("{'key': 'value'}\n")
            if args.text:
                file.write("This is text output.\n")
            print(f"Output written to {args.out}", flush=True)
    else:
        if args.csv:
            print("CSV Output:", flush=True)
            print("This is CSV content.", flush=True)
        if args.json:
            print("JSON Output:", flush=True)
            print(colored('[+]', color="light_yellow"),"JSON flagged :", args.json, flush=True)
            # print(json_string,flush=True,sep='s')

            print("{'key': 'value'}", flush=True)
        if args.text:
            print(colored('[+] ', color='light_cyan'), f'{args.text}', flush=True)
            text = "Hello, world!"
            
def main():
    parser = init_parser()
    args = parse_arguments(parser)
    output_formats = determine_output_formats(args)
    handle_output(args, output_formats)
    write_to_file(args, output_formats)

if __name__ == "__main__":
    main()
