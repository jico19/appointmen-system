import React from 'react';
import { useAuth } from '../context/AuthContext';

const AdminDashboard = () => {
    const { user, logout } = useAuth();
    return (
        <div className="p-8 bg-purple-50 min-h-screen">
            <h1 className="text-3xl font-bold text-purple-800">Admin Control Center</h1>
            <p className="mt-2 text-purple-600">Managing the system as: <strong>{user?.username}</strong></p>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
                <div className="p-6 bg-white rounded-xl shadow-sm border border-purple-100">
                    <h3 className="font-semibold text-lg">User Management</h3>
                    <p className="text-gray-500 text-sm mt-2">Create, edit, and deactivate users.</p>
                </div>
                <div className="p-6 bg-white rounded-xl shadow-sm border border-purple-100">
                    <h3 className="font-semibold text-lg">System Logs</h3>
                    <p className="text-gray-500 text-sm mt-2">View application and security logs.</p>
                </div>
                <div className="p-6 bg-white rounded-xl shadow-sm border border-purple-100">
                    <h3 className="font-semibold text-lg">Configurations</h3>
                    <p className="text-gray-500 text-sm mt-2">Global system settings.</p>
                </div>
            </div>

            <button 
                onClick={logout}
                className="mt-8 px-6 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition shadow-md"
            >
                Logout
            </button>
        </div>
    );
};

export default AdminDashboard;
