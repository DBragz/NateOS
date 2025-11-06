#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import urllib.request
import urllib.error

API_BASE = "http://localhost:8080/api"

def api_get(path):
	with urllib.request.urlopen(f"{API_BASE}{path}") as resp:
		return json.loads(resp.read().decode("utf-8"))


def api_put(path, payload):
	data = json.dumps(payload).encode("utf-8")
	req = urllib.request.Request(f"{API_BASE}{path}", data=data, headers={"Content-Type": "application/json"}, method="PUT")
	with urllib.request.urlopen(req) as resp:
		return json.loads(resp.read().decode("utf-8"))


def api_post(path, payload):
	data = json.dumps(payload).encode("utf-8")
	req = urllib.request.Request(f"{API_BASE}{path}", data=data, headers={"Content-Type": "application/json"}, method="POST")
	with urllib.request.urlopen(req) as resp:
		return json.loads(resp.read().decode("utf-8"))


def api_delete(path):
	req = urllib.request.Request(f"{API_BASE}{path}", method="DELETE")
	with urllib.request.urlopen(req) as resp:
		return json.loads(resp.read().decode("utf-8"))


class NateOSDesktop(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("NateOS Network Configuration")
		self.geometry("980x700")
		self._build_ui()
		self._load_all()

	def _build_ui(self):
		top = ttk.Frame(self)
		top.pack(fill=tk.X, padx=10, pady=10)

		self.status_var = tk.StringVar(value="Disconnected")
		status_lbl = ttk.Label(top, textvariable=self.status_var, foreground="#0a7f27")
		status_lbl.pack(side=tk.RIGHT)

		nb = ttk.Notebook(self)
		nb.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
		self.nb = nb

		self.tab_l2 = ttk.Frame(nb)
		nb.add(self.tab_l2, text="Layer 2")
		self._build_tab_l2(self.tab_l2)

		self.tab_l3 = ttk.Frame(nb)
		nb.add(self.tab_l3, text="Layer 3")
		self._build_tab_l3(self.tab_l3)

		self.tab_mgmt = ttk.Frame(nb)
		nb.add(self.tab_mgmt, text="Management")
		self._build_tab_mgmt(self.tab_mgmt)

		self.tab_system = ttk.Frame(nb)
		nb.add(self.tab_system, text="System")
		self._build_tab_system(self.tab_system)

	def _section(self, parent, title):
		frm = ttk.LabelFrame(parent, text=title)
		frm.pack(fill=tk.X, padx=6, pady=8)
		return frm

	# -------- L2 --------
	def _build_tab_l2(self, parent):
		# Interfaces
		sec_if = self._section(parent, "Interfaces")
		self.interfaces_list = tk.Listbox(sec_if, height=6)
		self.interfaces_list.pack(fill=tk.X, padx=6, pady=6)
		btns_if = ttk.Frame(sec_if)
		btns_if.pack(fill=tk.X, padx=6, pady=6)
		ttk.Button(btns_if, text="Add", command=self._add_interface).pack(side=tk.LEFT)
		ttk.Button(btns_if, text="Edit", command=self._edit_interface).pack(side=tk.LEFT, padx=6)

		# VLANs
		sec_vlan = self._section(parent, "VLANs")
		self.vlans_list = tk.Listbox(sec_vlan, height=6)
		self.vlans_list.pack(fill=tk.X, padx=6, pady=6)
		btns_vlan = ttk.Frame(sec_vlan)
		btns_vlan.pack(fill=tk.X, padx=6, pady=6)
		ttk.Button(btns_vlan, text="Add VLAN", command=self._add_vlan).pack(side=tk.LEFT)
		ttk.Button(btns_vlan, text="Delete VLAN", command=self._delete_vlan).pack(side=tk.LEFT, padx=6)

		# STP
		sec_stp = self._section(parent, "Spanning Tree (STP)")
		stp_row = ttk.Frame(sec_stp)
		stp_row.pack(fill=tk.X, padx=6, pady=6)
		self.stp_enabled = tk.BooleanVar(value=False)
		self.stp_mode = tk.StringVar(value="rstp")
		self.stp_priority = tk.IntVar(value=32768)
		ttk.Checkbutton(stp_row, text="Enable STP", variable=self.stp_enabled, command=self._update_stp).pack(side=tk.LEFT)
		ttk.Label(stp_row, text="Mode:").pack(side=tk.LEFT, padx=6)
		mode = ttk.Combobox(stp_row, textvariable=self.stp_mode, values=["rstp", "mstp"], width=8)
		mode.bind("<<ComboboxSelected>>", lambda e: self._update_stp())
		mode.pack(side=tk.LEFT)
		ttk.Label(stp_row, text="Priority:").pack(side=tk.LEFT, padx=6)
		pri = ttk.Entry(stp_row, textvariable=self.stp_priority, width=8)
		pri.bind("<FocusOut>", lambda e: self._update_stp())
		pri.pack(side=tk.LEFT)

		# LLDP / IGMP
		sec_l2_misc = self._section(parent, "LLDP / IGMP Snooping")
		misc_row = ttk.Frame(sec_l2_misc)
		misc_row.pack(fill=tk.X, padx=6, pady=6)
		self.lldp_enabled = tk.BooleanVar(value=False)
		self.igmp_enabled = tk.BooleanVar(value=False)
		ttk.Checkbutton(misc_row, text="Enable LLDP", variable=self.lldp_enabled, command=self._update_lldp).pack(side=tk.LEFT)
		ttk.Checkbutton(misc_row, text="Enable IGMP Snooping", variable=self.igmp_enabled, command=self._update_igmp).pack(side=tk.LEFT, padx=16)

	# -------- L3 --------
	def _build_tab_l3(self, parent):
		# Static routes
		sec_routes = self._section(parent, "Static Routes")
		self.routes_list = tk.Listbox(sec_routes, height=6)
		self.routes_list.pack(fill=tk.X, padx=6, pady=6)
		btns_routes = ttk.Frame(sec_routes)
		btns_routes.pack(fill=tk.X, padx=6, pady=6)
		ttk.Button(btns_routes, text="Add Route", command=self._add_route).pack(side=tk.LEFT)
		ttk.Button(btns_routes, text="Delete Route", command=self._delete_route).pack(side=tk.LEFT, padx=6)

		# OSPF
		sec_ospf = self._section(parent, "OSPF")
		self.ospf_enabled = tk.BooleanVar(value=False)
		ttk.Checkbutton(sec_ospf, text="Enable OSPF", variable=self.ospf_enabled, command=self._update_ospf).pack(side=tk.LEFT, padx=6, pady=6)

		# BGP
		sec_bgp = self._section(parent, "BGP")
		bgp_row = ttk.Frame(sec_bgp)
		bgp_row.pack(fill=tk.X, padx=6, pady=6)
		self.bgp_enabled = tk.BooleanVar(value=False)
		self.bgp_asn = tk.IntVar(value=0)
		ttk.Checkbutton(bgp_row, text="Enable BGP", variable=self.bgp_enabled, command=self._update_bgp).pack(side=tk.LEFT)
		ttk.Label(bgp_row, text="ASN:").pack(side=tk.LEFT, padx=6)
		asn = ttk.Entry(bgp_row, textvariable=self.bgp_asn, width=10)
		asn.bind("<FocusOut>", lambda e: self._update_bgp())
		asn.pack(side=tk.LEFT)

	# -------- Mgmt --------
	def _build_tab_mgmt(self, parent):
		sec_qos = self._section(parent, "QoS")
		ttk.Button(sec_qos, text="Configure QoS (stub)", command=lambda: messagebox.showinfo("QoS", "Coming soon")).pack(side=tk.LEFT, padx=6, pady=6)

		sec_acl = self._section(parent, "ACL")
		self.acl_list = tk.Listbox(sec_acl, height=6)
		self.acl_list.pack(fill=tk.X, padx=6, pady=6)
		btns_acl = ttk.Frame(sec_acl)
		btns_acl.pack(fill=tk.X, padx=6, pady=6)
		ttk.Button(btns_acl, text="Add ACL", command=self._add_acl).pack(side=tk.LEFT)

	# -------- System --------
	def _build_tab_system(self, parent):
		sec_sys = self._section(parent, "System Settings")
		row1 = ttk.Frame(sec_sys)
		row1.pack(fill=tk.X, padx=6, pady=6)
		self.sys_hostname = tk.StringVar(value="")
		self.sys_domain = tk.StringVar(value="")
		ttk.Label(row1, text="Hostname:").pack(side=tk.LEFT)
		ttk.Entry(row1, textvariable=self.sys_hostname, width=24).pack(side=tk.LEFT, padx=6)
		ttk.Label(row1, text="Domain:").pack(side=tk.LEFT, padx=6)
		ttk.Entry(row1, textvariable=self.sys_domain, width=24).pack(side=tk.LEFT, padx=6)
		ttk.Button(row1, text="Save", command=self._update_system).pack(side=tk.LEFT, padx=10)

		sec_aaa = self._section(parent, "AAA")
		row2 = ttk.Frame(sec_aaa)
		row2.pack(fill=tk.X, padx=6, pady=6)
		self.aaa_method = tk.StringVar(value="local")
		ttk.Label(row2, text="Auth Method:").pack(side=tk.LEFT)
		cmb = ttk.Combobox(row2, textvariable=self.aaa_method, values=["local", "radius", "tacacs"], width=12)
		cmb.bind("<<ComboboxSelected>>", lambda e: self._update_aaa())
		cmb.pack(side=tk.LEFT, padx=6)

	# -------- Loaders & Actions --------
	def _safe_call(self, fn, ok_msg=None):
		try:
			res = fn()
			if ok_msg:
				self.status_var.set(ok_msg)
			return res
		except urllib.error.URLError:
			self.status_var.set("Disconnected")
			messagebox.showerror("Error", "Cannot reach NateOS API at http://localhost:8080. Start it with scripts/run-web-gui.ps1")
		except Exception as e:
			messagebox.showerror("Error", str(e))

	def _load_all(self):
		# Health
		try:
			h = api_get("/health")
			self.status_var.set("Connected")
		except Exception:
			self.status_var.set("Disconnected")
		# L2
		self._load_interfaces()
		self._load_vlans()
		self._load_stp()
		self._load_lldp()
		self._load_igmp()
		# L3
		self._load_routes()
		self._load_ospf()
		self._load_bgp()
		# System
		self._load_system()
		self._load_aaa()

	# L2 loaders/actions
	def _load_interfaces(self):
		self.interfaces_list.delete(0, tk.END)
		ifs = self._safe_call(lambda: api_get("/l2/interfaces")) or {}
		for name, cfg in ifs.items():
			mode = cfg.get("mode", "access")
			vlan = cfg.get("vlan", "-")
			self.interfaces_list.insert(tk.END, f"{name} - {mode} - VLAN {vlan}")

	def _add_interface(self):
		name = simpledialog.askstring("Interface", "Interface name (e.g., eth0):", parent=self)
		if not name:
			return
		mode = simpledialog.askstring("Interface", "Mode (access/trunk):", parent=self) or "access"
		vlan = simpledialog.askinteger("Interface", "VLAN ID (1-4094):", parent=self)
		payload = {"mode": mode, "vlan": vlan}
		self._safe_call(lambda: api_put(f"/l2/interfaces/{name}", payload), ok_msg="Interface saved")
		self._load_interfaces()

	def _edit_interface(self):
		idx = self.interfaces_list.curselection()
		if not idx:
			return
		# In a simple stub, re-run add with same name prompt
		self._add_interface()

	def _load_vlans(self):
		self.vlans_list.delete(0, tk.END)
		vlans = self._safe_call(lambda: api_get("/l2/vlans")) or {}
		for vid, vcfg in vlans.items():
			name = vcfg.get("name", "")
			self.vlans_list.insert(tk.END, f"VLAN {vid} {('- ' + name) if name else ''}")

	def _add_vlan(self):
		vid = simpledialog.askinteger("VLAN", "VLAN ID (1-4094):", parent=self)
		if not vid:
			return
		name = simpledialog.askstring("VLAN", "VLAN name:", parent=self) or ""
		self._safe_call(lambda: api_post("/l2/vlans", {"vlan_id": vid, "name": name}), ok_msg="VLAN created")
		self._load_vlans()

	def _delete_vlan(self):
		sel = self.vlans_list.curselection()
		if not sel:
			return
		text = self.vlans_list.get(sel[0])
		vid = text.split()[1]
		self._safe_call(lambda: api_delete(f"/l2/vlans/{vid}"), ok_msg="VLAN deleted")
		self._load_vlans()

	def _load_stp(self):
		stp = self._safe_call(lambda: api_get("/l2/stp")) or {}
		self.stp_enabled.set(bool(stp.get("enabled", False)))
		self.stp_mode.set(stp.get("mode", "rstp"))
		self.stp_priority.set(int(stp.get("priority", 32768)))

	def _update_stp(self):
		payload = {
			"enabled": bool(self.stp_enabled.get()),
			"mode": self.stp_mode.get(),
			"priority": int(self.stp_priority.get()),
		}
		self._safe_call(lambda: api_put("/l2/stp", payload), ok_msg="STP updated")

	def _load_lldp(self):
		lldp = self._safe_call(lambda: api_get("/l2/lldp")) or {}
		self.lldp_enabled.set(bool(lldp.get("enabled", False)))

	def _update_lldp(self):
		self._safe_call(lambda: api_put("/l2/lldp", {"enabled": bool(self.lldp_enabled.get())}), ok_msg="LLDP updated")

	def _load_igmp(self):
		igmp = self._safe_call(lambda: api_get("/l2/igmp-snooping")) or {}
		self.igmp_enabled.set(bool(igmp.get("enabled", False)))

	def _update_igmp(self):
		self._safe_call(lambda: api_put("/l2/igmp-snooping", {"enabled": bool(self.igmp_enabled.get())}), ok_msg="IGMP updated")

	# L3 loaders/actions
	def _load_routes(self):
		self.routes_list.delete(0, tk.END)
		routes = self._safe_call(lambda: api_get("/l3/static-routes")) or []
		for r in routes:
			self.routes_list.insert(tk.END, f"{r.get('destination','') or 'N/A'} via {r.get('gateway','') or 'N/A'}")

	def _add_route(self):
		dest = simpledialog.askstring("Static Route", "Destination (CIDR):", parent=self)
		if not dest:
			return
		gw = simpledialog.askstring("Static Route", "Gateway IP:", parent=self)
		self._safe_call(lambda: api_post("/l3/static-routes", {"destination": dest, "gateway": gw}), ok_msg="Route added")
		self._load_routes()

	def _delete_route(self):
		idxs = self.routes_list.curselection()
		if not idxs:
			return
		idx = int(idxs[0])
		self._safe_call(lambda: api_delete(f"/l3/static-routes/{idx}"), ok_msg="Route deleted")
		self._load_routes()

	def _load_ospf(self):
		cfg = self._safe_call(lambda: api_get("/l3/ospf")) or {}
		self.ospf_enabled.set(bool(cfg.get("enabled", False)))

	def _update_ospf(self):
		self._safe_call(lambda: api_put("/l3/ospf", {"enabled": bool(self.ospf_enabled.get())}), ok_msg="OSPF updated")

	def _load_bgp(self):
		cfg = self._safe_call(lambda: api_get("/l3/bgp")) or {}
		self.bgp_enabled.set(bool(cfg.get("enabled", False)))
		self.bgp_asn.set(int(cfg.get("asn", 0)))

	def _update_bgp(self):
		payload = {"enabled": bool(self.bgp_enabled.get()), "asn": int(self.bgp_asn.get())}
		self._safe_call(lambda: api_put("/l3/bgp", payload), ok_msg="BGP updated")

	# System
	def _load_system(self):
		cfg = self._safe_call(lambda: api_get("/mgmt/system")) or {}
		self.sys_hostname.set(cfg.get("hostname", ""))
		self.sys_domain.set(cfg.get("domain", ""))

	def _update_system(self):
		self._safe_call(lambda: api_put("/mgmt/system", {"hostname": self.sys_hostname.get(), "domain": self.sys_domain.get()}), ok_msg="System saved")

	def _load_aaa(self):
		cfg = self._safe_call(lambda: api_get("/mgmt/aaa")) or {}
		self.aaa_method.set(cfg.get("auth_method", "local"))

	def _update_aaa(self):
		self._safe_call(lambda: api_put("/mgmt/aaa", {"auth_method": self.aaa_method.get()}), ok_msg="AAA saved")

	# ACL (simple add-only stub)
	def _add_acl(self):
		src = simpledialog.askstring("ACL", "Source (CIDR):", parent=self)
		dst = simpledialog.askstring("ACL", "Destination (CIDR):", parent=self)
		action = simpledialog.askstring("ACL", "Action (permit/deny):", parent=self) or "permit"
		if not src or not dst:
			return
		self._safe_call(lambda: api_post("/mgmt/acl", {"src": src, "dst": dst, "action": action}), ok_msg="ACL added")
		# Optional: refresh list (not stored separately in UI)


def main():
	app = NateOSDesktop()
	app.mainloop()


if __name__ == "__main__":
	main()
