const Detail = () => {
  function initDonutChart() {
    function createCanvasElement(size) {
      const canvas = document.createElement('canvas');
      canvas.width = canvas.height = size;
      return canvas;
    }

    function drawArc(ctx, color, lineWidth, percentage, radius) {
      ctx.beginPath();
      ctx.arc(0, 0, radius, 0, 2 * Math.PI * percentage, false);
      ctx.strokeStyle = color;
      ctx.lineCap = 'round';
      ctx.lineWidth = lineWidth;
      ctx.stroke();
    }

    const chartElement = document.getElementById('tcc_donut_chart');

    if (chartElement) {
      const config = {
        size: parseInt(chartElement.getAttribute('data-kt-size')) || 70,
        lineWidth: parseInt(chartElement.getAttribute('data-kt-line')) || 11,
        rotate: parseInt(chartElement.getAttribute('data-kt-rotate')) || 145,
      };

      const canvas = createCanvasElement(config.size);
      const spanElement = document.createElement('span');

      if (typeof G_vmlCanvasManager !== 'undefined') {
        G_vmlCanvasManager.initElement(canvas);
      }

      const ctx = canvas.getContext('2d');
      canvas.width = canvas.height = config.size;
      chartElement.appendChild(spanElement);
      chartElement.appendChild(canvas);
      ctx.translate(config.size / 2, config.size / 2);
      ctx.rotate((config.rotate / 180 - 0.5) * Math.PI);

      const radius = (config.size - config.lineWidth) / 2;

      const regular = Number($('#tcc_regular_score').data('regular-score'));
      const great = Number($('#tcc_great_score').data('great-score'));
      const terrible = Number($('#tcc_terrible_score').data('terrible-score'));
      const allScores = regular + great + terrible;

      drawArc(ctx, '#E4E6EF', config.lineWidth, 1, radius);

      if (((great + terrible) / allScores) > 0) {
        drawArc(ctx, KTUtil.getCssVariableValue('--bs-success'), config.lineWidth, (great + terrible) / allScores, radius);
      }

      if ((terrible / allScores) > 0) {
        drawArc(ctx, KTUtil.getCssVariableValue('--bs-danger'), config.lineWidth, terrible / allScores, radius);
      }
    }
  }

  initDonutChart();
}

KTUtil.onDOMContentLoaded(function() {
  Detail();
});
