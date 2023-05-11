import Head from 'next/head';


import Header from '../components/Header';
import TopCards from '../components/TopCards';
import BalanceLineChart from '../components/BalanceLineCharts';


export default function Home() {
  return (
    <>
      <Head>
        <title>Asset Allocation</title>
        <meta name="description" content="osjgogjg" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className='bg-gray-100 min-h-screen'>
        <Header />
        <TopCards />
        <BalanceLineChart />
      </main>
    </>
  );
}
