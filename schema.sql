-- =====================================================================
-- AirgapShield: Database Schema & Hybrid Graph-Vector Definitions
-- Target: Google Cloud AlloyDB Omni (Air-Gapped Local Deployment)
-- =====================================================================

-- 1. Enable Core Extensions
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. Critical Infrastructure Asset Inventory (Graph Nodes)
CREATE TABLE IF NOT EXISTS assets (
    asset_id VARCHAR(64) PRIMARY KEY,
    asset_name VARCHAR(128) NOT NULL,
    substation_zone VARCHAR(64) NOT NULL,
    criticality_tier INT DEFAULT 1, -- 1: Highest (Reactor/Main Grid), 3: Auxiliary
    operational_status VARCHAR(32) DEFAULT 'NORMAL',
    ip_internal INET,
    last_calibrated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Cyber-Physical Asset Dependency Graph (Graph Edges / Multi-Hop Topology)
CREATE TABLE IF NOT EXISTS asset_dependencies (
    dependency_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_asset_id VARCHAR(64) REFERENCES assets(asset_id),
    target_asset_id VARCHAR(64) REFERENCES assets(asset_id),
    relationship_type VARCHAR(64) NOT NULL, -- e.g., 'POWERS', 'CONTROLS_VALVE', 'DATA_TELEMETRY', 'SHARED_BUS'
    isolation_latency_ms INT DEFAULT 15,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. SCADA Time-Series Telemetry & Semantic Vector Storage (Hybrid Vector Store)
CREATE TABLE IF NOT EXISTS scada_telemetry (
    telemetry_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_id VARCHAR(64) REFERENCES assets(asset_id),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    temperature_celsius NUMERIC(6, 2),
    pressure_psi NUMERIC(6, 2),
    bus_voltage_kv NUMERIC(6, 2),
    frequency_hz NUMERIC(5, 2),
    vibration_amplitude_mm NUMERIC(5, 3),
    raw_event_log TEXT,
    -- 768-dimensional embeddings generated locally by on-device EmbeddingGemma-300m
    embedding vector(768)
);

-- Index for Accelerated On-Device Approximate Nearest Neighbor Search
CREATE INDEX IF NOT EXISTS scada_vector_idx 
ON scada_telemetry 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 10);

-- 5. Tactical Incident Log & Containment History
CREATE TABLE IF NOT EXISTS incident_playbooks (
    incident_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    root_cause_asset_id VARCHAR(64) REFERENCES assets(asset_id),
    severity_level VARCHAR(32) NOT NULL, -- CRITICAL, HIGH, MEDIUM
    causal_chain_path TEXT,              -- Multi-hop graph traversal path
    gemma_tactical_assessment TEXT,      -- Local Gemma 4 synthesis
    containment_status VARCHAR(32) DEFAULT 'MITIGATING'
);

-- =====================================================================
-- Seed Data: Industrial Grid Substation Alpha (Under Simulation Attack)
-- =====================================================================

INSERT INTO assets (asset_id, asset_name, substation_zone, criticality_tier, operational_status, ip_internal) VALUES
('PLC-GEN-01', 'Steam Turbine Primary PLC', 'Zone-1-Generation', 1, 'ANOMALY_WARNING', '10.240.10.11'),
('BUS-TRANS-04', '400kV Step-Down Transformer Bus', 'Zone-2-Transmission', 1, 'HIGH_THERMAL_LOAD', '10.240.10.14'),
('VALVE-COOL-09', 'Condenser Cooling Bypass Valve', 'Zone-1-Generation', 2, 'UNAUTHORIZED_OVERRIDE', '10.240.10.19'),
('RTU-SCADA-01', 'Substation Remote Terminal Unit', 'Zone-0-Supervisory', 1, 'NORMAL', '10.240.10.2');

-- Graph Relationships
INSERT INTO asset_dependencies (source_asset_id, target_asset_id, relationship_type) VALUES
('RTU-SCADA-01', 'PLC-GEN-01', 'POLL_TELEMETRY'),
('PLC-GEN-01', 'VALVE-COOL-09', 'CONTROLS_VALVE'),
('VALVE-COOL-09', 'BUS-TRANS-04', 'SHARED_COOLING_LOOP');
