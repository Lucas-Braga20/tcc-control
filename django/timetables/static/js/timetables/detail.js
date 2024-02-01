const Detail = () => {
  const API = {
    notifications: {
      send(receivers, message) {
        return fetch(`/tcc/api/notifications/send-notification/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
          body: JSON.stringify({
            receivers,
            message,
          }),
        });
      },
    },
  };

  function addErrorInField(error, id) {
    $(id).addClass('is-invalid');
    if (Array.isArray(error)) {
      error.forEach(err => {
        $(id).parent().append(`
          <div class="invalid-feedback">
            ${err}
          </div>
        `);
      });
    } else {
      $(id).parent().append(`
        <div class="invalid-feedback">
          ${error}
        </div>
      `);
    }
  }

  function removeErrorInField(id) {
    $(id).removeClass('is-invalid');
    $(id).parent().find('.invalid-feedback').remove();
  }

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

  function handleSendWarning() {
    function handleMaxLengthBadge() {
      $('#tcc_message').maxlength({
        warningClass: "badge badge-warning z-index-2000",
        limitReachedClass: "badge badge-success z-index-2000",
      });
    }

    function handleFormValidator() {
      $('#tcc_send_warning_form').validate({
        errorElement: 'div',
        errorClass: 'invalid-feedback',
        highlight: function(element) {
          $(element).addClass('is-invalid');
        },
        unhighlight: function(element) {
          $(element).removeClass('is-invalid');
        },
        rules: {
          receivers: {
            required: true,
          },
          message: {
            required: true,
            minlength: 3,
            maxlength: 255,
          },
        },
        messages: {
          receivers: {
            required: 'Os destinatários devem ser inseridos.',
          },
          message: {
            required: 'A mensagem deve ser inserida.',
            minlength: 'A mensagem deve ter pelo menos 3 caracteres.',
            maxlength: 'A mensagem não pode ter mais de 255 caracteres.',
          },
        },
        errorPlacement(error, element) {
          element.parent().append(error);
        },
      });

      $('#tcc_message').keyup(function(e) {
        $(this).valid();
      });

      $('#tcc_receivers').on('select2:select', function(e) {
        $(this).valid();
      });
      $('#tcc_receivers').on('select2:unselect', function(e) {
        $(this).valid();
      });
    }

    function handleFormSubmit() {
      function addLoading() {
        $('#tcc_receivers').addClass('disabled');
        $('#tcc_receivers').attr('disabled', true);

        $('#tcc_message').addClass('disabled');
        $('#tcc_message').attr('disabled', true);

        $('#tcc_send_warning_cancel').addClass('disabled');
        $('#tcc_send_warning_cancel').attr('disabled', true);
        $('#tcc_send_warning_cancel').html(`
          <div class="spinner-border spinner-border-sm text-gray-700 me-2" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          Cancelar
        `);

        $('#tcc_send_warning_confirm').addClass('disabled');
        $('#tcc_send_warning_confirm').attr('disabled', true);
        $('#tcc_send_warning_confirm').html(`
          <div class="spinner-border spinner-border-sm text-white me-2" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          Confirmar
        `);

        $('#tcc_modal_send_warning_close').addClass('disabled');
        $('#tcc_modal_send_warning_close').attr('disabled', true);
      }

      function removeLoading() {
        $('#tcc_receivers').removeClass('disabled');
        $('#tcc_receivers').removeAttr('disabled');

        $('#tcc_message').removeClass('disabled');
        $('#tcc_message').removeAttr('disabled');

        $('#tcc_send_warning_cancel').removeClass('disabled');
        $('#tcc_send_warning_cancel').removeAttr('disabled');
        $('#tcc_send_warning_cancel').html(`
          Cancelar
        `);

        $('#tcc_send_warning_confirm').removeClass('disabled');
        $('#tcc_send_warning_confirm').removeAttr('disabled');
        $('#tcc_send_warning_confirm').html(`
          Confirmar
        `);

        $('#tcc_modal_send_warning_close').removeClass('disabled');
        $('#tcc_modal_send_warning_close').removeAttr('disabled');
      }

      $('#tcc_send_warning_form').submit(function (e) {
        e.preventDefault();

        const isValid = $(this).valid();

        if (!isValid) {
          return;
        }

        let fetchResponse = null;

        removeErrorInField('#tcc_receivers');
        removeErrorInField('#tcc_message');

        $('#tcc_send_warning_info').removeClass('d-none');
        $('#tcc_send_warning_error').addClass('d-none');
        $('#tcc_send_warning_error_message').text('');

        addLoading();

        API.notifications.send(
          $('#tcc_receivers').val(),
          $('#tcc_message').val(),
        )
          .then(response => {
            fetchResponse = response;

            return response.json();
          })
          .then(response => {
            if (fetchResponse.ok === false) {
              if (response.receivers != null) {
                addErrorInField(response.receivers, '#tcc_receivers');
              }

              if (response.message != null) {
                addErrorInField(response.message, '#tcc_message');
              }

              if (response.detail != null) {
                $('#tcc_send_warning_info').addClass('d-none');
                $('#tcc_send_warning_error').removeClass('d-none');
                $('#tcc_send_warning_error_message').text(response.detail);
              }
            } else {
              Toast.fire({
                icon: 'success',
                title: 'Mensagem enviada com successo.'
              });

              modal.hide();
            }
          })
          .catch(() => {
            $('#tcc_send_warning_info').addClass('d-none');
            $('#tcc_send_warning_error').removeClass('d-none');
            $('#tcc_send_warning_error_message').text('Houve um erro no servidor. Tente novamente.');
          })
          .finally(() => {
            removeLoading();
          });
      });
    }

    let modal = new bootstrap.Modal($('#tcc_modal_send_warning'));

    $('#tcc_send_warning').click(function (e) {
      modal.show();
    });

    $('#tcc_receivers').select2({
      ajax: {
        url: '/tcc/api/users/',
        dataType: 'json',
        data: function ({ term }, page) {
          return {
            search: term,
            timetable: $('#tcc_modal_send_warning').data('timetable'),
          };
        },
        processResults: function (data) {
          return {
            results: data.results.map(user => {
              return {
                id: user.id,
                text: user.full_name,
              };
            }),
          };
        },
        cache: true,
      },
      closeOnSelect: false,
      placeholder: 'Selecione os destinatários.',
      dropdownParent: $('#tcc_modal_send_warning'),
      multiple: true,
    });

    handleMaxLengthBadge();
    handleFormValidator();
    handleFormSubmit();
  }

  initDonutChart();
  handleSendWarning();
}

KTUtil.onDOMContentLoaded(function() {
  Detail();
});
