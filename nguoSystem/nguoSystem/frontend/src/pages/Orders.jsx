import { useState, useEffect } from 'react';
import { ordersService } from '../services/api';
import './Orders.css';

const Orders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      const response = await ordersService.getMyOrders();
      setOrders(response.data);
    } catch (err) {
      setError('Hitilafu ya kupakua oda');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      PENDING: '#f39c12',
      APPROVED: '#3498db',
      IN_PROGRESS: '#9b59b6',
      COMPLETED: '#27ae60',
      DELIVERED: '#16a085',
      REJECTED: '#e74c3c',
      CANCELLED: '#95a5a6',
    };
    return colors[status] || '#95a5a6';
  };

  const getStatusText = (status) => {
    const texts = {
      PENDING: 'Inasubiri',
      APPROVED: 'Imekubaliwa',
      IN_PROGRESS: 'Inaendelea',
      COMPLETED: 'Imemaliza',
      DELIVERED: 'Imetumwa',
      REJECTED: 'Imekataliwa',
      CANCELLED: 'Imesitishwa',
    };
    return texts[status] || status;
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Inapakia oda...</p>
      </div>
    );
  }

  return (
    <div className="orders-container">
      <div className="orders-header">
        <h1>Oda Zangu</h1>
        <p>Angalia hali ya oda zako zote</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      {orders.length === 0 ? (
        <div className="no-orders">
          <p>Huna oda yoyote bado</p>
          <a href="/styles" className="btn-primary">
            Angalia Mitindo
          </a>
        </div>
      ) : (
        <div className="orders-list">
          {orders.map((order) => (
            <div key={order.id} className="order-card">
              <div className="order-header">
                <h3>Oda #{order.id}</h3>
                <span 
                  className="order-status"
                  style={{ backgroundColor: getStatusColor(order.status) }}
                >
                  {getStatusText(order.status)}
                </span>
              </div>
              
              <div className="order-details">
                {order.style && (
                  <div className="order-info">
                    <strong>Mtindo:</strong> {order.style_name || order.style}
                  </div>
                )}
                <div className="order-info">
                  <strong>Saizi:</strong> {order.size}
                </div>
                <div className="order-info">
                  <strong>Idadi:</strong> {order.quantity}
                </div>
                {order.total_price && (
                  <div className="order-info">
                    <strong>Bei:</strong> TSh {parseInt(order.total_price).toLocaleString()}
                  </div>
                )}
                {order.delivery_date && (
                  <div className="order-info">
                    <strong>Tarehe ya Kupokea:</strong> {new Date(order.delivery_date).toLocaleDateString('sw-TZ')}
                  </div>
                )}
              </div>

              {order.custom_style && (
                <div className="order-custom">
                  <strong>Maelezo ya Mtindo Maalum:</strong>
                  <p>{order.custom_style}</p>
                </div>
              )}

              <div className="order-footer">
                <span className="order-date">
                  Tarehe: {new Date(order.created_at).toLocaleDateString('sw-TZ')}
                </span>
                {order.status === 'PENDING' && order.can_delete && (
                  <button className="btn-delete">
                    Futa Oda
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Orders;
