import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';

function ProtectedRoute({ component: Component, role, ...rest }) {
    const location = useLocation();
    const user = JSON.parse(localStorage.getItem('user'));

    if ((!user) || (role === 'admin' && !user.is_superuser) || (role === 'user' && user.is_superuser)) {
        // User is not authenticated or authorized
        return <Navigate to="/login" state={{ from: location }} />;
    } else {
        // User is authenticated and has the correct role
        return <Component {...rest} />;
    }
}

export default ProtectedRoute;