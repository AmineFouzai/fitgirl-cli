# main.py

import argparse
from core.client import FitGirlClient
from utils.display import prompt_open_links, interactive_download_prompt,show_status_response


def main():
    parser = argparse.ArgumentParser(description="FitGirl Repacks CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status", help="Check if site is up")
    subparsers.add_parser("newposts", help="List latest posts")

    search_parser = subparsers.add_parser("search", help="Search for repacks")
    search_parser.add_argument("query")

    download_parser = subparsers.add_parser("download", help="Interactive download")
    download_parser.add_argument("query")

    args = parser.parse_args()
    client = FitGirlClient()

    match args.command:
        case "status":
            result = client.check_status()
            show_status_response(result)
        case "search":
            result = client.search(args.query)
            if result["status"] == "Success":
                prompt_open_links(result["results"])
            else:
                print(f"[red]{result['message']}[/red]")
        case "download":
            result = client.download_interactive(args.query)
            interactive_download_prompt(result)
        case "newposts":
            result = client.new_posts()
            if result["status"] == "Success":
                prompt_open_links(result["results"])
            else:
                print(f"[red]{result['message']}[/red]")


if __name__ == "__main__":
    main()
