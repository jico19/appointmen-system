import React from 'react';
import { useAuth } from '../context/AuthContext';

const UserDashboard = () => {
    const { user, logout } = useAuth();
    return (
        <div className="p-8 bg-green-50 min-h-screen">
            <h1 className="text-3xl font-bold text-green-800">My Appointments</h1>
            <p className="mt-2 text-green-600">Welcome back, <strong>{user?.username}</strong>!</p>
            
            <div className="mt-8 p-6 bg-white rounded-xl shadow-sm border border-green-100 max-w-2xl">
                <h3 className="font-semibold text-lg">Book New Appointment</h3>
                <p className="text-gray-500 text-sm mt-2">Schedule your next visit with our specialists.</p>
                <button className="mt-4 px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition">
                    Book Now
                </button>
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

export default UserDashboard;
