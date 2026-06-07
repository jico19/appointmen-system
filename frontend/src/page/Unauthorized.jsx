import React from 'react';
import { Link } from 'react-router-dom';

const Unauthorized = () => {
    return (
        <div className="p-8 text-center">
            <h1 className="text-4xl font-bold text-red-600">403 - Unauthorized</h1>
            <p className="mt-4">You do not have permission to view this page.</p>
            <Link to="/" className="mt-4 text-blue-500 underline block">Go to Dashboard</Link>
        </div>
    );
};

export default Unauthorized;
