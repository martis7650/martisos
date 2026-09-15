"""
MartisOS
Copyright (c) 2026 Martin Sláčala
Licensed under the MIT License.
"""

import os
import sys
import json
import shutil
import urllib.request

class MartisOS:
    def __init__(self):
        self.memory_file = "memory.txt"
        self.root_dir = os.path.abspath("MartisOS_Root")
        
        self.users = {}
        self.current_user = None
        self.current_dir = ""
        
        self.load_memory()

    def load_memory(self):
        if not os.path.exists(self.memory_file) or os.path.getsize(self.memory_file) == 0:
            print("=== PRVNÍ SPUŠTĚNÍ MARTISOS ===")
            print("Vytvářím systémovou paměť (memory.txt)...")
            username, password = self.setup_first_user()
            
            self.users = {username: password}
            self.current_user = username
            
            user_home = os.path.join(self.root_dir, username)
            os.makedirs(user_home, exist_ok=True)
            self.current_dir = f"/{username}"
            
            self.save_memory()
        else:
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.users = data.get("users", {})
                print("Paměť úspěšně načtena.")
                self.login_screen()
            except Exception as e:
                print(f"Chyba při čtení memory.txt: {e}")
                sys.exit(1)

    def save_memory(self):
        data = {"users": self.users}
        try:
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print("[Systém] Paměť byla úspěšně uložena do memory.txt.")
        except Exception as e:
            print(f"[Chyba] Nepodařilo se uložit memory.txt: {e}")

    def setup_first_user(self):
        print("Vítej v MartisOS! Musíme vytvořit prvního administrátora.")
        username = input("Zadej uživatelské jméno: ").strip()
        while not username:
            username = input("Jméno nemůže být prázdné. Zadej uživatelské jméno: ").strip()
            
        password = input("Zadej heslo: ").strip()
        return username, password

    def login_screen(self):
        print("\n=== PŘIHLÁŠENÍ DO MARTISOS ===")
        while True:
            username = input("Uživatelské jméno: ").strip()
            password = input("Heslo: ").strip()
            
            if username in self.users and self.users[username] == password:
                self.current_user = username
                user_folder = os.path.join(self.root_dir, username)
                os.makedirs(user_folder, exist_ok=True)
                self.current_dir = f"/{username}"
                print(f"Přihlášen jako {username}.\n")
                break
            else:
                print("Chybné jméno nebo heslo. Zkus to znovu.\n")

    def get_full_path(self, path_arg):
        if path_arg.startswith("/"):
            clean_path = path_arg.lstrip("/")
        else:
            current_rel = self.current_dir.lstrip("/")
            if current_rel == "":
                clean_path = path_arg
            else:
                clean_path = os.path.join(current_rel, path_arg)
        
        return os.path.join(self.root_dir, clean_path)

    def run(self):
        try:
            while True:
                prompt = f"{self.current_user}@martisos:{self.current_dir}$ "
                try:
                    command_line = input(prompt).strip()
                except (KeyboardInterrupt, EOFError):
                    print("\nNucené přerušení, ukládám systém a končím...")
                    self.save_memory()
                    break

                if not command_line:
                    continue

                parts = command_line.split(" ")
                cmd = parts[0]
                args = parts[1:]

                if cmd == "exit":
                    print("Ukládám systémová data do memory.txt...")
                    self.save_memory()
                    print("Vypínám MartisOS. Sbohem!")
                    break
                elif cmd == "help":
                    self.cmd_help()
                elif cmd == "ls":
                    self.cmd_ls()
                elif cmd == "pwd":
                    print(self.current_dir)
                elif cmd == "cd":
                    self.cmd_cd(args[0] if args else "")
                elif cmd == "mkdir":
                    if args:
                        self.cmd_mkdir(args[0])
                    else:
                        print("Použití: mkdir <název_složky>")
                elif cmd == "cat":
                    if args:
                        self.cmd_cat(args[0])
                    else:
                        print("Použití: cat <soubor>")
                elif cmd == "nano":
                    if args:
                        self.cmd_nano(args[0])
                    else:
                        print("Použití: nano <soubor>")
                elif cmd == "cp":
                    if len(args) >= 2:
                        self.cmd_cp(args[0], args[1])
                    else:
                        print("Použití: cp <zdroj> <cíl>")
                elif cmd == "mv":
                    if len(args) >= 2:
                        self.cmd_mv(args[0], args[1])
                    else:
                        print("Použití: mv <zdroj> <cíl>")
                elif cmd == "rm":
                    if args:
                        self.cmd_rm(args[0])
                    else:
                        print("Použití: rm <soubor_nebo_složka>")
                elif cmd == "clear":
                    os.system('cls' if os.name == 'nt' else 'clear')
                elif cmd == "addusr":
                    self.cmd_addusr()
                elif cmd == "dluser":
                    self.cmd_dluser()
                elif cmd == "apt":
                    if len(args) >= 2 and args[0] == "install":
                        self.cmd_apt_install(args[1])
                    else:
                        print("Použití: apt install <nazev_balicku>")
                elif cmd == "pm":
                    self.cmd_pymartis(args)
                else:
                    print(f"Neznámý příkaz: {cmd}. Napiš 'help' pro nápovědu.")
        except Exception as e:
            print(f"Neočekávaná chyba v běhu systému: {e}")
            self.save_memory()

    def cmd_help(self):
        print("Dostupné příkazy v MartisOS:")
        print("  help                    - Zobrazí nápovědu")
        print("  ls                      - Vypíše obsah aktuálního adresáře")
        print("  pwd                     - Zobrazí aktuální cestu")
        print("  cd <složka>             - Změní adresář (.. pro návrat)")
        print("  mkdir <složka>          - Vytvoří novou složku")
        print("  cat <soubor>            - Zobrazí obsah souboru")
        print("  nano <soubor>           - Vytvoří nebo upraví soubor")
        print("  cp <zdroj> <cíl>        - Zkopíruje soubor")
        print("  mv <zdroj> <cíl>        - Přesune nebo přejmenuje soubor")
        print("  rm <cesta>              - Smaže soubor nebo prázdnou složku")
        print("  clear                   - Vymaže obrazovku")
        print("  addusr                  - Přidá nového uživatele")
        print("  dluser                  - Smaže uživatele")
        print("  apt install <balíček>   - Stáhne aplikaci z repozitáře")
        print("  pm <příkaz>             - Práce s PyMartis kódem (mk, nano, run)")
        print("  exit                    - Uloží data a vypne MartisOS")

    def cmd_ls(self):
        real_path = self.get_full_path("")
        if os.path.exists(real_path):
            print("  ".join(os.listdir(real_path)))
        else:
            print("Chyba: Adresář neexistuje.")

    def cmd_pwd(self):
        print(self.current_dir)

    def cmd_cd(self, path):
        if not path:
            return
        if path == "..":
            if self.current_dir != "/":
                parent = os.path.dirname(self.current_dir)
                self.current_dir = parent if parent else "/"
            return

        new_virt_path = os.path.join(self.current_dir, path).replace("\\", "/")
        real_path = self.get_full_path(path)
        
        if os.path.exists(real_path) and os.path.isdir(real_path):
            self.current_dir = new_virt_path
        else:
            print(f"Chyba: Složka '{path}' nebyla nalezena.")

    def cmd_mkdir(self, dirname):
        try:
            os.makedirs(self.get_full_path(dirname), exist_ok=True)
            print(f"Složka '{dirname}' byla vytvořena.")
        except Exception as e:
            print(f"Chyba při vytváření složky: {e}")

    def cmd_cat(self, filename):
        real_path = self.get_full_path(filename)
        if os.path.exists(real_path) and os.path.isfile(real_path):
            with open(real_path, "r", encoding="utf-8") as f:
                print(f.read())
        else:
            print(f"Chyba: Soubor '{filename}' nebyl nalezen.")

    def cmd_nano(self, filename):
        real_path = self.get_full_path(filename)
        print(f"--- Editor Nano (upravuješ: {filename}) ---")
        print("Zadej text. Na novém řádku napiš ':wq' pro uložení a ukončení, nebo ':q' pro zrušení.")
        
        existing_content = ""
        if os.path.exists(real_path) and os.path.isfile(real_path):
            with open(real_path, "r", encoding="utf-8") as f:
                existing_content = f.read()

        lines = existing_content.splitlines() if existing_content else []

        while True:
            line = input()
            if line == ":wq":
                with open(real_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(lines) + ("\n" if lines else ""))
                print(f"Soubor '{filename}' byl uložen.")
                break
            elif line == ":q":
                print("Zrušeno bez uložení.")
                break
            else:
                lines.append(line)

    def cmd_cp(self, src, dest):
        real_src, real_dest = self.get_full_path(src), self.get_full_path(dest)
        if not os.path.exists(real_src):
            print(f"Chyba: Zdroj '{src}' neexistuje.")
            return
        try:
            if os.path.isdir(real_src):
                shutil.copytree(real_src, real_dest, dirs_exist_ok=True)
            else:
                shutil.copy(real_src, real_dest)
            print(f"Úspěšně zkopírováno.")
        except Exception as e:
            print(f"Chyba při kopírování: {e}")

    def cmd_mv(self, src, dest):
        real_src, real_dest = self.get_full_path(src), self.get_full_path(dest)
        if not os.path.exists(real_src):
            print(f"Chyba: Zdroj '{src}' neexistuje.")
            return
        try:
            shutil.move(real_src, real_dest)
            print("Úspěšně přesunuto.")
        except Exception as e:
            print(f"Chyba při přesouvání: {e}")

    def cmd_rm(self, target):
        real_path = self.get_full_path(target)
        if not os.path.exists(real_path):
            print(f"Chyba: Položka '{target}' neexistuje.")
            return
        if os.path.isfile(real_path):
            os.remove(real_path)
            print(f"Soubor '{target}' smazán.")
        elif os.path.isdir(real_path):
            try:
                os.rmdir(real_path)
                print(f"Složka '{target}' smazána.")
            except OSError:
                print("Chyba: Složka není prázdná.")

    def cmd_addusr(self):
        print("--- Přidání nového uživatele ---")
        new_user = input("Zadej jméno nového uživatele: ").strip()
        if not new_user or new_user in self.users:
            print("Neplatné nebo již existující jméno.")
            return
        self.users[new_user] = input("Zadej heslo: ").strip()
        os.makedirs(os.path.join(self.root_dir, new_user), exist_ok=True)
        print(f"Uživatel '{new_user}' vytvořen.")

    def cmd_dluser(self):
        if len(self.users) <= 1:
            print("Chyba: Nelze smazat posledního uživatele!")
            return
        target = input("Zadej uživatele ke smazání: ").strip()
        if target not in self.users:
            print("Uživatel nenalezen.")
            return
        del self.users[target]
        print(f"Uživatel '{target}' smazán.")

    def cmd_apt_install(self, package_name):
        repo_index_url = "https://raw.githubusercontent.com/martis7650/martisos/refs/heads/main/packages1.json"
        
        if repo_index_url == "hrabe?":
            print("Chyba: V kódu MartisOS není nastaven repozitář (repo_index_url).")
            return

        print(f"Hledám balíček '{package_name}' v repozitáři...")
        try:
            with urllib.request.urlopen(repo_index_url) as response:
                index_data = json.loads(response.read().decode('utf-8'))
            
            if package_name not in index_data:
                print(f"Chyba: Balíček '{package_name}' nebyl nalezen.")
                return
            
            script_url = index_data[package_name]
            filename = script_url.split("/")[-1]
            real_path = self.get_full_path(filename)
            
            print(f"Stahuji '{package_name}'...")
            urllib.request.urlretrieve(script_url, real_path)
            print(f"Balíček '{package_name}' úspěšně nainstalován!")
        except Exception as e:
            print(f"Chyba při stahování balíčku: {e}")

    # ==========================================
    # PYTHONOVSKÝ INTERPRET (PyMartis - pm)
    # ==========================================

    def _eval_expr(self, expr, variables):
        expr = expr.strip()
        if (expr.startswith('"') and expr.endswith('"')) or (expr.startswith("'") and expr.endswith("'")):
            return expr[1:-1]
        
        eval_expr = expr
        for var, val in variables.items():
            if isinstance(val, (int, float)):
                eval_expr = eval_expr.replace(var, str(val))
            else:
                eval_expr = eval_expr.replace(var, f'"{val}"')

        try:
            return eval(eval_expr, {"__builtins__": {}}, {})
        except Exception:
            if expr in variables:
                return variables[expr]
            return expr

    def _eval_cond(self, cond_str, variables):
        ops = ["==", "!=", ">=", "<=", ">", "<"]
        op_found = None
        for op in ops:
            if op in cond_str:
                op_found = op
                break
        
        if not op_found:
            return False

        parts = cond_str.split(op_found, 1)
        left = self._eval_expr(parts[0], variables)
        right = self._eval_expr(parts[1], variables)

        if op_found == "==": return left == right
        elif op_found == "!=": return left != right
        elif op_found == ">": return left > right
        elif op_found == "<": return left < right
        elif op_found == ">=": return left >= right
        elif op_found == "<=": return left <= right
        return False

    def _parse_block(self, lines, start_idx):
        block_lines = []
        i = start_idx
        while i < len(lines):
            line_raw = lines[i]
            if not line_raw.strip():
                i += 1
                continue
            
            indent = len(line_raw) - len(line_raw.lstrip(' '))
            if indent > 0:
                block_lines.append(line_raw)
                i += 1
            else:
                break
        return block_lines, i

    def _execute_block(self, lines, variables):
        i = 0
        while i < len(lines):
            raw_line = lines[i]
            line = raw_line.strip()
            
            if not line or line.startswith("#") or line.startswith("//"):
                i += 1
                continue

            # WHILE CYKLUS
            if line.startswith("while ") and line.endswith(":"):
                cond = line[6:-1].strip()
                body, next_i = self._parse_block(lines, i + 1)
                clean_body = [l[4:] if l.startswith("    ") else l.lstrip() for l in body]
                
                while self._eval_cond(cond, variables):
                    self._execute_block(clean_body, variables)
                
                i = next_i
                continue

            # IF / ELIF / ELSE BLOKY
            if (line.startswith("if ") or line.startswith("elif ")) and line.endswith(":"):
                is_if = line.startswith("if ")
                cond = line[3:-1].strip() if is_if else line[5:-1].strip()
                body, next_i = self._parse_block(lines, i + 1)
                clean_body = [l[4:] if l.startswith("    ") else l.lstrip() for l in body]
                
                matched = self._eval_cond(cond, variables)
                if matched:
                    self._execute_block(clean_body, variables)
                    i = next_i
                    while i < len(lines):
                        peek = lines[i].strip()
                        if peek.startswith("elif ") or peek.startswith("else:"):
                            _, i = self._parse_block(lines, i + 1)
                        else:
                            break
                    continue
                else:
                    i = next_i
                    continue

            if line == "else:":
                body, next_i = self._parse_block(lines, i + 1)
                clean_body = [l[4:] if l.startswith("    ") else l.lstrip() for l in body]
                self._execute_block(clean_body, variables)
                i = next_i
                continue

            # BĚŽNÉ PŘÍKAZY
            if line.startswith("print(") and line.endswith(")"):
                val = self._eval_expr(line[6:-1], variables)
                print(val)
            elif "=" in line and not line.startswith("=="):
                parts = line.split("=", 1)
                var_name = parts[0].strip()
                expr = parts[1].strip()

                if expr.startswith("input(") and expr.endswith(")"):
                    prompt_val = self._eval_expr(expr[6:-1], variables)
                    val = input(prompt_val + " ")
                    try:
                        val = float(val) if "." in val else int(val)
                    except ValueError:
                        pass
                    variables[var_name] = val
                else:
                    variables[var_name] = self._eval_expr(expr, variables)
            else:
                print(f"[PyMartis Chyba] Nerozpoznaný příkaz: {line}")
            
            i += 1

    def cmd_pymartis(self, args):
        if not args:
            print("Použití: pm <mk|nano|run> <název_skriptu.pm>")
            return

        sub_cmd, sub_args = args[0], args[1:]

        if sub_cmd == "mk":
            if not sub_args:
                print("Použití: pm mk <nazev.pm>")
                return
            filename = sub_args[0]
            if not filename.endswith(".pm"): filename += ".pm"
            with open(self.get_full_path(filename), "w", encoding="utf-8") as f:
                f.write("# PyMartis skript\n")
            print(f"Vytvořen soubor: {filename}")

        elif sub_cmd == "nano":
            if not sub_args:
                print("Použití: pm nano <nazev.pm>")
                return
            filename = sub_args[0]
            if not filename.endswith(".pm") and "." not in filename:
                filename += ".pm"
            self.cmd_nano(filename)

        elif sub_cmd == "run":
            if not sub_args:
                print("Použití: pm run <nazev.pm>")
                return
            filename = sub_args[0]
            if not filename.endswith(".pm") and "." not in filename:
                filename += ".pm"
            real_path = self.get_full_path(filename)
            
            if not os.path.exists(real_path):
                print(f"Chyba: Skript '{filename}' nenalezen.")
                return
                
            print(f"--- Spouštím PyMartis skript: {filename} ---")
            with open(real_path, "r", encoding="utf-8") as f:
                code_lines = [line.rstrip('\n') for line in f.readlines()]
                
            variables = {}
            self._execute_block(code_lines, variables)
            print("--- Konec skriptu ---")
        else:
            print(f"Neznámý podřízený příkaz pro pm: {sub_cmd}")

if __name__ == "__main__":
    OS = MartisOS()
    OS.run()
