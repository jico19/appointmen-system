import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from "./page/LoginPage";
import AdminDashboard from "./page/AdminDashboard";
import StaffDashboard from "./page/StaffDashboard";
import UserDashboard from "./page/UserDashboard";
import Unauthorized from "./page/Unauthorized";
import ProtectedRoute from "./components/ProtectedRoute";
import { useAuth } from './context/AuthContext';

// Simple component to redirect users to their specific dashboard based on role
const RoleRedirect = () => {
  const { user, loading } = useAuth();

  if (loading) return null; // Or a loader
  if (!user) return <Navigate to="/login" replace />;

  const role = (user.role || '').toUpperCase();

  if (role === 'ADMIN') return <Navigate to="/admin" replace />;
  if (role === 'STAFF') return <Navigate to="/staff" replace />;
  return <Navigate to="/dashboard" replace />;
};

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/unauthorized" element={<Unauthorized />} />

        {/* Entry Point Redirect */}
        <Route path="/" element={<RoleRedirect />} />

        {/* Protected Routes by Role */}
        <Route 
          path="/admin" 
          element={
            <ProtectedRoute allowedRoles={['ADMIN']}>
              <AdminDashboard />
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/staff" 
          element={
            <ProtectedRoute allowedRoles={['STAFF']}>
              <StaffDashboard />
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/dashboard" 
          element={
            <ProtectedRoute allowedRoles={['USER']}>
              <UserDashboard />
            </ProtectedRoute>
          } 
        />

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;