// <div class="row flex">
//     <div class="col-sm-12 col-lg-6">
//         <canvas id="orderChart" data-today-order="{{ today.recent_orders_count.order_id__count }}" data-today-total="{% if today.recent_orders_total.total__sum %}{{ today.recent_orders_total.total__sum }}{% else %}0{% endif %}" data-week-order="{{ this_week.recent_orders_count.order_id__count }}" data-week-total="{% if this_week.recent_orders_total.total__sum %}{{ this_week.recent_orders_total.total__sum }}{% else %}0{% endif %}" data-lastFourWeek-order="{{ last_four_week.recent_orders_count.order_id__count }}" data-lastFourWeek-total="{% if last_four_week.recent_orders_total.total__sum %}{{ last_four_week.recent_orders_total.total__sum }}{% else %}0{% endif %}"></canvas>
//         <canvas id="totalAmountChart"></canvas>
//     </div>
// </div>
var ctx = document.getElementById('orderChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Today', 'This Week', 'Last Four Week'],
        datasets: [{
            label: 'Today Order',
            data: [12, 19, 3],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});