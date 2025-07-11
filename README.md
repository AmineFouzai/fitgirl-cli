# 🎮 FitGirl-Cli

A terminal-based CLI tool for browsing and interacting with FitGirl repacks and download links.

---

![FitGirl Logo](fit-girl.jpg)

## 🚀 Features

- Terminal UI with pagination using [Rich](https://github.com/Textualize/rich)
- Colored, interactive tables for links
- Read configuration (like base URL) from `config.ini`
- Open download links directly from terminal

---

## 🛠️ Installation (Development Mode)

Make sure you have **Python 3.7+** and **pip** installed.

### 1. Clone the repository

```bash
git clone https://github.com/yourname/fitgirl-cli.git

cd fitgirl-cli

pip install -e .  

```
```bash
fitgirl -h

FitGirl Repacks CLI

positional arguments:
  {status,newposts,search,download}
    status              Check if site is up
    newposts            List latest posts
    search              Search for repacks
    download            Interactive download

options:
  -h, --help            show this help message and exit

```


![Demo](demo.png)
