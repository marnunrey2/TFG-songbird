import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';

function ProtectedRoute({ component: Component, ...rest }) {
    const location = useLocation();
    const isAuthenticated = Boolean(localStorage.getItem('user'));  // replace this with your actual authentication check

    return isAuthenticated ? <Component {...rest} /> : <Navigate to="/login" state={{ from: location }} />;
}

export default ProtectedRoute;