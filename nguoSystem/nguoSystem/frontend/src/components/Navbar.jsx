import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Navbar.css';

const Navbar = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          <h2>🧵 Nguo System</h2>
        </Link>
        
        <ul className="navbar-menu">
          <li><Link to="/">Nyumbani</Link></li>
          <li><Link to="/styles">Mitindo</Link></li>
          
          {isAuthenticated ? (
            <>
              <li><Link to="/orders">Oda Zangu</Link></li>
              <li><Link to="/feedback">Maoni</Link></li>
              <li><Link to="/custom-styles">Ombi la Mtindo</Link></li>
              
              {user?.role === 'tailor' && (
                <li><Link to="/tailor/dashboard">Dashboard ya Mshonaji</Link></li>
              )}
              
              {user?.role === 'superuser' && (
                <li><Link to="/admin">Admin</Link></li>
              )}
              
              <li className="navbar-user">
                <span>👤 {user?.full_name || user?.email}</span>
              </li>
              <li>
                <button onClick={handleLogout} className="btn-logout">
                  Toka
                </button>
              </li>
            </>
          ) : (
            <>
              <li><Link to="/login">Ingia</Link></li>
              <li><Link to="/register" className="btn-register">Sajili</Link></li>
            </>
          )}
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
