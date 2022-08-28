import os, sys, platform, subprocess, stat, tkinter as tk
from tkinter import filedialog


def start_copy(vm, destination, sources):
    output_widget.delete("1.0", "end")
    counters = {"valid":0, "invalid":0}
    def copy(source, dest, source_path=None):
        for x in source:
            if source_path != None:
                x = os.path.join(source_path, x)
            if os.path.isfile(x):
                output = subprocess.getoutput(
                    f"powershell.exe Copy-VMFile '{vm}' -SourcePath '{x}' -DestinationPath '{dest}' -CreateFullPath -FileSource Host")
                if output == "":
                    counters["valid"] += 1
                else:
                    output_widget.pack(side="bottom", fill="both", expand=1)
                    output_widget.insert("end", f"\n{x}")
                    output_widget.insert("end", f"\n{output}")
                    counters["invalid"] += 1
            elif os.path.isdir(x):
                try:
                    if os.readlink(x):
                        continue
                except:pass
                if not bool(os.stat(x).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN):
                    copy(os.listdir(x), dest, x)
            else:
                output_widget.pack(side="bottom", fill="both", expand=1)
                output_widget.insert("end", f"\n{x} - Invalid path\n")
                counters["invalid"] += 1
    if vm != "" and destination != "" and len(sources) > 0:
        copy(sources, destination)
        val, inval = counters["valid"], counters["invalid"]
        info_label.config(text=f"Successfully copied {val} files. Passed {inval}")
    else:
        info_label.config(text="Error")


def delete_path(path, frame):
    if path in sources:
        sources.remove(path)
        frame.destroy()


def ask_path(var):
    if var == "dir":
        path = filedialog.askdirectory()
    elif var == "file":
        path = filedialog.askopenfilename()
    if path not in sources and path != "":
        f = tk.Frame(window, border=1)
        f.pack(side="top", fill="x", expand=1)
        tk.Button(f, text="X", relief="groove", command=lambda: delete_path(s.get(), f)).pack(side="left")
        s = tk.Entry(f, font=("Arial", 12), justify="center", highlightcolor="white", highlightthickness=0, relief="groove", border=2)
        s.pack(side="top", fill="x", expand=1)
        s.insert("end", path)
        s.config(state="disabled")
        sources.append(path)


# Fix graphic on Win 10
if sys.platform == "win32" and platform.release() == "10":
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)

# GUI
root = tk.Tk()
root.title("Copy to Virtual Machine")
root.resizable(True, True)
root.minsize(width=600, height=300)
root.iconphoto(False, tk.PhotoImage(file='data/copy.png'))
window = tk.Frame(root, border=20)
window.pack(fill="both")

info_label = tk.Label(window, text="", font=("Arial", 12), border=2)
info_label.pack(side="top")
frame_1 = tk.Frame(window, border=1)
frame_1.pack(side="top", fill="x", expand=1)
tk.Label(frame_1, text="Virtual Machine Name", font=("Arial", 12), border=2).pack(side="left")
vm = tk.Entry(window, font=("Arial", 12), justify="center", highlightcolor="white", highlightthickness=0, relief="groove", border=2)
vm.pack(side="top", fill="x", expand=1)
frame_2 = tk.Frame(window, border=1)
frame_2.pack(side="top", fill="x", expand=1)
tk.Label(frame_2, text="Virtual Machine Destination", font=("Arial", 12), border=2).pack(side="left")
destination = tk.Entry(
    window, font=("Arial", 12), justify="center", highlightcolor="white", highlightthickness=0, relief="groove", border=2)
destination.pack(side="top", fill="x", expand=1)
frame_3 = tk.Frame(window, border=1)
frame_3.pack(side="top", fill="x", expand=1)
tk.Label(frame_3, text="Sources on this PC", font=("Arial", 12), border=2).pack(side="left")
tk.Button(frame_3, text="Choose file", relief="groove", command=lambda: ask_path("file")).pack(side="left")
tk.Button(frame_3, text="Choose dir", relief="groove", command=lambda: ask_path("dir")).pack(side="left")
start_button = tk.Button(
    window, text="START", font=("Arial", 12), relief="groove", border=2,
    command=lambda: start_copy(vm.get(), destination.get(), sources))
start_button.pack(side="bottom")
output_widget = tk.Text(root, height=15)

sources = []
root.mainloop()