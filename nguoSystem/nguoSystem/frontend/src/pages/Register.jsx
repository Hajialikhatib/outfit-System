import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Auth.css';

const Register = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    password2: '',
    full_name: '',
    phone: '',
    address: '',
    gender: '',
    is_tailor: false,
    tailor_type: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    setFormData({
      ...formData,
      [e.target.name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    // Validate passwords match
    if (formData.password !== formData.password2) {
      setError('Maneno ya siri hayaendani');
      return;
    }

    setLoading(true);
    const result = await register(formData);
    setLoading(false);

    if (result.success) {
      setSuccess('Umesajiliwa! Tafadhali ingia.');
      setTimeout(() => navigate('/login'), 2000);
    } else {
      setError(result.error);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card register-card">
        <h2>Sajili Akaunti Mpya</h2>
        
        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="full_name">Jina Kamili</label>
              <input
                type="text"
                id="full_name"
                name="full_name"
                value={formData.full_name}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="email">Barua pepe</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="phone">Simu</label>
              <input
                type="tel"
                id="phone"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="gender">Jinsia</label>
              <select
                id="gender"
                name="gender"
                value={formData.gender}
                onChange={handleChange}
                required
              >
                <option value="">Chagua jinsia</option>
                <option value="kiume">Kiume</option>
                <option value="kike">Kike</option>
              </select>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="address">Anwani</label>
            <input
              type="text"
              id="address"
              name="address"
              value={formData.address}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="password">Neno la siri</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                minLength="8"
              />
            </div>

            <div className="form-group">
              <label htmlFor="password2">Thibitisha neno la siri</label>
              <input
                type="password"
                id="password2"
                name="password2"
                value={formData.password2}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="form-group checkbox-group">
            <label>
              <input
                type="checkbox"
                name="is_tailor"
                checked={formData.is_tailor}
                onChange={handleChange}
              />
              <span>Je, wewe ni mshonaji?</span>
            </label>
          </div>

          {formData.is_tailor && (
            <div className="form-group">
              <label htmlFor="tailor_type">Aina ya Nguo Unazoshona</label>
              <select
                id="tailor_type"
                name="tailor_type"
                value={formData.tailor_type}
                onChange={handleChange}
                required={formData.is_staff}
              >
                <option value="">Chagua aina</option>
                <option value="kiume">Nguo za Kiume</option>
                <option value="kike">Nguo za Kike</option>
                <option value="zote">Zote</option>
              </select>
            </div>
          )}

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Inasajili...' : 'Sajili'}
          </button>
        </form>

        <p className="auth-link">
          Tayari una akaunti? <Link to="/login">Ingia hapa</Link>
        </p>
      </div>
    </div>
  );
};

export default Register;
