import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

/**
 * ProtectedRoute component for RBAC.
 * @param {Object} props
 * @param {Array} props.allowedRoles - List of roles that can access this route.
 * @param {React.ReactNode} props.children - Component to render if authorized.
 */
const ProtectedRoute = ({ allowedRoles, children }) => {
    const { user, loading } = useAuth();
    const location = useLocation();

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
            </div>
        );
    }

    if (!user) {
        // Not logged in: redirect to login
        return <Navigate to="/login" state={{ from: location }} replace />;
    }

    if (allowedRoles) {
        // Robust role check: case-insensitive and handle missing role
        const userRole = (user.role || '').toUpperCase();
        const hasAccess = allowedRoles.some(role => role.toUpperCase() === userRole);

        if (!hasAccess) {
            return <Navigate to="/unauthorized" replace />;
        }
    }

    return children;
};

export default ProtectedRoute;
