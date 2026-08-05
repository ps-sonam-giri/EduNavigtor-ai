import { Navigate } from 'react-router-dom'

// Authentication removed – redirect straight to dashboard
export default function RegisterPage() {
  return <Navigate to="/dashboard" replace />
}
