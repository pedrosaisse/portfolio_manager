import React from "react";

const TopCards = () => {
    return (
        <>
            <div className="grid lg:grid-cols-5 gap-4 p-4">
                <div className="lg:col-span-2 col-span-1 bg-white flex justify-between w-full border p-4 rounded-lg">
                    <div className="flex flex-col w-full pb-4">
                        <p className="text-2xl font-bold">R$ 11111</p>
                        <p className="text-gray-600">Stocks</p>
                    </div>
                </div>
                <div className="lg:col-span-2 col-span-1 bg-white flex justify-between w-full border p-4 rounded-lg">
                    <div className="flex flex-col w-full pb-4">
                        <p className="text-2xl font-bold">R$ 11111</p>
                        <p className="text-gray-600">Reits</p>
                    </div>
                </div>
                <div className="bg-white flex justify-between w-full border p-4 rounded-lg">
                    <div className="flex flex-col w-full pb-4">
                        <p className="text-2xl font-bold">R$ 11111</p>
                        <p className="text-gray-6y00">Total</p>
                    </div>
                </div>
            </div>
            <div className="grid lg:grid-cols-7 gap-4 p-4">
            <div className="lg:col-span-2 col-span-1 bg-white flex justify-between w-full border p-4 rounded-lg">
                <div className="flex flex-col w-full pb-4">
                    <p className="text-2xl font-bold">U$ 11111</p>
                    <p className="text-gray-600">Stocks</p>
                </div>
            </div>
            <div className="lg:col-span-2 col-span-1 bg-white flex justify-between w-full border p-4 rounded-lg">
                <div className="flex flex-col w-full pb-4">
                    <p className="text-2xl font-bold">U$ 11111</p>
                    <p className="text-gray-600">ETFs</p>
                </div>
            </div>
            <div className="lg:col-span-2 col-span-1 bg-white flex justify-between w-full border p-4 rounded-lg">
                <div className="flex flex-col w-full pb-4">
                    <p className="text-2xl font-bold">U$ 11111</p>
                    <p className="text-gray-600">Reits</p>
                </div>
            </div>
            <div className="bg-white flex justify-between w-full border p-4 rounded-lg">
                <div className="flex flex-col w-full pb-4">
                    <p className="text-2xl font-bold">U$ 11111</p>
                    <p className="text-gray-6y00">Total</p>
                </div>
            </div>
        </div>
    </>
    )
}

export default TopCards