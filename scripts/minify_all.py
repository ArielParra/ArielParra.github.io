#!/usr/bin/env python3
import glob
import subprocess
import os
import sys


def main():
    print("Starting minification...")
    files_to_minify = glob.glob("css/*.css") + glob.glob("js/*.js")
    for f in files_to_minify:
        if ".min." in f:
            continue

        if f.endswith(".css"):
            out_file = f.replace(".css", ".min.css")
        else:
            out_file = f.replace(".js", ".min.js")

        print(f"Minifying {f} -> {out_file}")

        # Use npx minify
        npx_cmd = "npx.exe" if os.name == 'nt' else "npx"
        try:
            if f.endswith(".css"):
                subprocess.run([npx_cmd, "-y", "cleancss", "-o", out_file, f], check=True)
            else:
                subprocess.run([npx_cmd, "-y", "terser", f, "-o", out_file], check=True)
        except Exception as e:
            print(f"Error minifying {f}: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
