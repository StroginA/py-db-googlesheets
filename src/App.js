import './App.css';
import axios from 'axios';
import React from 'react';

class App extends React.Component {
  state = {
    orders: []
  }
  componentDidMount = () => {
    axios.get('http://localhost:8000/api/orders')
    .then(res => {
      console.log(res)
      this.setState({orders: res.data})
    })
  }
  render() {
    return (
      <div className="App">
        <table>
        <thead>
          <tr>
            <th>Номер заказа</th>
            <th>Стоимость, $</th>
            <th>Стоимость, руб</th>
            <th>Срок поставки</th>
          </tr>
        </thead>
        <tbody>
          {this.state.orders.map(order => (
              <tr key={order.orderId}>
                <td>{order.orderId}</td>
                <td>{order.costUSD}</td>
                <td>{order.costRUB}</td>
                <td>{order.deliveryDate}</td>
              </tr>
            ))
          }
        </tbody>
        </table>
      </div>
    )
  }
}

export default App;
