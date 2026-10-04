"""
Aptimizer Software Packaging Script
Packages the full Aptimizer suite into a clean, distributable ZIP archive
ready for deployment or transfer to any Windows, Linux, or Cloud environment.
"""

import os
import zipfile
import time

def make_zip():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    output_filename = os.path.join(root_dir, "Aptimizer_Software_Bundle.zip")
    
    # Exclude bulky temporary folders
    EXCLUDE_DIRS = {
        "node_modules",
        "__pycache__",
        ".pytest_cache",
        ".git",
        ".gemini",
        "tmp",
        "temp"
    }
    
    EXCLUDE_FILES = {
        "Aptimizer_Software_Bundle.zip",
        "Aptimizer_Software_Bundle_v2.4.zip",
        "backend_dev.log",
        "frontend_dev.log",
        "backend_output.log",
        "npm_output.log"
    }

    print(f"Creating software bundle: {output_filename}...")
    start_time = time.time()
    
    total_files = 0
    total_bytes = 0

    with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(root_dir):
            # Prune excluded directories in-place
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".")]

            for file in files:
                if file in EXCLUDE_FILES or file.endswith(".log") or file.endswith(".pyc"):
                    continue

                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, root_dir)
                
                # Filter out anything inside excluded directories
                parts = rel_path.split(os.sep)
                if any(p in EXCLUDE_DIRS for p in parts):
                    continue

                try:
                    fsize = os.path.getsize(full_path)
                    zipf.write(full_path, rel_path)
                    total_files += 1
                    total_bytes += fsize
                except Exception as e:
                    print(f"Warning: skipped {rel_path} ({e})")

    elapsed = time.time() - start_time
    zip_size_mb = os.path.getsize(output_filename) / (1024 * 1024)
    print(f"SUCCESS: Packaged {total_files} files ({total_bytes / (1024*1024):.1f} MB uncompressed) in {elapsed:.1f}s")
    print(f"Archive Size: {zip_size_mb:.2f} MB")
    print(f"Location: {output_filename}")

if __name__ == "__main__":
    make_zip()
