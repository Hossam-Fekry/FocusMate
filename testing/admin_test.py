import sys
import ctypes
import os


def is_admin():
    """Check if the current process has admin rights."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


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
    print("🚀 FocusMate Admin Test Started")

    if is_admin():
        print("✅ Running as ADMIN")
        print("Now you can safely modify system files like hosts file.")
        input("Press Enter to exit...")
    else:
        print("❌ Not admin yet")
        print("Requesting admin privileges...")

        run_as_admin()

        print("🔁 Relaunch requested. Closing current process.")


if __name__ == "__main__":
    main()