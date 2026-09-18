"""
Web Interface HTML/JS/CSS generator for the Darukaa Biodiversity AI System.
Provides a clean, functional dashboard for conversational interactions,
structured JSON evaluation, multi-metric causal inspection, and scientific citation review.
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Darukaa.Earth — AI Biodiversity Intelligence System</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #0b1311;
            --bg-secondary: #121f1c;
            --bg-card: #182824;
            --bg-card-hover: #1f332e;
            --accent-green: #10b981;
            --accent-emerald: #059669;
            --accent-light: #6ee7b7;
            --accent-amber: #f59e0b;
            --accent-red: #ef4444;
            --accent-blue: #3b82f6;
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --border: #243c36;
            --border-light: #2d4c44;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        header {
            background-color: var(--bg-secondary);
            border-bottom: 1px solid var(--border);
            padding: 1rem 2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .brand-icon {
            font-size: 1.75rem;
        }

        .brand-title {
            font-size: 1.25rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            color: var(--text-main);
        }

        .brand-subtitle {
            font-size: 0.75rem;
            color: var(--accent-light);
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .badge-status {
            background-color: rgba(16, 185, 129, 0.15);
            color: var(--accent-light);
            border: 1px solid var(--accent-emerald);
            padding: 0.35rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.8rem;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }

        .pulse-dot {
            width: 8px;
            height: 8px;
            background-color: var(--accent-green);
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(0.95); opacity: 0.8; }
            50% { transform: scale(1.2); opacity: 1; }
            100% { transform: scale(0.95); opacity: 0.8; }
        }

        .main-container {
            display: grid;
            grid-template-columns: 320px 1fr 340px;
            flex: 1;
            height: calc(100vh - 73px);
            overflow: hidden;
        }

        /* LEFT SIDEBAR: VARIABLES & PRESETS */
        .sidebar {
            background-color: var(--bg-secondary);
            border-right: 1px solid var(--border);
            padding: 1.25rem;
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
            overflow-y: auto;
        }

        .panel-title {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .preset-btn {
            background-color: var(--bg-card);
            border: 1px solid var(--border);
            color: var(--text-main);
            padding: 0.6rem 0.85rem;
            border-radius: 6px;
            font-size: 0.8rem;
            cursor: pointer;
            text-align: left;
            transition: all 0.2s;
            display: flex;
            flex-direction: column;
            gap: 0.2rem;
        }

        .preset-btn:hover {
            background-color: var(--bg-card-hover);
            border-color: var(--accent-emerald);
        }

        .preset-title {
            font-weight: 600;
            color: var(--accent-light);
        }

        .preset-desc {
            font-size: 0.72rem;
            color: var(--text-muted);
        }

        .active-vars-box {
            background-color: var(--bg-primary);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.75rem;
            min-height: 120px;
            display: flex;
            flex-wrap: wrap;
            gap: 0.4rem;
            align-content: flex-start;
        }

        .var-tag {
            background-color: var(--bg-card);
            border: 1px solid var(--border-light);
            border-radius: 4px;
            padding: 0.25rem 0.5rem;
            font-size: 0.75rem;
            font-family: 'JetBrains Mono', monospace;
            display: flex;
            align-items: center;
            gap: 0.35rem;
        }

        .var-name {
            color: var(--accent-light);
        }

        .var-val {
            color: var(--text-main);
            font-weight: 600;
        }

        /* CENTER: CONVERSATION AREA */
        .chat-section {
            display: flex;
            flex-direction: column;
            background-color: var(--bg-primary);
            height: 100%;
        }

        .chat-messages {
            flex: 1;
            padding: 1.5rem 2rem;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
        }

        .message {
            display: flex;
            gap: 1rem;
            max-width: 90%;
            animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .message.user {
            align-self: flex-end;
            flex-direction: row-reverse;
        }

        .message.assistant {
            align-self: flex-start;
        }

        .avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
            flex-shrink: 0;
        }

        .avatar.user {
            background-color: var(--accent-blue);
            color: white;
        }

        .avatar.assistant {
            background-color: var(--accent-emerald);
            color: white;
        }

        .msg-bubble {
            background-color: var(--bg-card);
            border: 1px solid var(--border);
            padding: 1rem 1.25rem;
            border-radius: 8px;
            font-size: 0.92rem;
            line-height: 1.6;
        }

        .message.user .msg-bubble {
            background-color: #1e3a5f;
            border-color: #2b5285;
            color: white;
        }

        .clarification-banner {
            background-color: rgba(245, 158, 11, 0.12);
            border: 1px solid var(--accent-amber);
            border-radius: 6px;
            padding: 0.75rem 1rem;
            margin-top: 0.75rem;
        }

        .clarification-title {
            font-size: 0.82rem;
            font-weight: 700;
            color: var(--accent-amber);
            margin-bottom: 0.3rem;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }

        .clarification-list {
            list-style: disc;
            margin-left: 1.25rem;
            font-size: 0.85rem;
            color: #fde68a;
        }

        /* INPUT BAR */
        .chat-input-bar {
            background-color: var(--bg-secondary);
            border-top: 1px solid var(--border);
            padding: 1rem 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 0.6rem;
        }

        .input-row {
            display: flex;
            gap: 0.75rem;
        }

        .text-input {
            flex: 1;
            background-color: var(--bg-primary);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 0.75rem 1rem;
            color: var(--text-main);
            font-size: 0.92rem;
            font-family: inherit;
            outline: none;
            transition: border-color 0.2s;
        }

        .text-input:focus {
            border-color: var(--accent-green);
        }

        .btn-send {
            background-color: var(--accent-emerald);
            color: white;
            border: none;
            border-radius: 6px;
            padding: 0 1.5rem;
            font-weight: 600;
            font-size: 0.9rem;
            cursor: pointer;
            transition: background-color 0.2s;
        }

        .btn-send:hover {
            background-color: var(--accent-green);
        }

        .btn-toggle-json {
            background-color: transparent;
            color: var(--accent-light);
            border: 1px dashed var(--border-light);
            border-radius: 4px;
            padding: 0.35rem 0.6rem;
            font-size: 0.78rem;
            cursor: pointer;
            width: fit-content;
        }

        /* RIGHT PANEL: SCIENTIFIC TELEMETRY & KNOWLEDGE PROVENANCE */
        .telemetry-panel {
            background-color: var(--bg-secondary);
            border-left: 1px solid var(--border);
            padding: 1.25rem;
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
            overflow-y: auto;
        }

        .telemetry-card {
            background-color: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1rem;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .card-header {
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--accent-light);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .citation-item {
            border-left: 3px solid var(--accent-green);
            padding-left: 0.6rem;
            margin-top: 0.5rem;
            font-size: 0.78rem;
        }

        .citation-title {
            font-weight: 600;
            color: var(--text-main);
        }

        .citation-org {
            color: var(--accent-light);
            font-size: 0.72rem;
        }

        .citation-text {
            color: var(--text-muted);
            margin-top: 0.2rem;
            font-style: italic;
        }

        /* JSON MODAL */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.75);
            align-items: center;
            justify-content: center;
            z-index: 1000;
        }

        .modal-content {
            background-color: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 8px;
            width: 580px;
            max-width: 90%;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .json-textarea {
            width: 100%;
            height: 240px;
            background-color: var(--bg-primary);
            border: 1px solid var(--border);
            border-radius: 6px;
            color: var(--accent-light);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            padding: 0.75rem;
            outline: none;
        }
    </style>
</head>
<body>
    <header>
        <div class="brand">
            <span class="brand-icon">🌱</span>
            <div>
                <h1 class="brand-title">Darukaa.Earth</h1>
                <div class="brand-subtitle">AI Biodiversity Intelligence Chatbot Challenge</div>
            </div>
        </div>
        <div class="badge-status">
            <span class="pulse-dot"></span>
            <span>Scientific Knowledge Engine: Grounded</span>
        </div>
    </header>

    <div class="main-container">
        <!-- LEFT: PARAMETERS & DEMO PRESETS -->
        <aside class="sidebar">
            <div class="panel-title">
                <span>Scenario Presets</span>
                <span>💡</span>
            </div>
            <button class="preset-btn" onclick="applyPreset('arid_wheat')">
                <span class="preset-title">Test Scenario (PDF Use Case)</span>
                <span class="preset-desc">SOC 0.3%, low rainfall, monoculture wheat, semi-arid</span>
            </button>
            <button class="preset-btn" onclick="applyPreset('incomplete_query')">
                <span class="preset-title">Clarification Trigger</span>
                <span class="preset-desc">"Biodiversity is declining on my land"</span>
            </button>
            <button class="preset-btn" onclick="applyPreset('chemical_runoff')">
                <span class="preset-title">Riparian & Chemical Stress</span>
                <span class="preset-desc">High pesticide runoff, fragmented habitat</span>
            </button>
            <button class="preset-btn" onclick="applyPreset('acidic_degraded')">
                <span class="preset-title">Acidic Soil Depletion</span>
                <span class="preset-desc">Soil pH 4.8, low organic carbon, low richness</span>
            </button>

            <div class="panel-title" style="margin-top: 1rem;">
                <span>Active Variables In Memory</span>
                <span id="var-count-badge" style="color: var(--accent-green);">0</span>
            </div>
            <div class="active-vars-box" id="active-vars-container">
                <span style="color: var(--text-muted); font-size: 0.78rem;">No variables detected yet. Provide context via chat or structured JSON.</span>
            </div>

            <button class="preset-btn" style="border-color: var(--accent-red); margin-top: auto;" onclick="resetMemory()">
                <span class="preset-title" style="color: var(--accent-red);">Reset Conversation Memory</span>
                <span class="preset-desc">Clear accumulated context and variables</span>
            </button>
        </aside>

        <!-- CENTER: CONVERSATION AREA -->
        <main class="chat-section">
            <div class="chat-messages" id="chat-messages">
                <div class="message assistant">
                    <div class="avatar assistant">🌿</div>
                    <div class="msg-bubble">
                        <strong>Darukaa.Earth AI Environmental Scientist</strong><br>
                        Welcome. I evaluate ecosystem and agricultural parameters using multi-metric causal analysis and peer-reviewed environmental literature (FAO, IPCC, IUCN).<br><br>
                        <em>Provide an environmental condition or question to begin your scientific assessment.</em>
                    </div>
                </div>
            </div>

            <div class="chat-input-bar">
                <button class="btn-toggle-json" onclick="openJsonModal()">+ Provide Structured JSON Input</button>
                <div class="input-row">
                    <input type="text" id="user-input" class="text-input" placeholder="e.g. Soil organic carbon is 0.3%, low rainfall, monoculture wheat in semi-arid region..." onkeydown="if(event.key==='Enter') sendMessage()">
                    <button class="btn-send" onclick="sendMessage()">Consult</button>
                </div>
            </div>
        </main>

        <!-- RIGHT: SCIENTIFIC TELEMETRY & CITATIONS -->
        <aside class="telemetry-panel">
            <div class="panel-title">
                <span>Multi-Metric Telemetry</span>
                <span>🔬</span>
            </div>

            <div class="telemetry-card">
                <div class="card-header">
                    <span>Ecological Reasoning Nexus</span>
                </div>
                <div id="telemetry-nexus" style="font-size: 0.8rem; color: var(--text-muted);">
                    Awaiting sufficient environmental variables (&ge; 3) to construct causal chains.
                </div>
            </div>

            <div class="telemetry-card">
                <div class="card-header">
                    <span>Grounding Citations (RAG)</span>
                    <span id="citation-count" style="color: var(--accent-light);">0</span>
                </div>
                <div id="citations-list">
                    <span style="font-size: 0.78rem; color: var(--text-muted);">Scientific literature will be cited upon retrieval.</span>
                </div>
            </div>
        </aside>
    </div>

    <!-- JSON MODAL -->
    <div class="modal" id="json-modal">
        <div class="modal-content">
            <div class="card-header">
                <span>Provide Structured Environmental Profile (JSON)</span>
                <button onclick="closeJsonModal()" style="background:none; border:none; color:white; font-size:1.2rem; cursor:pointer;">&times;</button>
            </div>
            <textarea id="json-input-field" class="json-textarea">{
  "soil_organic_carbon": 0.3,
  "soil_ph": 6.5,
  "soil_moisture": "low",
  "rainfall": "low",
  "temperature": "high",
  "land_use": "monoculture wheat",
  "species_richness": "low",
  "habitat_diversity": "low",
  "pollution": "none",
  "deforestation": "none",
  "region": "semi-arid"
}</textarea>
            <div style="display: flex; justify-content: flex-end; gap: 0.75rem;">
                <button onclick="closeJsonModal()" style="padding: 0.5rem 1rem; border-radius: 4px; background: transparent; border: 1px solid var(--border); color: white; cursor: pointer;">Cancel</button>
                <button onclick="submitJsonProfile()" class="btn-send" style="padding: 0.5rem 1.25rem;">Submit Profile</button>
            </div>
        </div>
    </div>

    <script>
        let currentSessionId = 'session_' + Math.random().toString(36).substr(2, 9);

        function openJsonModal() {
            document.getElementById('json-modal').style.display = 'flex';
        }

        function closeJsonModal() {
            document.getElementById('json-modal').style.display = 'none';
        }

        function applyPreset(type) {
            const input = document.getElementById('user-input');
            if (type === 'arid_wheat') {
                input.value = "Soil organic carbon: 0.3%, rainfall: low, crop: monoculture wheat, region: semi-arid";
            } else if (type === 'incomplete_query') {
                input.value = "Biodiversity is declining on my land.";
            } else if (type === 'chemical_runoff') {
                input.value = "High pesticide runoff pollution and low habitat diversity with fragmented agricultural land.";
            } else if (type === 'acidic_degraded') {
                input.value = "Soil pH is 4.8 with low organic carbon 0.4% and critically low species richness.";
            }
            input.focus();
        }

        async function sendMessage() {
            const input = document.getElementById('user-input');
            const message = input.value.trim();
            if (!message) return;

            appendMessage('user', message);
            input.value = '';

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        message: message,
                        session_id: currentSessionId
                    })
                });

                const data = await response.json();
                handleApiResponse(data);
            } catch (err) {
                appendMessage('assistant', '⚠️ Error contacting the scientific analysis engine: ' + err.message);
            }
        }

        async function submitJsonProfile() {
            const raw = document.getElementById('json-input-field').value;
            closeJsonModal();

            try {
                const parsed = JSON.parse(raw);
                appendMessage('user', '📋 [Submitted Structured Environmental Profile]');

                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        structured_data: parsed,
                        session_id: currentSessionId
                    })
                });

                const data = await response.json();
                handleApiResponse(data);
            } catch (e) {
                alert('Invalid JSON: ' + e.message);
            }
        }

        async function resetMemory() {
            try {
                await fetch('/api/reset', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ session_id: currentSessionId })
                });
                currentSessionId = 'session_' + Math.random().toString(36).substr(2, 9);
                document.getElementById('active-vars-container').innerHTML = '<span style="color: var(--text-muted); font-size: 0.78rem;">Memory reset. No active variables.</span>';
                document.getElementById('var-count-badge').innerText = '0';
                document.getElementById('telemetry-nexus').innerHTML = 'Awaiting input...';
                document.getElementById('citations-list').innerHTML = '<span style="font-size: 0.78rem; color: var(--text-muted);">Citations cleared.</span>';
                document.getElementById('citation-count').innerText = '0';
                appendMessage('assistant', '🔄 *Conversation memory has been reset.*');
            } catch (e) {
                console.error(e);
            }
        }

        function handleApiResponse(data) {
            currentSessionId = data.session_id;

            // Render message
            let formattedReply = formatMarkdown(data.reply);
            
            // If clarifying questions are present, append clarification banner
            if (data.clarifying_questions && data.clarifying_questions.length > 0) {
                let banner = '<div class="clarification-banner">' +
                    '<div class="clarification-title">❓ Incomplete Information Detected — Clarification Required:</div>' +
                    '<ul class="clarification-list">';
                data.clarifying_questions.forEach(q => {
                    banner += `<li><strong>${q.question_text}</strong><br><span style="color:#d1d5db; font-size:0.75rem;">(Why needed: ${q.ecological_importance})</span></li>`;
                });
                banner += '</ul></div>';
                formattedReply += banner;
            }

            appendMessage('assistant', formattedReply);

            // Update Active Variables Pill Box
            renderActiveVariables(data.variables_in_context);

            // Update Telemetry & Citations
            if (data.analysis) {
                renderTelemetry(data.analysis);
            }
        }

        function renderActiveVariables(vars) {
            const container = document.getElementById('active-vars-container');
            const keys = Object.keys(vars || {});
            document.getElementById('var-count-badge').innerText = keys.length;

            if (keys.length === 0) {
                container.innerHTML = '<span style="color: var(--text-muted); font-size: 0.78rem;">No variables detected yet.</span>';
                return;
            }

            container.innerHTML = '';
            keys.forEach(k => {
                const tag = document.createElement('div');
                tag.className = 'var-tag';
                tag.innerHTML = `<span class="var-name">${k}:</span> <span class="var-val">${vars[k]}</span>`;
                container.appendChild(tag);
            });
        }

        function renderTelemetry(analysis) {
            const nexus = document.getElementById('telemetry-nexus');
            if (analysis.causal_relationships && analysis.causal_relationships.length > 0) {
                nexus.innerHTML = analysis.causal_relationships.map(c => `<pre style="font-family:inherit; white-space:pre-wrap; font-size:0.75rem; color:var(--accent-light);">${c}</pre>`).join('<hr style="border-color:var(--border); margin:0.5rem 0;">');
            } else {
                nexus.innerText = "Single variable or baseline state.";
            }

            const citeList = document.getElementById('citations-list');
            const recs = analysis.recommendations || [];
            let allCites = [];
            recs.forEach(r => {
                if (r.citations) allCites.push(...r.citations);
            });

            document.getElementById('citation-count').innerText = allCites.length;
            if (allCites.length === 0) {
                citeList.innerHTML = '<span style="font-size: 0.78rem; color: var(--text-muted);">No external citations retrieved.</span>';
                return;
            }

            citeList.innerHTML = allCites.map(c => `
                <div class="citation-item">
                    <div class="citation-title">[${c.id}] ${c.title}</div>
                    <div class="citation-org">${c.source_org} (${c.year})</div>
                    <div class="citation-text">${c.citation_text}</div>
                </div>
            `).join('');
        }

        function appendMessage(role, htmlContent) {
            const chat = document.getElementById('chat-messages');
            const msgDiv = document.createElement('div');
            msgDiv.className = `message ${role}`;
            
            const avatar = document.createElement('div');
            avatar.className = `avatar ${role}`;
            avatar.innerText = role === 'user' ? '👤' : '🌿';

            const bubble = document.createElement('div');
            bubble.className = 'msg-bubble';
            bubble.innerHTML = htmlContent;

            msgDiv.appendChild(avatar);
            msgDiv.appendChild(bubble);
            chat.appendChild(msgDiv);
            chat.scrollTop = chat.scrollHeight;
        }

        function formatMarkdown(text) {
            if (!text) return '';
            return text
                .replace(/^### (.*$)/gim, '<h3 style="color:var(--accent-light); margin:0.6rem 0 0.3rem;">$1</h3>')
                .replace(/^#### (.*$)/gim, '<h4 style="color:var(--accent-green); margin:0.5rem 0 0.2rem;">$1</h4>')
                .replace(/\\*\\*(.*?)\\*\\*/gim, '<strong>$1</strong>')
                .replace(/\\*(.*?)\\*/gim, '<em>$1</em>')
                .replace(/`([^`]+)`/gim, '<code style="background:rgba(255,255,255,0.08); padding:2px 4px; border-radius:3px; font-family:JetBrains Mono;">$1</code>')
                .replace(/\\n/g, '<br>');
        }
    </script>
</body>
</html>
"""


def get_index_html() -> str:
    """Returns the standalone SPA HTML dashboard."""
    return HTML_TEMPLATE
