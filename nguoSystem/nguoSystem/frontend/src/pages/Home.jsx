import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Home.css';

const Home = () => {
  const { user, isAuthenticated } = useAuth();

  return (
    <div className="home-container">
      <section className="hero">
        <div className="hero-content">
          <h1>Karibu kwenye Nguo System 🧵</h1>
          <p className="hero-subtitle">
            Mfumo wa kisasa wa kushona nguo kwa njia ya mtandao
          </p>
          
          {isAuthenticated ? (
            <div className="hero-welcome">
              <h2>Karibu tena, {user?.full_name || user?.email}!</h2>
              <div className="hero-actions">
                <Link to="/styles" className="btn-hero">
                  Angalia Mitindo
                </Link>
                <Link to="/orders" className="btn-hero-outline">
                  Oda Zangu
                </Link>
              </div>
            </div>
          ) : (
            <div className="hero-actions">
              <Link to="/register" className="btn-hero">
                Anza Sasa
              </Link>
              <Link to="/login" className="btn-hero-outline">
                Ingia
              </Link>
            </div>
          )}
        </div>
      </section>

      <section className="features">
        <h2>Huduma Zetu</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">👔</div>
            <h3>Mitindo Mbalimbali</h3>
            <p>Chagua kutoka mitindo mingi ya nguo za kiume na kike</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">📐</div>
            <h3>Vipimo Maalum</h3>
            <p>Oda nguo kwa vipimo vyako maalum</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">🎨</div>
            <h3>Mitindo Maalum</h3>
            <p>Omba mtindo wa kipekee kutoka kwa washonaji wetu</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">🚚</div>
            <h3>Utoaji Haraka</h3>
            <p>Pokea nguo zako kwa wakati unaopendwa</p>
          </div>
        </div>
      </section>

      <section className="about">
        <h2>Kuhusu Sisi</h2>
        <p>
          Nguo System ni jukwaa la mtandao linalounganisha wateja na washonaji 
          mahiri. Tunawezesha watu kupata nguo za ubora wa hali ya juu kwa bei nafuu.
        </p>
        <p>
          Washonaji wetu ni wataalam wenye uzoefu wa miaka mingi katika ushonaji 
          wa aina mbalimbali za nguo.
        </p>
      </section>
    </div>
  );
};

export default Home;
