"""
AirgapShield: Web Operations Dashboard & Incident Commander
Flask Application demonstrating On-Device GraphRAG & pgvector Incident Triage
"""

import os
from flask import Flask, render_template_string, jsonify, request
from agent import AirgapShieldAgent

app = Flask(__name__)
agent = AirgapShieldAgent()

HTML_DASHBOARD = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>AirgapShield | On-Device GraphRAG & Autonomous OT Agent</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    body { background-color: #0b0f19; color: #e2e8f0; font-family: ui-sans-serif, system-ui, sans-serif; }
    .neon-border { border: 1px solid rgba(16, 185, 129, 0.3); }
    .pulse-dot { animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; }
    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: .3; } }
  </style>
</head>
<body class="p-6">
  <div class="max-w-7xl mx-auto space-y-6">
    <!-- Header Banner -->
    <header class="flex items-center justify-between pb-4 border-b border-slate-800">
      <div class="flex items-center gap-3">
        <div class="p-2.5 bg-emerald-950/80 border border-emerald-500/40 rounded-xl text-emerald-400">
          <i class="fa-solid fa-shield-halved text-xl"></i>
        </div>
        <div>
          <h1 class="text-xl font-bold tracking-tight text-white flex items-center gap-2">
            AirgapShield <span class="text-xs font-mono font-normal bg-emerald-500/20 text-emerald-400 px-2 py-0.5 rounded border border-emerald-500/30">Zero-Exfiltration</span>
          </h1>
          <p class="text-xs text-slate-400">On-Device GraphRAG & Autonomous Incident Commander running on AlloyDB Omni & Local Gemma 4</p>
        </div>
      </div>
      <div class="flex items-center gap-4 text-xs font-mono">
        <span class="flex items-center gap-1.5 bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-lg text-emerald-400">
          <span class="h-2 w-2 rounded-full bg-emerald-400 pulse-dot"></span> AIR-GAPPED PERIMETER
        </span>
        <span class="bg-indigo-950/50 border border-indigo-700/50 text-indigo-300 px-3 py-1.5 rounded-lg">
          AlloyDB Omni + pgvector
        </span>
        <span class="bg-purple-950/50 border border-purple-700/50 text-purple-300 px-3 py-1.5 rounded-lg">
          Gemma 4 Local (Ollama)
        </span>
      </div>
    </header>

    <!-- Main Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
      <!-- Left Column: SCADA Telemetry & Anomaly Trigger (7 Cols) -->
      <div class="lg:col-span-7 space-y-5">
        <!-- Telemetry Feeds -->
        <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-5 space-y-4">
          <div class="flex items-center justify-between">
            <h2 class="text-sm font-semibold uppercase tracking-wider text-slate-300 flex items-center gap-2">
              <i class="fa-solid fa-network-wired text-emerald-400"></i> Cyber-Physical Substation Telemetry
            </h2>
            <button onclick="triggerAnomalySimulation()" class="bg-rose-600 hover:bg-rose-500 text-white text-xs font-semibold px-3 py-1.5 rounded-lg transition shadow-lg shadow-rose-950/50 flex items-center gap-1.5">
              <i class="fa-solid fa-triangle-exclamation"></i> Inject Modbus Lateral Attack
            </button>
          </div>

          <div class="grid grid-cols-3 gap-3">
            <div class="bg-slate-950/70 p-3 rounded-lg border border-slate-800">
              <span class="text-[10px] text-slate-500 uppercase font-mono">Asset ID</span>
              <p class="font-mono text-xs font-bold text-white">PLC-GEN-01</p>
              <p class="text-[10px] text-amber-400 mt-1"><i class="fa-solid fa-circle-exclamation"></i> Cavitation Warning</p>
            </div>
            <div class="bg-slate-950/70 p-3 rounded-lg border border-slate-800">
              <span class="text-[10px] text-slate-500 uppercase font-mono">Cooling Loop</span>
              <p class="font-mono text-xs font-bold text-white">VALVE-COOL-09</p>
              <p class="text-[10px] text-rose-400 mt-1"><i class="fa-solid fa-bolt"></i> Clamp at 12% Flow</p>
            </div>
            <div class="bg-slate-950/70 p-3 rounded-lg border border-slate-800">
              <span class="text-[10px] text-slate-500 uppercase font-mono">Step-Down Bus</span>
              <p class="font-mono text-xs font-bold text-white">BUS-TRANS-04</p>
              <p class="text-[10px] text-orange-400 mt-1"><i class="fa-solid fa-temperature-arrow-up"></i> Temp: 94.2 C</p>
            </div>
          </div>
        </div>

        <!-- Multi-Hop GraphRAG & Vector Similarity View -->
        <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-5 space-y-3">
          <h2 class="text-sm font-semibold uppercase tracking-wider text-slate-300 flex items-center gap-2">
            <i class="fa-solid fa-diagram-project text-indigo-400"></i> Local AlloyDB Omni Graph & Vector Context
          </h2>
          <div class="grid grid-cols-2 gap-3 text-xs font-mono">
            <div class="bg-slate-950 p-3 rounded-lg border border-slate-800 space-y-2">
              <span class="text-indigo-400 font-bold">1. Multi-Hop Graph Traversal</span>
              <div class="text-[11px] text-slate-400 space-y-1">
                <p>PLC-GEN-01 <span class="text-slate-600">--[CONTROLS]--></span> VALVE-COOL-09</p>
                <p>VALVE-COOL-09 <span class="text-slate-600">--[SHARED_COOLING]--></span> BUS-TRANS-04</p>
                <p class="text-emerald-400 text-[10px]">> Recursive Depth: 2 hops (15ms)</p>
              </div>
            </div>
            <div class="bg-slate-950 p-3 rounded-lg border border-slate-800 space-y-2">
              <span class="text-purple-400 font-bold">2. Local pgvector Cosine Match</span>
              <div class="text-[11px] text-slate-400 space-y-1">
                <p>Top Match: <strong>VALVE-COOL-09</strong> (dist: 0.084)</p>
                <p>Prior Incident: Unauthorized setpoint override</p>
                <p class="text-emerald-400 text-[10px]">> EmbeddingGemma: 768 dims on CPU</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column: Autonomous Local Gemma 4 Incident Response (5 Cols) -->
      <div class="lg:col-span-5 bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col space-y-4">
        <div class="flex items-center justify-between pb-3 border-b border-slate-800">
          <div class="flex items-center gap-2">
            <div class="h-2 w-2 rounded-full bg-emerald-400 pulse-dot"></div>
            <h3 class="text-sm font-bold text-white">Gemma 4 Tactical Commander</h3>
          </div>
          <span class="text-[10px] font-mono bg-purple-500/20 text-purple-300 px-2 py-0.5 rounded border border-purple-500/30">Local Model</span>
        </div>

        <div id="aiResponsePanel" class="flex-1 bg-slate-950 p-4 rounded-lg border border-slate-800/80 font-sans text-xs leading-relaxed space-y-3 overflow-y-auto max-h-[460px]">
          <p class="text-slate-400 italic">Click "Inject Modbus Lateral Attack" to trigger real-time on-device GraphRAG correlation and autonomous tactical incident triage.</p>
        </div>
      </div>
    </div>
  </div>

  <script>
    async function triggerAnomalySimulation() {
      const panel = document.getElementById("aiResponsePanel");
      panel.innerHTML = '<p class="text-amber-400 font-mono"><i class="fa-solid fa-spinner fa-spin"></i> Ingesting telemetry -> executing on-device GraphRAG traversal & local Gemma 4 synthesis...</p>';

      try {
        const res = await fetch("/api/triage", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({
            root_asset: "PLC-GEN-01",
            anomaly_summary: "Severe flow cavitation detected; condenser heat dissipation dropped 78% following unauthorized setpoint delta."
          })
        });
        const data = await res.json();
        panel.innerHTML = data.analysis.replace(/\\n/g, '<br>').replace(/### (.*?)(<br>|$)/g, '<h4 class="font-bold text-emerald-400 mt-2 mb-1">$1</h4>');
      } catch (err) {
        panel.innerHTML = '<p class="text-rose-400">Simulation Error: ' + err + '</p>';
      }
    }
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_DASHBOARD)

@app.route("/api/triage", methods=["POST"])
def api_triage():
    data = request.json or {}
    root_asset = data.get("root_asset", "PLC-GEN-01")
    anomaly_summary = data.get("anomaly_summary", "Modbus unauthorized override on cooling valve")
    
    analysis = agent.synthesize_gemma_incident_response(root_asset, anomaly_summary)
    return jsonify({
        "status": "success",
        "root_asset": root_asset,
        "analysis": analysis
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8088))
    app.run(host="0.0.0.0", port=port, debug=False)
