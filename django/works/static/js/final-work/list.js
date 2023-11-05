const FinalWorkList = () => {
  let dataTableElement = null;
  let dataTableObject = null;

  let completedButtonFilters = null;

  let searchInputElement = null;

  let completed = false;

  const badges = {
    0: `
      <span class="badge badge-light-dark">Atribuído</span>
    `,
    1: `
      <span class="badge badge-light-warning">Pendente</span>
    `,
    2: `
      <span class="badge badge-light-primary">Aguardando correção</span>
    `,
    3: `
      <span class="badge badge-light-info">Corrigido</span>
    `,
    4: `
      <span class="badge badge-light-danger">Entregue com atraso</span>
    `,
    5: `
      <span class="badge badge-light-success">Entregue</span>
    `,
    6: `
      <span class="badge badge-light-success">Apresentado</span>
    `,
  };

  const API = {
    works: {
      completed(id) {
        return fetch(`/api/final-works/${id}/`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
          body: JSON.stringify({
            completed: true
          }),
        });
      },

      details(id) {
        return fetch(`/api/final-works/${id}/`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
        });
      },

      update(id) {
        return fetch(`/api/final-works/${id}/`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
          body: JSON.stringify({
            supervisor: $('#tcc_participants_supervisor').val(),
            mentees: $('#tcc_participants_mentee').val(),
          }),
        });
      },
    },
  };


  function getElements() {
    dataTableElement = document.getElementById('tcc_datatable_users');
    searchInputElement = document.getElementById('tcc_datatable_search_input');
    completedButtonFilters = document.getElementById('tcc_completed_button_filters');
  }

  function initParticipantsModal() {
    new bootstrap.Modal($('#tcc_participants_modal'));
  }

  function handleSupervisorSelect(finalWorkId, initial) {
    $('#tcc_participants_supervisor').html('');
    $('#tcc_participants_supervisor').select2({
      minimumResultsForSearch: -1,
      placeholder: 'Selecione uma opção de orientador',
      allowClear: false,
      ajax: {
        url: `/api/final-works/${finalWorkId}/available-supervisors/`,
        dataType: 'json',
        processResults: function(data) {
          return {
            results: data.map(item => ({ id: item.id, text: item.full_name }))
          };
        },
        cache: true,
      },
    });

    $('#tcc_participants_supervisor')
      .append(new Option(
        initial.full_name,
        initial.id,
        true,
        true,
      ))
      .trigger('change');
  }

  function handleMenteeSelect(finalWorkId, initials) {
    $('#tcc_participants_mentee').html('');
    $('#tcc_participants_mentee').select2({
      minimumResultsForSearch: -1,
      placeholder: 'Selecione uma opção de orientando',
      allowClear: false,
      multiple: true,
      closeOnSelect: false,
      ajax: {
        url: `/api/final-works/${finalWorkId}/available-mentees/`,
        dataType: 'json',
        processResults: function(data) {
          return {
            results: data.map(item => ({ id: item.id, text: item.full_name }))
          };
        },
        cache: true,
      },
    });

    for (const initial of initials) {
      $('#tcc_participants_mentee')
        .append(new Option(
          initial.full_name,
          initial.id,
          true,
          true,
        ))
        .trigger('change');
    }
  }

  function handleParticipantsButtons() {
    $('.tcc_participants_action').click(function () {
      const modal = bootstrap.Modal.getInstance('#tcc_participants_modal');
      const id = $(this).data('id');

      $('#tcc_participants_modal').data('id', id);

      $('#tcc_participants_modal').find('#tcc_participants_loading').removeClass('d-none');
      $('#tcc_participants_modal').find('#tcc_participants_form_body').addClass('d-none');

      modal.show();

      API.works.details(id)
        .then(response => response.json())
        .then(response => {
          // Processa select de orientador.
          handleSupervisorSelect(response.id, response.supervisor_detail);

          // Processa select de orientandos.
          handleMenteeSelect(response.id, response.mentees_detail);

          initParticipantsFormValidator();

          $('#tcc_participants_modal').find('#tcc_participants_loading').addClass('d-none');
          $('#tcc_participants_modal').find('#tcc_participants_form_body').removeClass('d-none');
        })
        .catch(() => {
          Toast.fire({
            icon: 'error',
            title: 'Houve um erro no servidor.'
          });
        });
    });
  }

  function removeErrorInField(id) {
    $(id).removeClass('is-invalid');
    $(id).parent().find('.invalid-feedback').remove();
  }

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

  function initParticipantsFormValidator() {
    $('#tcc_participants_form').validate({
      errorElement: 'div',
      errorClass: 'invalid-feedback',
      highlight: function(element, errorClass, validClass) {
        $(element).addClass('is-invalid');
      },
      unhighlight: function(element, errorClass, validClass) {
        $(element).removeClass('is-invalid');
      },
      rules: {
        tcc_participants_supervisor: {
          required: true,
        },
        tcc_participants_mentee: {
          required: true,
        },
      },
      messages: {
        tcc_participants_supervisor: {
          required: 'O orientador deve ser selecionado.',
        },
        tcc_participants_mentee: {
          required: 'Os orientandos devem ser selecionados.',
        },
      },
      errorPlacement(error, element) {
        element.parent().append(error);
      },
    });

    $('#tcc_participants_supervisor').on('select2:select', function(e) {
      $(this).valid();
    });

    $('#tcc_participants_mentee').on('select2:select', function(e) {
      $(this).valid();
    });

    $('#tcc_participants_supervisor').on('select2:unselect', function(e) {
      $(this).valid();
    });

    $('#tcc_participants_supervisor').on('select2:select', function(e) {
      $(this).valid();
    });
  }

  function handleMenteesSelectElement() {
    $('#tcc_participants_mentee').on('select2:unselecting', e => {
      const currentUser = $('#tcc_participants_mentee').val();
    
      const userWillBeRemoved = e.params.args.data.id;
    
      if (currentUser === userWillBeRemoved) {
        e.preventDefault();
      }
    });
    
    $('#tcc_participants_mentee').on('select2:selecting', e => {
      const selectedItems = $('#tcc_participants_mentee').select2('val');
    
      if (selectedItems.length > 1) {
        e.preventDefault();
      }
    });
  }

  function handleUpdateParticipantsForm() {
    $('#tcc_participants_confirm_button').click(function (e) {
      if (!$('#tcc_participants_form').valid()) {
        e.preventDefault();

        return;
      }

      const finalWorkId = $('#tcc_participants_modal').data('id');

      let fetchResponse;

      $('#tcc_participants_modal .form-actions').addClass('disabled');
      $('#tcc_participants_modal .form-actions').html(`
        <div class="d-flex flex-row justify-content-center align-items-center">
          <div class="spinner-border spinner-border-sm text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>

          <span class="ms-1">
            Carregando...
          </span>
        </div>
      `);

      API.works.update(finalWorkId)
        .then(response => fetchResponse = response)
        .then(response => response.json())
        .then(data => {
          if (fetchResponse.status >= 300) {
            removeErrorInField('#tcc_participants_supervisor');
            removeErrorInField('#tcc_participants_mentee');

            if (data.supervisor) {
              addErrorInField(data.supervisor, '#tcc_participants_supervisor');
            }

            if (data.mentees) {
              addErrorInField(data.mentees, '#tcc_participants_mentee');
            }

            if (data.detail) {
              Toast.fire({
                icon: 'error',
                title: data.detail
              });
            }
          } else {
            bootstrap.Modal.getInstance('#tcc_participants_modal').hide();

            Toast.fire({
              icon: 'success',
              title: 'Participantes atualizados com sucesso.'
            });

            dataTableObject.ajax.reload();
            dataTableObject.draw();
          }
        })
        .catch(() => {
          Toast.fire({
            icon: 'error',
            title: 'Houve um erro no servidor. Tente novamente!'
          });
        })
        .finally(() => {
          $('#tcc_participants_modal .form-actions').removeClass('disabled');

          $('#tcc_participants_cancel_button').html('Fechar');
          $('#tcc_participants_confirm_button').html('Confirmar');
        });
    });
  }

  function handleCompleteButtons() {
    $('.tcc_complete_action').click(function () {
      const id = $(this).data('id');

      Swal.fire({
        title: 'Completar TCC',
        text: 'Tem certeza que deseja completar este TCC?',
        icon: 'warning',
        customClass: {
          actions: 'my-actions',
          cancelButton: 'btn btn-secondary order-1',
          confirmButton: 'btn btn-primary order-2',
        },
        buttonsStyling: false,
        showCancelButton: true,
        confirmButtonText: 'Confirmar'
      }).then(result => {
        const { isConfirmed } = result;

        if (isConfirmed) {
          API.works.completed(id).then(response => {
            if (response.ok === false) {
              throw new Error(response.statusText);
            }

            return response.json();
          }).then(() => {
            dataTableObject.ajax.reload();
            dataTableObject.draw();
            Toast.fire({
              icon: 'success',
              title: 'TCC completado com sucesso.'
            });
          }).catch(err => {
            Toast.fire({
              icon: 'error',
              title: 'Houve um erro no servidor.'
            });
          });
        }
      });
    });
  }

  function handleCompletedButtonFilters() {
    $(completedButtonFilters).find('button').click(function () {
      completed = $(this).data('completed');
      dataTableObject.ajax.reload();
      dataTableObject.draw();
    });
  }

  function initFinalWorkDataTable() {
    $.fn.dataTable.ext.errMode = 'none';

    dataTableObject = $(dataTableElement).DataTable({
      responsive: true,
      drawCallback(settings) {
        handleCompleteButtons();
        handleParticipantsButtons();

        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
          return new bootstrap.Tooltip(tooltipTriggerEl);
        });
      },
      ajax: {
        url: $(dataTableElement).data('api'),
        data(data) {
          data.completed = completed;
        },
      },
      columnDefs: [{
        targets: '_all',
        className: 'align-middle',
        render(data) {
          return data != null ? data : "";
        },
      }],
      columns: [
        {
          data: 'title',
          render(data) {
            return `
              <div>
                <span class="text-gray-700 fw-bold">${data}</span>
              </div>
            `;
          },
        },
        {
          data: 'mentees_detail',
          render(data) {
            return `
              <div class="text-gray-700 text-ellipsis max-w-200px">
                ${data.map(mentee => mentee.full_name).join(', ')}
              </div>
            `;
          },
        },
        {
          data: 'supervisor_detail',
          render(data) {
            return `
              <div>
                <span class="text-gray-700">${data.full_name}</span>
              </div>
            `;
          },
        },
        {
          data: 'completed',
          render(data) {
            if (data === true) {
              return `
                <div>
                  <i class="far fa-check-circle text-success fs-3"></i>
                </div>
              `;
            } else {
              return `
                <div>
                  <i class="far fa-times-circle text-danger fs-3"></i>
                </div>
              `;
            }
          },
        },
        {
          data: null,
          orderable: false,
          className: 'end-column',
          render(data) {
            let actions = `
              <a
                href="/works/${data.id}/stages/"
                class="btn btn-sm btn-icon btn-primary"
                data-bs-toggle="tooltip"
                data-bs-placement="top"
                title="Ver etapas">
                <i class="fas fa-eye"></i>
              </a>
            `;

            if (data.current_stage) {
              actions += `
                <a
                  href="/works/stages/${data.current_stage.id}/detail"
                  class="btn btn-sm btn-icon btn-primary"
                  data-bs-toggle="tooltip"
                  data-bs-placement="top"
                  title="${data.current_stage.stage_detail.description}">
                  <i class="fas fa-calendar-day"></i>
                </a>
              `;
            }

            if ($('#tcc_datatable_users').data('teacher') && data.completed === false) {
              actions += `
                <button
                  class="btn btn-sm btn-icon btn-primary ms-1 tcc_complete_action"
                  data-id="${data.id}"
                  data-bs-toggle="tooltip"
                  data-bs-placement="top"
                  title="Completar TCC">
                  <i class="fas fa-clipboard-check"></i>
                </button>

                <button
                  class="btn btn-sm btn-icon btn-primary ms-1 tcc_participants_action"
                  data-id="${data.id}"
                  data-bs-toggle="tooltip"
                  data-bs-placement="top"
                  title="Atualizar participantes">
                  <i class="fas fa-users"></i>
                </button>
              `;
            }

            return `<div>${actions}</div>`;
          },
        },
      ],
      language: dataTableLanguages,
    });

    $(dataTableElement).on('responsive-display.dt', () => {
      handleCompleteButtons();
      handleParticipantsButtons();

      const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
          return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    });

    $(dataTableElement).on('error.dt', (e, settings, techNote, message) => {
      console.log(message);
    });
  }


  getElements();
  handleCompletedButtonFilters();
  handleUpdateParticipantsForm();
  handleMenteesSelectElement();
  initFinalWorkDataTable();
  initParticipantsModal();
}

KTUtil.onDOMContentLoaded(function() {
  FinalWorkList();
});
