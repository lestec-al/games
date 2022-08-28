import tkinter as tk, os, sys, platform, socket, http.server, socketserver, pyqrcode, threading, logging
from tkinter import filedialog
from requests.utils import requote_uri
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer

# TCP

class TCPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        output_widget.insert("end", f"{self.log_date_time_string()} - {self.address_string()} - {format%args}\n")

    def list_directory(self, path):
        from http import HTTPStatus
        import html, io
        try:
            list = os.listdir(path)
        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND, "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        r = []
        try:
            displaypath = requote_uri(self.path)
        except UnicodeDecodeError:
            displaypath = requote_uri(path)
        displaypath = html.escape(displaypath, quote=False)
        enc = sys.getfilesystemencoding()
        title = 'Files %s' % displaypath
        r.append('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">')
        r.append('<html>\n<head>')
        r.append('<meta http-equiv="Content-Type" content="text/html; charset=%s">' % enc)
        r.append('<title>%s</title>\n</head>' % title)
        r.append('<body>\n<h1>%s</h1>' % title)
        r.append('<hr>\n<ul>')
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
                r.append('<li><a href="%s">%s</a></li>'
                        % (requote_uri(linkname), html.escape(displayname, quote=False)))
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
                r.append('<li><a href="%s">%s</a></li>'
                        % (requote_uri(linkname), html.escape(displayname, quote=False)))
            else:
                r.append('<li><a href="%s" download>%s</a></li>'
                        % (requote_uri(linkname), html.escape(displayname, quote=False)))
        r.append('</ul>\n<hr>\n</body>\n</html>\n')
        encoded = '\n'.join(r).encode(enc, 'surrogateescape')
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return f


class TCPServer(socketserver.ThreadingTCPServer):
    def verify_request(self, request, client_address):
        if client_address[0] not in connections:
            connections.append(client_address[0])
        connections_label.config(text=f"{len(connections)}")
        return True


class TCPThread(threading.Thread):
    def run(self):
        self.server = TCPServer(("", PORT), TCPRequestHandler)
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()


# FTP

class FTPLogHandler():
    def write(self, str=None):
        output_widget.insert("end", f"{str}")
    def flush(self, str=None):
        pass


class FTPServer(ThreadedFTPServer):
    def handle_accepted(self, request, client_address):
        if client_address[0] not in connections:
            connections.append(client_address[0])
        connections_label.config(text=f"{len(connections)}")
        return super().handle_accepted(request, client_address)


class FTPThread(threading.Thread):
    def run(self):
        authorizer = DummyAuthorizer()
        # authorizer.add_user("user", "12345", path_text.cget("text"), perm="elradfmwMT")
        authorizer.add_anonymous(path_text.cget("text"))
        handler = FTPHandler
        handler.authorizer = authorizer
        logging.basicConfig(stream=FTPLogHandler(), level=logging.INFO)
        self.server = FTPServer((IP, PORT), handler)
        self.server.serve_forever()

    def stop(self):
        self.server.close_all()

#

def start_stop_server(goal_server):
    global server
    global qrcode_img
    if server == None:
        try:
            os.chdir(path_text.cget("text"))
            connections.clear()
            output_widget.delete("1.0", "end")
            catalog_button.config(state="disabled")

            link = f"http://{IP}:{PORT}" if goal_server == "tcp" else f"ftp://{IP}:{PORT}"
            url_text.config(text=link)
            url_text.pack(side="top", pady=10)
            output_widget.insert("end", f"Sharing start at {link}\n")
            # QRcode
            qr = pyqrcode.create(link)
            qrcode_img = tk.BitmapImage(data=qr.xbm(scale=8))
            image_label.config(image=qrcode_img)
            image_label.pack(side="bottom")

            if goal_server == "tcp":
                start_ftp_button.config(state="disabled")
                start_tcp_button.config(text="Stop Web")
                server = TCPThread()
                server.start()

            elif goal_server == "ftp":
                start_tcp_button.config(state="disabled")
                start_ftp_button.config(text="Stop FTP")
                server = FTPThread()
                server.start()

        except Exception as e:
            output_widget.insert("end", f"{e}\n")

    elif server != None:
        server.stop()
        server = None

        if goal_server == "tcp":
            start_tcp_button.config(text="Start Web")
            start_ftp_button.config(state="normal")
        elif goal_server == "ftp":
            start_ftp_button.config(text="Start FTP")
            start_tcp_button.config(state="normal")

        image_label.pack_forget()
        url_text.pack_forget()
        catalog_button.config(state="normal")
        connections_label.config(text="0")
        output_widget.insert("end", "Sharing stop\n")


def ask_path():
    path = filedialog.askdirectory()
    if path != path_text.cget("text") and path != "":
        path_text.config(text=path)


server = None
qrcode_img = None
connections = []
IP = socket.gethostbyname(socket.gethostname())
PORT = 8000

# Fix graphic on Win 10
if sys.platform == "win32" and platform.release() == "10":
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)

# GUI
root = tk.Tk()
root.title("Share files")
root.resizable(True, True)
root.iconphoto(False, tk.PhotoImage(file="data/copy.png"))
root.configure(bg="white")
window = tk.Frame(root, border=20, bg="white")
window.pack(side="top")

f1 = tk.Frame(window, border=1, bg="white")
f1.pack(side="top", fill="x", expand=1, pady=10)
start_tcp_button = tk.Button(f1, text="Start Web", font=("Arial", 12), relief="groove", border=2, padx=5,
    command=lambda:start_stop_server("tcp"))
start_tcp_button.pack(side="left", padx=5)
start_ftp_button = tk.Button(f1, text="Start FTP", font=("Arial", 12), relief="groove", border=2, padx=5,
    command=lambda:start_stop_server("ftp"))
start_ftp_button.pack(side="left", padx=5)
catalog_button = tk.Button(f1, text="Select catalog", font=("Arial", 12), relief="groove", command=ask_path)
catalog_button.pack(side="left", padx=10)
connections_label = tk.Label(f1, text="0", font=("Arial", 12), bg="white")
connections_label.pack(side="left", padx=10)

path_text = tk.Label(window, text="", font=("Arial", 12), border=2, bg="white")
path_text.pack(side="top", pady=10)
url_text = tk.Label(window, text="", font=("Arial", 12), border=2, bg="white")
image_label = tk.Label(window, text="", font=("Arial", 12), border=2, bg="white")

output_widget = tk.Text(root, height=15, width=15)
output_widget.pack(side="bottom", fill="both", expand=1)

root.mainloop()