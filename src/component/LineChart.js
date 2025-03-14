import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

const LineChart = () => {
  const chartRef = useRef(null); 

  useEffect(() => {
    const myChart = echarts.init(chartRef.current);

    const option = {
      title: {
        text: 'Ultraviolet index',
      },
      tooltip: {
        trigger: 'axis',
      },
      xAxis: {
        type: 'category',
        data: ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'],
      },
      yAxis: {
        type: 'value',
      },
      series: [
        {
          name: 'UV',
          type: 'line',
          data: [0,1,1,1,1,3,5,6,8,9,10,11,11,11,10,9,8,6,4,3,4,3,2,1],
        },
      ],
    };

    myChart.setOption(option);

    return () => {
      myChart.dispose();
    };
  }, []);

  return <div ref={chartRef} style={{ width: '100%', height: '400px' }} />;
};

export default LineChart;