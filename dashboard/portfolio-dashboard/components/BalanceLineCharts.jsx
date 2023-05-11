import React from 'react';
import moment from 'moment';
import { useState, useEffect } from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
  } from 'chart.js';
import { Line } from 'react-chartjs-2';
  
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
  );

const BalanceLineChart = () => {
    const [data, setData] = useState([]);
    const [url, setUrl] = useState('');
  
    useEffect(() => {
      async function fetchData() {
        const res = await fetch('http://localhost:9050/dividends?country_id=1&class_id=2');
        const json = await res.json();
        setData(json);
      }
      fetchData();
    }, []);

    const chartData = {
        labels: data.map((item) => item.date_payment),
        datasets:[
            {
                label: 'Amount',
                data: data.map((item) => item.payment),
                borderColor: 'rgba(255, 99, 132, 1)',
                fill: false
            }
        ],       
    };
    return (
        <>
            <div className='w-full md:col-span-2 relative lg:h-[70vh] h-[50vh] m-auto p-4 border rounded-lg bg-white'>
                <Line data={chartData}/>
            </div>
        </>
        
    )
}

export default BalanceLineChart