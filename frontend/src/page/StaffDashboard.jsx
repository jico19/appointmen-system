import React from 'react';
import { useAuth } from '../context/AuthContext';

const StaffDashboard = () => {
    const { user, logout } = useAuth();
    return (
        <div className="p-8 bg-blue-50 min-h-screen">
            <h1 className="text-3xl font-bold text-blue-800">Staff Dashboard</h1>
            <p className="mt-2 text-blue-600">Operational view for: <strong>{user?.username}</strong></p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
                <div className="p-6 bg-white rounded-xl shadow-sm border border-blue-100">
                    <h3 className="font-semibold text-lg">Pending Appointments</h3>
                    <p className="text-gray-500 text-sm mt-2">Review and approve upcoming requests.</p>
                </div>
                <div className="p-6 bg-white rounded-xl shadow-sm border border-blue-100">
                    <h3 className="font-semibold text-lg">Schedule Overview</h3>
                    <p className="text-gray-500 text-sm mt-2">Daily and weekly view of all staff activity.</p>
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

export default StaffDashboard;
