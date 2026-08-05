import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from '@/components/Layout'

// Pages
import DashboardPage from '@/pages/DashboardPage'
import ProfilePage from '@/pages/ProfilePage'
import UniversitiesPage from '@/pages/UniversitiesPage'
import UniversityDetailPage from '@/pages/UniversityDetailPage'
import ComparisonPage from '@/pages/ComparisonPage'
import BudgetPage from '@/pages/BudgetPage'
import ScholarshipsPage from '@/pages/ScholarshipsPage'
import TimelinePage from '@/pages/TimelinePage'
import ReportsPage from '@/pages/ReportsPage'
import ChatPage from '@/pages/ChatPage'

// Authentication is disabled – app is fully open
export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard"        element={<DashboardPage />} />
        <Route path="profile"          element={<ProfilePage />} />
        <Route path="universities"     element={<UniversitiesPage />} />
        <Route path="universities/:id" element={<UniversityDetailPage />} />
        <Route path="compare"          element={<ComparisonPage />} />
        <Route path="budget"           element={<BudgetPage />} />
        <Route path="scholarships"     element={<ScholarshipsPage />} />
        <Route path="timeline"         element={<TimelinePage />} />
        <Route path="reports"          element={<ReportsPage />} />
        <Route path="chat"             element={<ChatPage />} />
      </Route>

      {/* Redirect any unknown path to dashboard */}
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  )
}
