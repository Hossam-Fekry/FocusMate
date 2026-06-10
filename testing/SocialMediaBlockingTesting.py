import ctypes
import sys
import os

HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"

START_MARK = "# FOCUSMATE START"
END_MARK = "# FOCUSMATE END"

BLOCKED_SITES = [
    "127.0.0.1 facebook.com",
    "127.0.0.1 www.facebook.com",
    "127.0.0.1 instagram.com",
    "127.0.0.1 www.instagram.com",
    "127.0.0.1 tiktok.com",
    "127.0.0.1 www.tiktok.com",
]


def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()


def read_hosts():
    with open(HOSTS_PATH, "r", encoding="utf-8") as f:
        return f.readlines()


def write_hosts(lines):
    with open(HOSTS_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)


def block_sites():
    print("🚫 Blocking sites...")

    lines = read_hosts()

    # remove old block if exists
    new_lines = []
    inside_block = False

    for line in lines:
        if START_MARK in line:
            inside_block = True
            continue
        if END_MARK in line:
            inside_block = False
            continue
        if not inside_block:
            new_lines.append(line)

    # add new block section
    new_lines.append("\n" + START_MARK + "\n")
    for site in BLOCKED_SITES:
        new_lines.append(site + "\n")
    new_lines.append(END_MARK + "\n")

    write_hosts(new_lines)

    print("✅ Sites blocked successfully!")


def unblock_sites():
    print("🔓 Unblocking sites...")

    lines = read_hosts()

    new_lines = []
    inside_block = False

    for line in lines:
        if START_MARK in line:
            inside_block = True
            continue
        if END_MARK in line:
            inside_block = False
            continue
        if not inside_block:
            new_lines.append(line)

    write_hosts(new_lines)

    print("✅ Sites unblocked successfully!")


def run_as_admin():
    """Relaunch the script with admin privileges."""
    script = sys.argv[0]
    params = " ".join(sys.argv[1:])

    # ShellExecute with "runas" triggers UAC popup
    ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        sys.executable,
        f'"{script}" {params}',
        None,
        1
    )

def main():
    if not is_admin():
        print("❌ Asking for ")
        run_as_admin()

    print("🧪 FocusMate Hosts Test")
    print("1 - Block sites")
    print("2 - Unblock sites")

    choice = input("Choose: ")

    if choice == "1":
        block_sites()
    elif choice == "2":
        unblock_sites()
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()