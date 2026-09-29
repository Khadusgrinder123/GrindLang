from pathlib import Path
import subprocess

import Cgen
import NewLexer

grind_path = NewLexer.grind_path

c_code = Cgen.Output()

c_file_path = Path(grind_path).with_suffix('.c')
with open(c_file_path, 'w', encoding='utf-8') as f:
    f.write(c_code)

print(f"Generated: {c_file_path}")

answer = input("Convert to an executable and run it? [y/N]: ").strip().lower()
if answer in ("y", "yes"):
    executable_path = grind_path.with_suffix("")
    try:
        result = subprocess.run(
            ["gcc", str(c_file_path), "-o", str(executable_path)],
            check=False,
        )
    except FileNotFoundError:
        print("GCC was not found. Install GCC and make sure it is available on PATH.")
    else:
        if result.returncode != 0:
            print(f"GCC compilation failed (exit code {result.returncode}).")
        else:
            print(f"Generated executable: {executable_path}")
            subprocess.run([str(executable_path)], cwd=grind_path.parent, check=False)
        


print("\n\n if you made this executable then do ./{your executable name} to run it.")