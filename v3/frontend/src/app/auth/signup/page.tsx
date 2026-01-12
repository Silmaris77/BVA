'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import Link from 'next/link'

export default function SignupPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [fullName, setFullName] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)
  const [loading, setLoading] = useState(false)
  const { signUp } = useAuth()
  const router = useRouter()

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await signUp(email, password, fullName)
      setSuccess(true)
    } catch (err: any) {
      setError(err.message || 'Failed to create account')
      setLoading(false)
    }
  }

  if (success) {
    return (
      <>
        <style jsx>{`
          .container {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
          }
          .glass-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            padding: 40px;
            max-width: 420px;
            width: 100%;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            text-align: center;
          }
          .icon {
            font-size: 4rem;
            margin-bottom: 16px;
          }
          h1 {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 16px;
          }
          .text {
            color: rgba(255, 255, 255, 0.7);
            margin-bottom: 24px;
          }
          .btn-glow {
            display: inline-block;
            padding: 16px 32px;
            background: linear-gradient(135deg, #a855f7, #6366f1);
            border-radius: 12px;
            color: white;
            text-decoration: none;
            font-weight: 600;
            box-shadow: 0 4px 20px rgba(168, 85, 247, 0.4);
          }
        `}</style>
        <div className="container">
          <div className="glass-card">
            <div className="icon">✅</div>
            <h1>Sprawdź swoją skrzynkę!</h1>
            <p className="text">
              Wysłaliśmy link aktywacyjny na <strong>{email}</strong>. Kliknij w niego, aby aktywować konto.
            </p>
            <Link href="/auth/login" className="btn-glow">Przejdź do logowania</Link>
          </div>
        </div>
      </>
    )
  }

  return (
    <>
      <style jsx>{`
        .container {
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 20px;
        }
        .glass-card {
          background: rgba(255, 255, 255, 0.1);
          backdrop-filter: blur(20px);
          -webkit-backdrop-filter: blur(20px);
          border: 1px solid rgba(255, 255, 255, 0.2);
          border-radius: 20px;
          padding: 40px;
          max-width: 420px;
          width: 100%;
          box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        h1 {
          font-size: 2rem;
          font-weight: 700;
          margin-bottom: 8px;
          text-align: center;
        }
        .subtitle {
          text-align: center;
          color: rgba(255, 255, 255, 0.6);
          margin-bottom: 32px;
        }
        .form-group {
          margin-bottom: 20px;
        }
        .label {
          display: block;
          margin-bottom: 8px;
          font-size: 0.875rem;
          color: rgba(255, 255, 255, 0.8);
        }
        .input {
          width: 100%;
          padding: 14px 16px;
          border-radius: 10px;
          background: rgba(255, 255, 255, 0.1);
          border: 1px solid rgba(255, 255, 255, 0.2);
          color: white;
          font-size: 1rem;
          font-family: 'Outfit', sans-serif;
          outline: none;
          transition: border-color 0.3s, background 0.3s;
          box-sizing: border-box;
        }
        .input::placeholder {
          color: rgba(255, 255, 255, 0.4);
        }
        .input:focus {
          border-color: #a855f7;
          background: rgba(255, 255, 255,0.15);
        }
        .input:-webkit-autofill,
        .input:-webkit-autofill:hover,
        .input:-webkit-autofill:focus,
        .input:-webkit-autofill:active {
          -webkit-background-clip: text !important;
          -webkit-text-fill-color: white !important;
          background-color: transparent !important;
          box-shadow: 0 0 0 1000px rgba(255, 255, 255, 0.1) inset !important;
          caret-color: white !important;
          filter: none !important;
        }
        .hint {
          font-size: 0.75rem;
          color: rgba(255, 255, 255, 0.5);
          margin-top: 6px;
        }
        .error-box {
          background: rgba(239, 68, 68, 0.2);
          border: 1px solid #ef4444;
          color: #fca5a5;
          padding: 12px 16px;
          border-radius: 10px;
          margin-bottom: 20px;
        }
        .btn-glow {
          width: 100%;
          padding: 16px 32px;
          background: linear-gradient(135deg, #a855f7, #6366f1);
          border: none;
          border-radius: 12px;
          color: white;
          font-size: 1rem;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s ease;
          box-shadow: 0 4px 20px rgba(168, 85, 247, 0.4);
          margin-top: 8px;
        }
        .btn-glow:hover {
          transform: translateY(-2px);
          box-shadow: 0 6px 30px rgba(168, 85, 247, 0.6);
        }
        .btn-glow:disabled {
          opacity: 0.7;
          cursor: not-allowed;
        }
        .footer-text {
          text-align: center;
          margin-top: 24px;
          font-size: 0.875rem;
          color: rgba(255, 255, 255, 0.6);
        }
        .link {
          color: #f0abfc !important;
          text-decoration: none;
          font-weight: 600;
        }
        .link:hover {
          text-decoration: underline;
          color: #fde4ff !important;
        }
      `}</style>

      <div className="container">
        <div className="glass-card">
          <h1>Utwórz konto</h1>
          <p className="subtitle">Rozpocznij swoją naukę</p>

          {error && <div className="error-box">{error}</div>}

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="label">Imię i nazwisko</label>
              <input
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                className="input"
                placeholder="Jan Kowalski"
                required
              />
            </div>

            <div className="form-group">
              <label className="label">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="input"
                placeholder="your@email.com"
                required
              />
            </div>

            <div className="form-group">
              <label className="label">Hasło</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input"
                placeholder="••••••••"
                required
                minLength={6}
              />
              <p className="hint">Minimum 6 znaków</p>
            </div>

            <button type="submit" disabled={loading} className="btn-glow">
              {loading ? 'Tworzenie konta...' : 'Zarejestruj się'}
            </button>
          </form>

          <p className="footer-text">
            Masz już konto?{' '}
            <Link href="/auth/login" style={{ color: '#f0abfc', fontWeight: 600, textDecoration: 'none' }}>Zaloguj się</Link>
          </p>
        </div>
      </div>
    </>
  )
}
