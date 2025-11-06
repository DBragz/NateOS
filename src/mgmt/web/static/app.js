const API_BASE = 'http://localhost:8080/api';

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    checkHealth();
    loadAllConfigs();
});

// Tab switching
function initTabs() {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.dataset.tab;
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(tabName).classList.add('active');
        });
    });
}

// Health check
async function checkHealth() {
    try {
        const res = await fetch(`${API_BASE}/health`);
        const data = await res.json();
        updateStatus('ok', 'Connected');
    } catch (e) {
        updateStatus('error', 'Disconnected');
    }
}

function updateStatus(status, text) {
    const indicator = document.getElementById('status-indicator');
    const statusText = document.getElementById('status-text');
    indicator.className = `status-indicator status-${status}`;
    statusText.textContent = text;
}

// Load all configurations
async function loadAllConfigs() {
    await Promise.all([
        loadInterfaces(),
        loadVLANs(),
        loadSTP(),
        loadLLDP(),
        loadIGMP(),
        loadStaticRoutes(),
        loadOSPF(),
        loadBGP(),
        loadSystem(),
        loadAAA()
    ]);
}

// L2 Functions
async function loadInterfaces() {
    try {
        const res = await fetch(`${API_BASE}/l2/interfaces`);
        const interfaces = await res.json();
        const list = document.getElementById('interfaces-list');
        list.innerHTML = Object.keys(interfaces).length === 0 
            ? '<p>No interfaces configured</p>'
            : Object.entries(interfaces).map(([name, config]) => 
                `<div class="list-item">
                    <span><strong>${name}</strong> - ${config.mode || 'access'} - VLAN ${config.vlan || 'N/A'}</span>
                    <button class="btn-secondary" onclick="editInterface('${name}')">Edit</button>
                </div>`
            ).join('');
    } catch (e) {
        console.error('Failed to load interfaces:', e);
    }
}

function addInterface() {
    showModal(`
        <h3>Add Interface</h3>
        <div class="form-group">
            <label>Interface Name:</label>
            <input type="text" id="if-name" placeholder="eth0">
        </div>
        <div class="form-group">
            <label>Mode:</label>
            <select id="if-mode">
                <option value="access">Access</option>
                <option value="trunk">Trunk</option>
            </select>
        </div>
        <div class="form-group">
            <label>VLAN:</label>
            <input type="number" id="if-vlan" placeholder="1">
        </div>
        <button class="btn-primary" onclick="saveInterface()">Save</button>
    `);
}

async function saveInterface() {
    const name = document.getElementById('if-name').value;
    const mode = document.getElementById('if-mode').value;
    const vlan = document.getElementById('if-vlan').value;
    
    try {
        await fetch(`${API_BASE}/l2/interfaces/${name}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({mode, vlan: parseInt(vlan)})
        });
        closeModal();
        loadInterfaces();
        showSuccess('Interface configured');
    } catch (e) {
        showError('Failed to configure interface');
    }
}

async function loadVLANs() {
    try {
        const res = await fetch(`${API_BASE}/l2/vlans`);
        const vlans = await res.json();
        const list = document.getElementById('vlans-list');
        list.innerHTML = Object.keys(vlans).length === 0
            ? '<p>No VLANs configured</p>'
            : Object.entries(vlans).map(([id, vlan]) =>
                `<div class="list-item">
                    <span><strong>VLAN ${id}</strong> - ${vlan.name || 'Unnamed'}</span>
                    <button class="btn-danger" onclick="deleteVLAN('${id}')">Delete</button>
                </div>`
            ).join('');
    } catch (e) {
        console.error('Failed to load VLANs:', e);
    }
}

function showAddVlan() {
    showModal(`
        <h3>Add VLAN</h3>
        <div class="form-group">
            <label>VLAN ID:</label>
            <input type="number" id="vlan-id" placeholder="100" min="1" max="4094">
        </div>
        <div class="form-group">
            <label>VLAN Name:</label>
            <input type="text" id="vlan-name" placeholder="VLAN100">
        </div>
        <button class="btn-primary" onclick="saveVLAN()">Save</button>
    `);
}

async function saveVLAN() {
    const vlanId = document.getElementById('vlan-id').value;
    const name = document.getElementById('vlan-name').value;
    
    try {
        await fetch(`${API_BASE}/l2/vlans`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({vlan_id: parseInt(vlanId), name})
        });
        closeModal();
        loadVLANs();
        showSuccess('VLAN created');
    } catch (e) {
        showError('Failed to create VLAN');
    }
}

async function deleteVLAN(vlanId) {
    if (!confirm(`Delete VLAN ${vlanId}?`)) return;
    
    try {
        await fetch(`${API_BASE}/l2/vlans/${vlanId}`, {method: 'DELETE'});
        loadVLANs();
        showSuccess('VLAN deleted');
    } catch (e) {
        showError('Failed to delete VLAN');
    }
}

async function loadSTP() {
    try {
        const res = await fetch(`${API_BASE}/l2/stp`);
        const stp = await res.json();
        document.getElementById('stp-enabled').checked = stp.enabled || false;
        document.getElementById('stp-mode').value = stp.mode || 'rstp';
        document.getElementById('stp-priority').value = stp.priority || 32768;
    } catch (e) {
        console.error('Failed to load STP:', e);
    }
}

async function updateSTP() {
    const enabled = document.getElementById('stp-enabled').checked;
    const mode = document.getElementById('stp-mode').value;
    const priority = parseInt(document.getElementById('stp-priority').value);
    
    try {
        await fetch(`${API_BASE}/l2/stp`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({enabled, mode, priority})
        });
        showSuccess('STP configuration updated');
    } catch (e) {
        showError('Failed to update STP');
    }
}

async function loadLLDP() {
    try {
        const res = await fetch(`${API_BASE}/l2/lldp`);
        const lldp = await res.json();
        document.getElementById('lldp-enabled').checked = lldp.enabled || false;
    } catch (e) {
        console.error('Failed to load LLDP:', e);
    }
}

async function updateLLDP() {
    const enabled = document.getElementById('lldp-enabled').checked;
    
    try {
        await fetch(`${API_BASE}/l2/lldp`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({enabled})
        });
        showSuccess('LLDP configuration updated');
    } catch (e) {
        showError('Failed to update LLDP');
    }
}

async function loadIGMP() {
    try {
        const res = await fetch(`${API_BASE}/l2/igmp-snooping`);
        const igmp = await res.json();
        document.getElementById('igmp-enabled').checked = igmp.enabled || false;
    } catch (e) {
        console.error('Failed to load IGMP:', e);
    }
}

async function updateIGMP() {
    const enabled = document.getElementById('igmp-enabled').checked;
    
    try {
        await fetch(`${API_BASE}/l2/igmp-snooping`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({enabled})
        });
        showSuccess('IGMP snooping configuration updated');
    } catch (e) {
        showError('Failed to update IGMP snooping');
    }
}

function configureLACP() {
    showModal('<h3>LACP Configuration</h3><p>LACP configuration form coming soon...</p>');
}

// L3 Functions
async function loadStaticRoutes() {
    try {
        const res = await fetch(`${API_BASE}/l3/static-routes`);
        const routes = await res.json();
        const list = document.getElementById('routes-list');
        list.innerHTML = routes.length === 0
            ? '<p>No static routes configured</p>'
            : routes.map((route, idx) =>
                `<div class="list-item">
                    <span><strong>${route.destination || 'N/A'}</strong> via ${route.gateway || 'N/A'}</span>
                    <button class="btn-danger" onclick="deleteRoute(${idx})">Delete</button>
                </div>`
            ).join('');
    } catch (e) {
        console.error('Failed to load routes:', e);
    }
}

function showAddRoute() {
    showModal(`
        <h3>Add Static Route</h3>
        <div class="form-group">
            <label>Destination:</label>
            <input type="text" id="route-dest" placeholder="192.168.1.0/24">
        </div>
        <div class="form-group">
            <label>Gateway:</label>
            <input type="text" id="route-gateway" placeholder="192.168.1.1">
        </div>
        <button class="btn-primary" onclick="saveRoute()">Save</button>
    `);
}

async function saveRoute() {
    const destination = document.getElementById('route-dest').value;
    const gateway = document.getElementById('route-gateway').value;
    
    try {
        await fetch(`${API_BASE}/l3/static-routes`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({destination, gateway})
        });
        closeModal();
        loadStaticRoutes();
        showSuccess('Static route added');
    } catch (e) {
        showError('Failed to add route');
    }
}

async function deleteRoute(index) {
    if (!confirm('Delete this route?')) return;
    
    try {
        await fetch(`${API_BASE}/l3/static-routes/${index}`, {method: 'DELETE'});
        loadStaticRoutes();
        showSuccess('Route deleted');
    } catch (e) {
        showError('Failed to delete route');
    }
}

async function loadOSPF() {
    try {
        const res = await fetch(`${API_BASE}/l3/ospf`);
        const ospf = await res.json();
        document.getElementById('ospf-enabled').checked = ospf.enabled || false;
    } catch (e) {
        console.error('Failed to load OSPF:', e);
    }
}

async function updateOSPF() {
    const enabled = document.getElementById('ospf-enabled').checked;
    
    try {
        await fetch(`${API_BASE}/l3/ospf`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({enabled})
        });
        showSuccess('OSPF configuration updated');
    } catch (e) {
        showError('Failed to update OSPF');
    }
}

function addOSPFArea() {
    showModal('<h3>Add OSPF Area</h3><p>OSPF area configuration coming soon...</p>');
}

async function loadBGP() {
    try {
        const res = await fetch(`${API_BASE}/l3/bgp`);
        const bgp = await res.json();
        document.getElementById('bgp-enabled').checked = bgp.enabled || false;
        document.getElementById('bgp-asn').value = bgp.asn || '';
    } catch (e) {
        console.error('Failed to load BGP:', e);
    }
}

async function updateBGP() {
    const enabled = document.getElementById('bgp-enabled').checked;
    const asn = parseInt(document.getElementById('bgp-asn').value);
    
    try {
        await fetch(`${API_BASE}/l3/bgp`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({enabled, asn})
        });
        showSuccess('BGP configuration updated');
    } catch (e) {
        showError('Failed to update BGP');
    }
}

function addBGPNeighbor() {
    showModal('<h3>Add BGP Neighbor</h3><p>BGP neighbor configuration coming soon...</p>');
}

function configureVRRP() {
    showModal('<h3>VRRP Configuration</h3><p>VRRP configuration coming soon...</p>');
}

// Management Functions
function configureQoS() {
    showModal('<h3>QoS Configuration</h3><p>QoS policy configuration coming soon...</p>');
}

function showAddACL() {
    showModal('<h3>Add ACL Rule</h3><p>ACL rule configuration coming soon...</p>');
}

function configureSPAN() {
    showModal('<h3>SPAN Configuration</h3><p>Port mirroring configuration coming soon...</p>');
}

// System Functions
async function loadSystem() {
    try {
        const res = await fetch(`${API_BASE}/mgmt/system`);
        const system = await res.json();
        document.getElementById('system-hostname').value = system.hostname || '';
        document.getElementById('system-domain').value = system.domain || '';
    } catch (e) {
        console.error('Failed to load system config:', e);
    }
}

async function updateSystem() {
    const hostname = document.getElementById('system-hostname').value;
    const domain = document.getElementById('system-domain').value;
    
    try {
        await fetch(`${API_BASE}/mgmt/system`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({hostname, domain})
        });
        showSuccess('System configuration updated');
    } catch (e) {
        showError('Failed to update system config');
    }
}

async function loadAAA() {
    try {
        const res = await fetch(`${API_BASE}/mgmt/aaa`);
        const aaa = await res.json();
        document.getElementById('aaa-method').value = aaa.auth_method || 'local';
    } catch (e) {
        console.error('Failed to load AAA:', e);
    }
}

async function updateAAA() {
    const auth_method = document.getElementById('aaa-method').value;
    
    try {
        await fetch(`${API_BASE}/mgmt/aaa`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({auth_method})
        });
        showSuccess('AAA configuration updated');
    } catch (e) {
        showError('Failed to update AAA');
    }
}

// Modal helpers
function showModal(html) {
    document.getElementById('modal-body').innerHTML = html;
    document.getElementById('modal-overlay').classList.add('active');
}

function closeModal() {
    document.getElementById('modal-overlay').classList.remove('active');
}

function showSuccess(message) {
    const msg = document.createElement('div');
    msg.className = 'success-message';
    msg.textContent = message;
    document.querySelector('main').insertBefore(msg, document.querySelector('main').firstChild);
    setTimeout(() => msg.remove(), 3000);
}

function showError(message) {
    const msg = document.createElement('div');
    msg.className = 'error-message';
    msg.textContent = message;
    document.querySelector('main').insertBefore(msg, document.querySelector('main').firstChild);
    setTimeout(() => msg.remove(), 5000);
}

