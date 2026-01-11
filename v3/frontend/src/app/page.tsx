"use client";

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import {
  LayoutGrid,
  Cpu,
  Zap,
  Crosshair,
  User,
  Shield,
  Power,
  BrainCircuit,
  AlertTriangle,
  ChevronDown,
  Activity,
  Coins,
  Target,
  BookOpen,
  AlertOctagon,
  Crown,
  Mic,
  ScanEye
} from 'lucide-react';
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js';
import { Radar } from 'react-chartjs-2';
import { fetchDashboard, type DashboardData } from '@/utils/api';

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

export default function Home() {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadDashboard() {
      try {
        const data = await fetchDashboard();
        setDashboardData(data);
        setLoading(false);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load dashboard');
        setLoading(false);
      }
    }
    loadDashboard();
  }, []);

  const radarData = dashboardData ? {
    labels: dashboardData.competence.labels,
    datasets: [
      {
        label: 'Current Status',
        data: dashboardData.competence.values,
        fill: true,
        backgroundColor: 'rgba(176, 0, 255, 0.2)',
        borderColor: '#b000ff',
        pointBackgroundColor: '#00d4ff',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: '#00d4ff',
        borderWidth: 2,
        pointRadius: 4,
      },
    ],
  } : null;

  const radarOptions = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      r: {
        angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
        grid: { color: 'rgba(255, 255, 255, 0.1)' },
        pointLabels: { color: 'rgba(255, 255, 255, 0.8)', font: { size: 11, family: 'Outfit' } },
        ticks: { display: false, backdropColor: 'transparent' }
      }
    },
    plugins: {
      legend: { display: false }
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen w-full bg-gradient-to-br from-[#0f0c29] via-[#302b63] to-[#24243e]">
        <div className="text-white text-2xl">
          <BrainCircuit className="animate-pulse w-16 h-16 mx-auto mb-4" />
          <p>Initializing Tactical OS...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-screen w-full bg-gradient-to-br from-[#0f0c29] via-[#302b63] to-[#24243e]">
        <div className="glass-card p-8 max-w-md text-center">
          <AlertTriangle className="w-16 h-16 mx-auto mb-4 text-[#ff0055]" />
          <h2 className="text-2xl font-bold mb-2 text-white">System Error</h2>
          <p className="text-[rgba(255,255,255,0.6)] mb-4">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="btn-glow"
          >
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  if (!dashboardData) return null;

  return (
    <>
      {/* Ambient Orbs */}
      <div className="orb orb-1"></div>
      <div className="orb orb-2"></div>
      <div className="orb orb-3"></div>

      {/* Mobile Header */}
      <div className="mobile-header">
        <div className="mobile-header-content">
          <div className="mobile-logo">
            <div className="logo-icon" style={{ width: '32px', height: '32px' }}>
              <BrainCircuit size={18} color="white" />
            </div>
            <span style={{ fontSize: '0.95rem' }}>TACTICAL OS</span>
          </div>
          <div style={{
            width: '32px',
            height: '32px',
            borderRadius: '50%',
            background: '#64748b',
            border: '2px solid var(--neon-purple)'
          }}></div>
        </div>
      </div>

      {/* Sidebar */}
      <div className="sidebar">
        <div className="logo">
          <div className="logo-icon">
            <BrainCircuit size={24} color="white" />
          </div>
          <span>TACTICAL OS</span>
        </div>

        <div className="nav-group">
          <div className="nav-label">Operations</div>
          <Link href="/" style={{ textDecoration: 'none', color: 'inherit' }}>
            <div className="nav-item active">
              <LayoutGrid size={18} /> War Room
            </div>
          </Link>
          <Link href="/implants" style={{ textDecoration: 'none', color: 'inherit' }}>
            <div className="nav-item">
              <Cpu size={18} /> Neural Implants
            </div>
          </Link>
          <div className="nav-item" style={{ opacity: 0.5, cursor: 'not-allowed' }}>
            <Zap size={18} /> AI Agents
          </div>
          <div className="nav-item" style={{ opacity: 0.5, cursor: 'not-allowed' }}>
            <Crosshair size={18} /> Simulations
          </div>
        </div>

        <div className="nav-group">
          <div className="nav-label">System</div>
          <div className="nav-item">
            <User size={18} /> Cyberdeck
          </div>
          <div className="nav-item">
            <Shield size={18} /> Shadow Ops
          </div>
        </div>

        <div style={{ marginTop: 'auto' }}>
          <div className="nav-item" style={{ color: 'var(--neon-red)', borderColor: 'rgba(255,0,85,0.2)' }}>
            <Power size={18} /> Disconnect
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="main">
        <div className="header">
          <div className="page-title">
            <h1>Witaj, {dashboardData.operator_name}.</h1>
            <p>
              Status Systemu: <span style={{ color: 'var(--neon-blue)' }}>{dashboardData.system_status}</span> • Synchronizacja Kalendarza: <span style={{ color: 'var(--neon-blue)' }}>{dashboardData.calendar_sync}</span>
            </p>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
            <div className="alert-badge">
              <AlertTriangle size={14} />
              MARKET CRASH DETECTED
            </div>

            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '1rem',
              background: 'rgba(0,0,0,0.3)',
              padding: '0.5rem 1rem',
              borderRadius: '50px',
              border: '1px solid var(--glass-border)'
            }}>
              <div style={{
                width: '32px',
                height: '32px',
                borderRadius: '50%',
                background: '#64748b',
                border: '2px solid var(--neon-purple)'
              }}></div>
              <span style={{ fontWeight: 600 }}>{dashboardData.operator_name}</span>
              <ChevronDown size={16} style={{ opacity: 0.5 }} />
            </div>
          </div>
        </div>

        {/* Stats Row */}
        <div className="stats-row">
          <div className="glass-card stat-card">
            <div className="stat-icon" style={{
              color: 'var(--neon-purple)',
              borderColor: 'var(--neon-purple)',
              boxShadow: '0 0 15px rgba(176,0,255,0.2)'
            }}>
              <Zap size={28} />
            </div>
            <div>
              <div className="stat-label">Doświadczenie</div>
              <div className="stat-value">{dashboardData.stats.xp.toLocaleString()} XP</div>
              <div style={{ color: 'var(--neon-purple)', fontSize: '0.7rem', marginTop: '5px' }}>
                {dashboardData.stats.xp_change}
              </div>
            </div>
          </div>

          <div className="glass-card stat-card">
            <div className="stat-icon" style={{
              color: 'var(--neon-blue)',
              borderColor: 'var(--neon-blue)',
              boxShadow: '0 0 15px rgba(0,212,255,0.2)'
            }}>
              <Coins size={28} />
            </div>
            <div>
              <div className="stat-label">Venture Credits</div>
              <div className="stat-value">{dashboardData.stats.vc} VC</div>
              <div style={{ color: 'var(--neon-blue)', fontSize: '0.7rem', marginTop: '5px' }}>
                Access: Level {dashboardData.stats.vc_level}
              </div>
            </div>
          </div>

          <div className="glass-card stat-card">
            <div className="stat-icon" style={{
              color: 'var(--neon-red)',
              borderColor: 'var(--neon-red)',
              boxShadow: '0 0 15px rgba(255,0,85,0.2)'
            }}>
              <Activity size={28} />
            </div>
            <div>
              <div className="stat-label">Neural Link</div>
              <div className="stat-value">{dashboardData.stats.neural_link_status}</div>
              <div style={{ color: 'var(--text-muted)', fontSize: '0.7rem', marginTop: '5px' }}>
                Latency: {dashboardData.stats.neural_link_latency}
              </div>
            </div>
          </div>
        </div>

        {/* Dashboard Grid */}
        <div className="dashboard-grid">
          {/* Left Column */}
          <div className="col">
            <div className="glass-card" style={{ flex: 1 }}>
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: '1.5rem'
              }}>
                <h3 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.8rem' }}>
                  <Target style={{ color: 'var(--neon-blue)' }} />
                  Active Protocols (Missions)
                </h3>
                <button className="btn-glow" style={{ padding: '0.4rem 0.8rem', fontSize: '0.8rem' }}>
                  View All
                </button>
              </div>

              {dashboardData.missions.map((mission) => {
                const iconMap: Record<string, React.ReactNode> = {
                  'book': <BookOpen size={20} />,
                  'alert': <AlertOctagon size={20} />
                };
                return (
                  <div
                    key={mission.id}
                    className="mission-item"
                    style={mission.is_crisis ? {
                      borderColor: 'var(--neon-red)',
                      background: 'rgba(255,0,85,0.05)'
                    } : {}}
                  >
                    <div className="mission-icon" style={mission.is_crisis ? { color: 'var(--neon-red)' } : {}}>
                      {iconMap[mission.icon_type] || <Target size={20} />}
                    </div>
                    <div style={{ flex: 1 }}>
                      <div style={{ fontWeight: 600, color: mission.is_crisis ? '#ff8fa3' : 'white' }}>{mission.title}</div>
                      <div style={{ fontSize: '0.8rem', color: mission.is_crisis ? '#ff8fa3' : 'var(--text-muted)', opacity: mission.is_crisis ? 0.8 : 1, marginTop: '2px' }}>
                        {mission.subtitle}
                      </div>
                    </div>
                    <div style={{ textAlign: 'right', marginRight: '1.5rem' }}>
                      <div style={{ color: 'var(--neon-gold)', fontWeight: 700, fontSize: '0.9rem' }}>{mission.reward_xp}</div>
                      {mission.reward_vc && <div style={{ color: 'var(--neon-blue)', fontSize: '0.8rem' }}>{mission.reward_vc}</div>}
                    </div>
                    <button
                      className="btn-glow"
                      style={mission.is_crisis ? {
                        background: 'var(--neon-red)',
                        borderColor: 'var(--neon-red)'
                      } : {}}
                    >
                      {mission.action}
                    </button>
                  </div>
                );
              })}
            </div>

            <div className="glass-card" style={{ height: '300px', display: 'flex', flexDirection: 'column' }}>
              <h3 style={{
                margin: '0 0 1rem 0',
                fontSize: '1rem',
                color: 'var(--text-muted)',
                textTransform: 'uppercase',
                letterSpacing: '1px'
              }}>
                Competence Radar
              </h3>
              <div style={{ flex: 1, position: 'relative' }}>
                {radarData && <Radar data={radarData} options={radarOptions} />}
              </div>
            </div>
          </div>

          {/* Right Column */}
          <div className="col">
            <div className="glass-card">
              <h3 style={{ margin: '0 0 1.5rem 0', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Crown style={{ color: 'var(--neon-gold)' }} />
                Top Operators
              </h3>

              {dashboardData.top_operators.map((operator) => (
                <div
                  key={operator.rank}
                  className="leaderboard-row"
                  style={operator.is_current_user ? {
                    background: 'rgba(255,255,255,0.05)',
                    padding: '0.5rem',
                    borderRadius: '8px',
                    marginTop: '1rem',
                    border: '1px solid var(--neon-blue)'
                  } : {}}
                >
                  <div style={{ display: 'flex', alignItems: 'center' }}>
                    <div
                      className={operator.rank === 1 ? 'rank-badge rank-1' : 'rank-badge'}
                      style={operator.is_current_user ? { background: 'var(--neon-blue)', color: '#000' } : {}}
                    >
                      {operator.rank}
                    </div>
                    {!operator.is_current_user && (
                      <div style={{
                        width: '24px',
                        height: '24px',
                        borderRadius: '50%',
                        background: operator.rank === 1 ? '#fff' : '#ccc',
                        marginRight: '10px'
                      }}></div>
                    )}
                    <span style={{
                      fontWeight: 600,
                      color: operator.is_current_user ? '#fff' : (operator.rank === 1 ? 'inherit' : 'var(--text-muted)')
                    }}>
                      {operator.name}
                    </span>
                  </div>
                  <span style={{
                    color: operator.is_current_user ? '#fff' : (operator.rank === 1 ? 'var(--neon-purple)' : 'var(--text-muted)'),
                    fontWeight: operator.is_current_user || operator.rank === 1 ? 700 : 600
                  }}>
                    {operator.score}
                  </span>
                </div>
              ))}
            </div>

            <div className="glass-card">
              <h3 style={{ margin: '0 0 1rem 0', fontSize: '1rem' }}>Quick Actions</h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
                <button className="btn-glow" style={{
                  width: '100%',
                  display: 'flex',
                  justifyContent: 'center',
                  gap: '0.5rem'
                }}>
                  <Mic size={20} /> Voice Sim (Marcus)
                </button>
                <button className="btn-glow" style={{
                  width: '100%',
                  display: 'flex',
                  justifyContent: 'center',
                  gap: '0.5rem',
                  background: 'transparent',
                  borderColor: 'rgba(255,255,255,0.2)'
                }}>
                  <ScanEye size={18} /> Run VK Protocol
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile Bottom Navigation */}
      <div className="mobile-nav">
        <div className="mobile-nav-item active">
          <LayoutGrid size={20} />
          <span>War Room</span>
        </div>
        <div className="mobile-nav-item">
          <Zap size={20} />
          <span>AI Agents</span>
        </div>
        <div className="mobile-nav-item">
          <User size={20} />
          <span>Profile</span>
        </div>
        <div className="mobile-nav-item">
          <Target size={20} />
          <span>Missions</span>
        </div>
      </div>
    </>
  );
}
