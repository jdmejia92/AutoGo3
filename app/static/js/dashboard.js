
document.addEventListener('DOMContentLoaded', function() {
    // Configuración común para los mini gráficos de tendencia
const miniChartConfig = {
  type: 'line',
  options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
          legend: {
              display: false
          },
          tooltip: {
              enabled: false
          }
      },
      scales: {
          x: {
              display: false
          },
          y: {
              display: false
          }
      },
      elements: {
          point: {
              radius: 0
          },
          line: {
              borderWidth: 2,
              tension: 0.4
          }
      }
  }
};

// Función para crear datos de ejemplo (reemplazar con datos reales)
const generateMockData = (count, min, max) => {
  return Array.from({length: count}, () => 
      Math.floor(Math.random() * (max - min + 1)) + min
  );
};

document.addEventListener('DOMContentLoaded', function() {
  // ------ PESTAÑA GENERAL ------
  
  // Mini gráficos de tendencia en KPIs
  new Chart('generalFleetTrend', {
      ...miniChartConfig,
      data: {
          labels: Array(12).fill(''),
          datasets: [{
              data: generateMockData(12, 30, 50),
              borderColor: '#0d6efd',
              fill: false
          }]
      }
  });

  new Chart('generalIncomeTrend', {
      ...miniChartConfig,
      data: {
          labels: Array(12).fill(''),
          datasets: [{
              data: generateMockData(12, 5000, 8000),
              borderColor: '#198754',
              fill: false
          }]
      }
  });

  new Chart('generalReservationsTrend', {
      ...miniChartConfig,
      data: {
          labels: Array(12).fill(''),
          datasets: [{
              data: generateMockData(12, 20, 40),
              borderColor: '#ffc107',
              fill: false
          }]
      }
  });

  new Chart('generalAvailabilityTrend', {
      ...miniChartConfig,
      data: {
          labels: Array(12).fill(''),
          datasets: [{
              data: generateMockData(12, 60, 90),
              borderColor: '#0dcaf0',
              fill: false
          }]
      }
  });

  // Gráfico principal de ingresos
  new Chart('generalIncomeChart', {
      type: 'bar',
      data: {
          labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
          datasets: [{
              label: 'Ingresos',
              data: generateMockData(12, 10000, 20000),
              backgroundColor: '#0d6efd80',
              borderColor: '#0d6efd',
              borderWidth: 1
          }]
      },
      options: {
          responsive: true,
          plugins: {
              legend: {
                  position: 'top',
              },
              title: {
                  display: false
              }
          }
      }
  });

  // Gráfico de distribución de flota
  new Chart('generalFleetDistribution', {
      type: 'doughnut',
      data: {
          labels: ['Económicos', 'Intermedios', 'Premium', 'Lujo'],
          datasets: [{
              data: [30, 25, 25, 20],
              backgroundColor: [
                  '#0d6efd80',
                  '#19875480',
                  '#ffc10780',
                  '#dc354580'
              ]
          }]
      },
      options: {
          responsive: true,
          plugins: {
              legend: {
                  position: 'bottom'
              }
          }
      }
  });

  // ------ PESTAÑA AUTOS ------
  
  // Gráfico de uso por categoría
  new Chart('carUsageChart', {
      type: 'bar',
      data: {
          labels: ['Económicos', 'Intermedios', 'Premium', 'Lujo'],
          datasets: [{
              label: 'En Uso',
              data: generateMockData(4, 10, 20),
              backgroundColor: '#0d6efd80'
          }, {
              label: 'Disponibles',
              data: generateMockData(4, 5, 15),
              backgroundColor: '#19875480'
          }]
      },
      options: {
          responsive: true,
          plugins: {
              legend: {
                  position: 'top'
              }
          },
          scales: {
              x: {
                  stacked: true
              },
              y: {
                  stacked: true
              }
          }
      }
  });

  // Gráfico de estado de mantenimiento
  new Chart('maintenanceStatusChart', {
      type: 'pie',
      data: {
          labels: ['Al Día', 'Próximo', 'Atrasado', 'En Mantenimiento'],
          datasets: [{
              data: [60, 20, 10, 10],
              backgroundColor: [
                  '#19875480',
                  '#ffc10780',
                  '#dc354580',
                  '#0d6efd80'
              ]
          }]
      },
      options: {
          responsive: true,
          plugins: {
              legend: {
                  position: 'bottom'
              }
          }
      }
  });

  // ------ PESTAÑA RESERVAS ------
  
  // Mini gráficos de tendencia
  const reservationsMiniCharts = [
      'reservationsTrendMini',
      'occupationTrendMini',
      'durationTrendMini',
      'cancellationTrendMini'
  ];

  reservationsMiniCharts.forEach(chartId => {
      new Chart(chartId, {
          ...miniChartConfig,
          data: {
              labels: Array(12).fill(''),
              datasets: [{
                  data: generateMockData(12, 20, 80),
                  borderColor: '#0d6efd',
                  fill: false
              }]
          }
      });
  });

  // Gráfico de tendencia de reservas
  new Chart('reservationTrendChart', {
      type: 'line',
      data: {
          labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
          datasets: [{
              label: 'Reservas',
              data: generateMockData(12, 50, 100),
              borderColor: '#0d6efd',
              tension: 0.4,
              fill: false
          }]
      },
      options: {
          responsive: true,
          plugins: {
              legend: {
                  position: 'top'
              }
          }
      }
  });

  // Gráfico de distribución por duración
  new Chart('durationDistributionChart', {
      type: 'pie',
      data: {
          labels: ['1-3 días', '4-7 días', '8-14 días', '15+ días'],
          datasets: [{
              data: [40, 30, 20, 10],
              backgroundColor: [
                  '#0d6efd80',
                  '#19875480',
                  '#ffc10780',
                  '#dc354580'
              ]
          }]
      },
      options: {
          responsive: true,
          plugins: {
              legend: {
                  position: 'bottom'
              }
          }
      }
  });

  // ------ PESTAÑA INGRESOS ------
  
  // Mini gráficos de tendencia
  const incomeMiniCharts = [
      'incomeTrendMini',
      'incomePerCarTrendMini',
      'marginTrendMini',
      'roiTrendMini'
  ];

  incomeMiniCharts.forEach(chartId => {
      new Chart(chartId, {
          ...miniChartConfig,
          data: {
              labels: Array(12).fill(''),
              datasets: [{
                  data: generateMockData(12, 1000, 5000),
                  borderColor: '#198754',
                  fill: false
              }]
          }
      });
  });

  // Gráfico de evolución de ingresos
  new Chart('incomeEvolutionChart', {
      type: 'line',
      data: {
          labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
          datasets: [{
              label: 'Ingresos',
              data: generateMockData(12, 10000, 20000),
              borderColor: '#198754',
              backgroundColor: '#19875420',
              fill: true,
              tension: 0.4
          }]
      },
      options: {
          responsive: true,
          plugins: {
              legend: {
                  position: 'top'
              }
          },
          scales: {
              y: {
                  beginAtZero: true
              }
          }
      }
  });

  // Gráfico de distribución por categoría
  new Chart('incomeCategoryDistribution', {
      type: 'doughnut',
      data: {
          labels: ['Económicos', 'Intermedios', 'Premium', 'Lujo'],
          datasets: [{
              data: [25, 30, 25, 20],
              backgroundColor: [
                  '#0d6efd80',
                  '#19875480',
                  '#ffc10780',
                  '#dc354580'
              ]
          }]
      },
      options: {
          responsive: true,
          plugins: {
              legend: {
                  position: 'bottom'
              }
          }
      }
  });

  // Inicializar los mini gráficos de tendencia en la tabla de resumen
  document.querySelectorAll('[id^="trend-"]').forEach(canvas => {
      new Chart(canvas, {
          ...miniChartConfig,
          data: {
              labels: Array(6).fill(''),
              datasets: [{
                  data: generateMockData(6, 20, 80),
                  borderColor: '#0d6efd',
                  fill: false
              }]
          }
      });
  });
});
});
