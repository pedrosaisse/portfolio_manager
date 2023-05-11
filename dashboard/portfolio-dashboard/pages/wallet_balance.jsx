import React from "react";
import { useState, useEffect } from 'react';

const WalletBalance = () => {
    const [data, setData] = useState([]);
    const [url, setUrl] = useState('');
    
    useEffect(() => {
        async function fetchData() {
            const res = await fetch(url);
            const json = await res.json();
            setData(json);
        }
        fetchData();
    }, [url]);

    const formatNumber = (number) => {
        return new Intl.NumberFormat('en-US').format(number);
    };

    return (
        <>
            <div>
                <h1>Current Balance - Wallet</h1>
                <button onClick={() => setUrl('http://localhost:9050/current_position?class_id=1&country_id=1&wallet_id=1')}>
                BRL Stocks
                </button>
                <button onClick={() => setUrl('http://localhost:9050/current_position?class_id=2&country_id=1&wallet_id=2')}>
                BRL Reits
                </button>
                <button onClick={() => setUrl('http://localhost:9050/current_position?class_id=1&country_id=2&wallet_id=3')}>
                USD Stocks
                </button>
                <button onClick={() => setUrl('http://localhost:9050/current_position?class_id=1&country_id=2&wallet_id=4')}>
                USD Stocks Motley Fool Report
                </button>
                <button onClick={() => setUrl('http://localhost:9050/current_position?class_id=4&country_id=2&wallet_id=5')}>
                USD ETFs
                </button>
                <button onClick={() => setUrl('http://localhost:9050/current_position?class_id=3&country_id=2&wallet_id=6')}>
                USD Reits
                </button>
                <table style={{ borderCollapse: 'collapse', border: '2px solid black' }}>
                <thead>
                    <tr>
                    <th style={{ border: '1px solid black', padding: '10px' }}>Company</th>
                    <th style={{ border: '1px solid black', padding: '10px' }}>Ticker</th>
                    <th style={{ border: '1px solid black', padding: '10px' }}>Date/Time</th>
                    <th style={{ border: '1px solid black', padding: '10px' }}>Close Price</th>
                    <th style={{ border: '1px solid black', padding: '10px' }}>Balance</th>
                    <th style={{ border: '1px solid black', padding: '10px' }}>Size</th>
                    <th style={{ border: '1px solid black', padding: '10px' }}>Desired Size %</th>
                    <th style={{ border: '1px solid black', padding: '10px' }}>Desired Size Value</th>
                    <th style={{ border: '1px solid black', padding: '10px' }}>Desired Size Qtt</th>
                    <th style={{ border: '1px solid black', padding: '10px' }}>Average Price</th>
                    <th style={{ border: '1px solid black', padding: '10px' }}>average_cost</th>
                    <th style={{ border: '1px solid black', padding: '10px' }}>PnL</th>
                    <th style={{ border: '1px solid black', padding: '10px' }}>PnL %</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((item) => (
                    <tr>
                        <td style={{ border: '1px solid black', padding: '10px' }}>{item.company}</td>
                        <td style={{ border: '1px solid black', padding: '10px' }}>{item.ticker}</td>
                        <td style={{ border: '1px solid black', padding: '10px' }}>{item.read_date}</td>
                        <td style={{ border: '1px solid black', padding: '10px' }}>{formatNumber(item.close_price)}</td>
                        <td style={{ border: '1px solid black', padding: '10px' }}>{formatNumber(item.balance)}</td>
                        <td style={{ border: '1px solid black', padding: '10px' }}>{formatNumber(item.size)}</td>
                        <td style={{ border: '1px solid black', padding: '10px' }}>{formatNumber(item.desired_position_pct)}</td>
                        <td style={{ border: '1px solid black', padding: '10px' }}>{formatNumber(item.desired_position_value)}</td>
                        <td style={{ border: '1px solid black', padding: '10px' }}>{formatNumber(item.desired_position_qtt)}</td>
                        <td style={{ border: '1px solid black', padding: '10px' }}>{formatNumber(item.average_price)}</td>
                        <td style={{ border: '1px solid black', padding: '10px' }}>{formatNumber(item.average_cost)}</td>
                        <td style={{ border: '1px solid black', padding: '10px' }}>{formatNumber(item.pnl)}</td>
                        <td style={{ border: '1px solid black', padding: '10px' }}>{formatNumber(item.pnl_pct)}</td>
                    </tr>
                    ))}
                </tbody>
                </table>
            </div>
        </>
    );
  }
  
export default WalletBalance;
