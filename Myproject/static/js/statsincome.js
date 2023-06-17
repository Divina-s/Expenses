
const renderChartIncome=(data, labels) =>{
    const ctx = document.getElementById('myChartincome');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Last six months Income',
          data: data,
          borderWidth: 1
        }]
      },
      options: {
        title:{
          display:true,
          text:'Income per Source'
        }
      }
    });
}
const getChartDataIncome=()=>{
      console.log('fetching');
    fetch('income_source_summary').then(res=>res.json()).then(results=>{
        console.log('results',results);
        const source_data=results.income_source_data;
        const[ labels,data]=[Object.keys(source_data),Object.values(source_data)
        ];


        renderChartIncome(data, labels);
    }
        )
}
document.onload=getChartDataIncome();