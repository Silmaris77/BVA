'use client'

import { startTransition, useState, useMemo } from 'react'
import { DollarSign, PieChart, Info, ArrowRight, Download } from 'lucide-react'
import { useAuth } from '@/contexts/AuthContext'

export default function ROICalculator() {
    // State
    const { refreshProfile } = useAuth()
    const [price, setPrice] = useState(10000)
    const [savings, setSavings] = useState(2500)
    const [timeFrame, setTimeFrame] = useState(12) // months
    const [efficiency, setEfficiency] = useState(15) // % increase
    const [teamSize, setTeamSize] = useState(5)

    // Save State
    const [isSaving, setIsSaving] = useState(false)
    const [lastSaved, setLastSaved] = useState<Date | null>(null)

    // Calculations
    const annualSavings = savings * 12
    const efficiencyGainValue = (teamSize * 5000) * (efficiency / 100) * 12 // Assuming 5k/employee/mo cost base
    const totalBenefitFirstYear = annualSavings + efficiencyGainValue
    const roiFirstYear = ((totalBenefitFirstYear - price) / price) * 100
    const breakEvenMonths = price / (savings + ((teamSize * 5000) * (efficiency / 100)))

    // Formatting
    const formatCurrency = (val: number) => new Intl.NumberFormat('pl-PL', { style: 'currency', currency: 'PLN', maximumFractionDigits: 0 }).format(val)

    const handleSave = async () => {
        setIsSaving(true)
        try {
            const response = await fetch('/api/tools/usage', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    tool_id: 'roi-calculator',
                    input_data: { price, savings, timeFrame, efficiency, teamSize },
                    output_data: { annualSavings, efficiencyGainValue, totalBenefitFirstYear, roiFirstYear, breakEvenMonths }
                })
            })

            const data = await response.json()
            if (data.success) {
                if (data.xp_awarded > 0) {
                    await refreshProfile()
                }
                setLastSaved(new Date())
            }
        } catch (error) {
            console.error('Failed to save tool usage:', error)
        } finally {
            setIsSaving(false)
        }
    }

    return (
        <div style={{
            background: 'rgba(20, 20, 35, 0.4)',
            backdropFilter: 'blur(15px)',
            border: '1px solid rgba(255,255,255,0.08)',
            borderRadius: '20px',
            padding: '32px'
        }}>
            <h3 style={{ fontSize: '18px', fontWeight: 600, marginBottom: '24px', color: '#ff8800', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <PieChart size={20} /> Kalkulator ROI
            </h3>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '40px' }}>
                {/* Inputs */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>

                    {/* Input Group */}
                    <div>
                        <label style={{ display: 'block', marginBottom: '8px', fontSize: '14px', color: 'rgba(255,255,255,0.8)' }}>
                            Koszt Inwestycji (PLN)
                        </label>
                        <input
                            type="range"
                            min="1000" max="100000" step="1000"
                            value={price}
                            onChange={(e) => setPrice(Number(e.target.value))}
                            style={{ width: '100%', marginBottom: '8px', accentColor: '#ff8800' }}
                        />
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <span style={{ fontSize: '12px', color: 'rgba(255,255,255,0.5)' }}>1k</span>
                            <div style={{
                                background: 'rgba(0,0,0,0.3)',
                                padding: '4px 12px',
                                borderRadius: '6px',
                                border: '1px solid rgba(255,255,255,0.1)',
                                color: '#fff',
                                fontWeight: 600
                            }}>
                                {formatCurrency(price)}
                            </div>
                            <span style={{ fontSize: '12px', color: 'rgba(255,255,255,0.5)' }}>100k</span>
                        </div>
                    </div>

                    {/* Input Group */}
                    <div>
                        <label style={{ display: 'block', marginBottom: '8px', fontSize: '14px', color: 'rgba(255,255,255,0.8)' }}>
                            Miesięczne Oszczędności (PLN)
                        </label>
                        <input
                            type="range"
                            min="100" max="20000" step="100"
                            value={savings}
                            onChange={(e) => setSavings(Number(e.target.value))}
                            style={{ width: '100%', marginBottom: '8px', accentColor: '#00ff88' }}
                        />
                        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
                            <div style={{
                                background: 'rgba(0,0,0,0.3)',
                                padding: '4px 12px',
                                borderRadius: '6px',
                                border: '1px solid rgba(255,255,255,0.1)',
                                color: '#00ff88',
                                fontWeight: 600
                            }}>
                                {formatCurrency(savings)}
                            </div>
                        </div>
                    </div>

                    {/* Input Group */}
                    <div>
                        <label style={{ display: 'block', marginBottom: '8px', fontSize: '14px', color: 'rgba(255,255,255,0.8)' }}>
                            Wzrost Efektywności (%)
                        </label>
                        <input
                            type="range"
                            min="0" max="100" step="1"
                            value={efficiency}
                            onChange={(e) => setEfficiency(Number(e.target.value))}
                            style={{ width: '100%', marginBottom: '8px', accentColor: '#00d4ff' }}
                        />
                        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
                            <div style={{
                                background: 'rgba(0,0,0,0.3)',
                                padding: '4px 12px',
                                borderRadius: '6px',
                                border: '1px solid rgba(255,255,255,0.1)',
                                color: '#00d4ff',
                                fontWeight: 600
                            }}>
                                {efficiency}%
                            </div>
                        </div>
                    </div>

                    {/* Input Group */}
                    <div>
                        <label style={{ display: 'block', marginBottom: '8px', fontSize: '14px', color: 'rgba(255,255,255,0.8)' }}>
                            Wielkość Zespołu
                        </label>
                        <div style={{ display: 'flex', gap: '8px' }}>
                            {[1, 5, 10, 20, 50].map((size) => (
                                <button
                                    key={size}
                                    onClick={() => setTeamSize(size)}
                                    style={{
                                        padding: '8px 16px',
                                        borderRadius: '8px',
                                        border: size === teamSize ? '1px solid #ff8800' : '1px solid rgba(255,255,255,0.1)',
                                        background: size === teamSize ? 'rgba(255,136,0,0.2)' : 'rgba(255,255,255,0.05)',
                                        color: size === teamSize ? '#ff8800' : 'rgba(255,255,255,0.6)',
                                        cursor: 'pointer'
                                    }}
                                >
                                    {size} os.
                                </button>
                            ))}
                        </div>
                    </div>

                </div>

                {/* Results Visual */}
                <div style={{
                    background: 'rgba(0, 0, 0, 0.2)',
                    borderRadius: '16px',
                    padding: '24px',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'center'
                }}>
                    <div style={{ textAlign: 'center', marginBottom: '32px' }}>
                        <div style={{ fontSize: '14px', color: 'rgba(255,255,255,0.5)', marginBottom: '8px' }}>
                            ROI po 1 roku
                        </div>
                        <div style={{
                            fontSize: '48px',
                            fontWeight: 800,
                            color: roiFirstYear > 0 ? '#00ff88' : '#ef4444',
                            textShadow: roiFirstYear > 0 ? '0 0 30px rgba(0,255,136,0.2)' : 'none'
                        }}>
                            {roiFirstYear.toFixed(0)}%
                        </div>
                        <div style={{ fontSize: '14px', color: roiFirstYear > 0 ? '#00ff88' : '#ef4444', opacity: 0.8 }}>
                            {roiFirstYear > 0 ? 'Inwestycja opłacalna' : 'Zbyt wysoki koszt'}
                        </div>
                    </div>

                    <div style={{ display: 'flex', gap: '16px', marginBottom: '24px' }}>
                        <div style={{ flex: 1, background: 'rgba(255,255,255,0.05)', padding: '16px', borderRadius: '12px' }}>
                            <div style={{ fontSize: '12px', color: 'rgba(255,255,255,0.5)', marginBottom: '4px' }}>Całkowity Zwrot</div>
                            <div style={{ fontSize: '18px', fontWeight: 600, color: '#fff' }}>{formatCurrency(totalBenefitFirstYear)}</div>
                        </div>
                        <div style={{ flex: 1, background: 'rgba(255,255,255,0.05)', padding: '16px', borderRadius: '12px' }}>
                            <div style={{ fontSize: '12px', color: 'rgba(255,255,255,0.5)', marginBottom: '4px' }}>Zwrot inwestycji (BEP)</div>
                            <div style={{ fontSize: '18px', fontWeight: 600, color: '#fff' }}>{breakEvenMonths.toFixed(1)} msc</div>
                        </div>
                    </div>

                    <button
                        onClick={handleSave}
                        disabled={isSaving}
                        style={{
                            width: '100%',
                            padding: '16px',
                            background: lastSaved ? 'linear-gradient(135deg, #00ff88, #00d4ff)' : 'linear-gradient(135deg, #ff8800, #ff5500)',
                            border: 'none',
                            borderRadius: '12px',
                            color: lastSaved ? '#000' : 'white',
                            fontSize: '16px',
                            fontWeight: 700,
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            gap: '8px',
                            transition: 'all 0.3s',
                            boxShadow: lastSaved ? '0 0 20px rgba(0, 255, 136, 0.4)' : '0 4px 20px rgba(255, 136, 0, 0.3)',
                            opacity: isSaving ? 0.7 : 1
                        }}>
                        <Download size={20} />
                        {isSaving ? 'Zapisywanie...' : lastSaved ? 'Zapisano! (Eksportuj PDF)' : 'Zapisz i Eksportuj PDF'}
                    </button>
                    <div style={{ textAlign: 'center', marginTop: '12px', fontSize: '12px', color: 'rgba(255,255,255,0.4)' }}>
                        Generuje raport + zapisuje wynik (XP)
                    </div>
                </div>
            </div>
        </div>
    )
}
