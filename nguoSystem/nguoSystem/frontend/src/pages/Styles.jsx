import { useState, useEffect, useMemo } from 'react';
import { stylesService } from '../services/api';
import { useAuth } from '../context/AuthContext';
import './Styles.css';

const Styles = () => {
  const [styles, setStyles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState('zote');
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    fetchStyles();
  }, []);

  const fetchStyles = async () => {
    try {
      const response = await stylesService.getAll();
      setStyles(response.data);
    } catch (err) {
      setError('Hitilafu ya kupakua mitindo');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Memoize filtered styles to avoid recalculation
  const filteredStyles = useMemo(() => {
    return filter === 'zote' 
      ? styles 
      : styles.filter(style => style.gender === filter);
  }, [styles, filter]);

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Inapakia mitindo...</p>
      </div>
    );
  }

  return (
    <div className="styles-container">
      <div className="styles-header">
        <h1>Mitindo ya Nguo</h1>
        <p>Chagua mtindo unaopenda kutoka orodha yetu</p>
      </div>

      <div className="styles-filters">
        <button 
          className={filter === 'zote' ? 'filter-btn active' : 'filter-btn'}
          onClick={() => setFilter('zote')}
        >
          Zote
        </button>
        <button 
          className={filter === 'kiume' ? 'filter-btn active' : 'filter-btn'}
          onClick={() => setFilter('kiume')}
        >
          Nguo za Kiume
        </button>
        <button 
          className={filter === 'kike' ? 'filter-btn active' : 'filter-btn'}
          onClick={() => setFilter('kike')}
        >
          Nguo za Kike
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {filteredStyles.length === 0 ? (
        <div className="no-styles">
          <p>Hakuna mitindo ya {filter === 'zote' ? 'sasa hivi' : filter}</p>
        </div>
      ) : (
        <div className="styles-grid">
          {filteredStyles.map((style) => (
            <div key={style.id} className="style-card">
              <div className="style-image">
                <img 
                  src={`http://localhost:8000${style.image}`} 
                  alt={style.name}
                  loading="lazy"
                  onError={(e) => {
                    e.target.src = 'https://via.placeholder.com/300x400?text=Hakuna+Picha';
                  }}
                />
              </div>
              <div className="style-info">
                <h3>{style.name}</h3>
                <p className="style-description">{style.description}</p>
                <div className="style-meta">
                  <span className="style-category">{style.category}</span>
                  <span className="style-gender">
                    {style.gender === 'kiume' ? '👔 Kiume' : 
                     style.gender === 'kike' ? '👗 Kike' : '👔👗 Zote'}
                  </span>
                </div>
                <div className="style-footer">
                  <span className="style-price">
                    TSh {parseInt(style.price).toLocaleString()}
                  </span>
                  {isAuthenticated && (
                    <button className="btn-order">
                      Oda Sasa
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Styles;
