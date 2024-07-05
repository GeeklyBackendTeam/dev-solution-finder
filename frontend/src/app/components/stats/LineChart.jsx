"use client";

import React from 'react';
import { ResponsiveLine } from '@nivo/line';

const LineChart = () => {
    const data = [
        {
            id: "Desktop",
            data: [
                { x: "Jan", y: 43 },
                { x: "Feb", y: 137 },
                { x: "Mar", y: 61 },
                { x: "Apr", y: 145 },
                { x: "May", y: 26 },
                { x: "Jun", y: 154 },
            ],
        },
        {
            id: "Mobile",
            data: [
                { x: "Jan", y: 60 },
                { x: "Feb", y: 48 },
                { x: "Mar", y: 177 },
                { x: "Apr", y: 78 },
                { x: "May", y: 96 },
                { x: "Jun", y: 204 },
            ],
        },
    ];

    return (
        <div className="w-[600px] h-[400px]">
            <ResponsiveLine
                data={data}
                margin={{ top: 10, right: 10, bottom: 40, left: 40 }}
                xScale={{ type: 'point' }}
                yScale={{ type: 'linear', stacked: true, min: 'auto', max: 'auto' }}
                axisTop={null}
                axisRight={null}
                axisBottom={{
                    tickSize: 0,
                    tickPadding: 16,
                    legend: 'Month',
                    legendPosition: 'middle',
                    legendOffset: 32,
                }}
                axisLeft={{
                    tickSize: 0,
                    tickPadding: 16,
                    legend: 'Value',
                    legendPosition: 'middle',
                    legendOffset: -40,
                }}
                colors={['#2563eb', '#e11d48']}
                pointSize={6}
                pointColor={{ theme: 'background' }}
                pointBorderWidth={2}
                pointBorderColor={{ from: 'serieColor' }}
                pointLabelYOffset={-12}
                useMesh={true}
                gridYValues={6}
                theme={{
                    tooltip: {
                        container: {
                            background: '#333',
                            color: '#ddd',
                            fontSize: '12px',
                            borderRadius: '4px',
                            boxShadow: '0 1px 2px rgba(0, 0, 0, 0.25)',
                            padding: '5px 9px',
                        },
                    },
                    grid: {
                        line: {
                            stroke: '#e0e0e0',
                            strokeWidth: 1,
                        },
                    },
                }}
                legends={[
                    {
                        anchor: 'bottom-right',
                        direction: 'column',
                        justify: false,
                        translateX: 100,
                        translateY: 0,
                        itemsSpacing: 0,
                        itemDirection: 'left-to-right',
                        itemWidth: 80,
                        itemHeight: 20,
                        itemOpacity: 0.75,
                        symbolSize: 12,
                        symbolShape: 'circle',
                        symbolBorderColor: 'rgba(0, 0, 0, .5)',
                        effects: [
                            {
                                on: 'hover',
                                style: {
                                    itemBackground: 'rgba(0, 0, 0, .03)',
                                    itemOpacity: 1,
                                },
                            },
                        ],
                    },
                ]}
                role="application"
                ariaLabel="Nivo line chart demo"
                curve="natural"
            />
        </div>
    );
};

export default LineChart;
