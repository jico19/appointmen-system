import { useForm } from 'react-hook-form';
import { useAuth } from '@/context/AuthContext';
import api from '@/client/api';
import { jwtDecode } from 'jwt-decode';
import { useNavigate, useLocation } from 'react-router-dom';
import { useEffect } from 'react';


function LoginPage() {
    const { user, login, loading } = useAuth();
    const { register, handleSubmit, reset, formState: { errors } } = useForm();
    const navigate = useNavigate();
    const location = useLocation();

    // If user is already logged in and not loading, redirect to home
    useEffect(() => {
        if (!loading && user) {
            navigate("/", { replace: true });
        }
    }, [user, loading, navigate]);

    if (loading) return null;

    // Where to go after login (defaults to dashboard)
    const from = location.state?.from?.pathname || "/";

    const handleLogin = async (data) => {
        try {
            const res = await api.post('/api/token/', data);
            const decoded = jwtDecode(res.data.access || res.data.refresh);

            // Simulation: If backend doesn't provide role in JWT yet, we can default it 
            // but in production grade, it should come from the token.
            login(decoded);

            reset();
            navigate(from, { replace: true });
        } catch (error) {
            console.error("Login failed", error);
            alert("Login failed. Check console for details.");
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
            <div className="p-8 bg-white shadow-md rounded-lg w-96">
                <h2 className="text-2xl font-bold mb-6 text-center">Login</h2>
                <form onSubmit={handleSubmit(handleLogin)} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Username</label>
                        <input
                            type="text"
                            {...register('username', { required: "Username is required" })}
                            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                        />
                        {errors.username && <span className="text-red-500 text-xs">{errors.username.message}</span>}
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Password</label>
                        <input
                            type="password"
                            {...register('password', { required: "Password is required" })}
                            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                        />
                        {errors.password && <span className="text-red-500 text-xs">{errors.password.message}</span>}
                    </div>
                    <button
                        type='submit'
                        className="w-full py-2 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition"
                    >
                        Login
                    </button>
                </form>
            </div>
        </div>
    );
}

export default LoginPage;
