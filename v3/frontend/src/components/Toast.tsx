'use client'

import { useEffect } from 'react'

interface ToastProps {
    message: string
    type?: 'success' | 'error' | 'info'
    onClose: () => void
}

export default function Toast({ message, type = 'success', onClose }: ToastProps) {
    useEffect(() => {
        const timer = setTimeout(onClose, 3000)
        return () => clearTimeout(timer)
    }, [onClose])

    const colors = {
        success: { bg: '#00ff88', border: '#00ff88' },
        error: { bg: '#ef4444', border: '#ef4444' },
        info: { bg: '#00d4ff', border: '#00d4ff' }
    }

    return (
        <div style={{
            position: 'fixed',
            bottom: '24px',
            right: '24px',
            padding: '16px 24px',
            background: `${colors[type].bg}20`,
            border: `1px solid ${colors[type].border}`,
            borderRadius: '12px',
            color: 'white',
            fontWeight: 500,
            boxShadow: '0 8px 32px rgba(0, 0, 0, 0.4)',
            animation: 'slideUp 0.3s ease, fadeOut 0.3s ease 2.7s',
            zIndex: 9999,
            backdropFilter: 'blur(10px)',
            WebkitBackdropFilter: 'blur(10px)',
            fontSize: '14px'
        }}>
            <style>{`
        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        @keyframes fadeOut {
          to {
            opacity: 0;
            transform: translateY(-10px);
          }
        }
      `}</style>
            {message}
        </div>
    )
}
