# fitgirl/parser.py

import re


def parse_search_results(html, exclude_upcoming=False)->dict:
    results = re.findall(
        r'<h1 class="entry-title"><a href="(.+?)" rel="bookmark">(.+?)</a></h1>', html
    )
    if exclude_upcoming:
        results = [r for r in results if "Upcoming Repacks" not in r[1]]

    if not results:
        return {"status": "Error", "message": "No results found."}

    return {
        "status": "Success",
        "results": [{"url": url, "title": title} for url, title in results],
    }


def parse_download_sections(html):
    def extract_section(title):
        pattern = rf"<h3>{re.escape(title)}</h3>(.+?)</ul>"
        match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
        return (
            re.findall(
                r'<li>\s*<a href="(.+?)"[^>]*>(.+?)</a>', match.group(1), re.IGNORECASE
            )
            if match
            else []
        )

    def extract_updates():
        match = re.search(
            r"<h3>Game Updates.*?</h3>(.+?)<p>", html, re.DOTALL | re.IGNORECASE
        )
        return (
            re.findall(r'<a href="(.+?)"[^>]*>(.+?)</a>', match.group(1), re.IGNORECASE)
            if match
            else []
        )

    return {
        "HTTP Mirrors": extract_section("Download Mirrors"),
        "Torrent Mirrors": extract_section("Download Mirrors (Torrent)"),
        "Game Updates": extract_updates(),
    }
