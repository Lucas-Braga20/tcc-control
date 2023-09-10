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
          method: 'patch',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
          body: JSON.stringify({
            completed: true
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
    dataTableObject = $(dataTableElement).DataTable({
      responsive: true,
      drawCallback(settings) {
        handleCompleteButtons();

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
          data: 'description',
          render(data) {
            return data
          },
        },
        {
          data: 'mentees_detail',
          render(data) {
            return data.map(mentee => mentee.full_name).join(', ');
          },
        },
        {
          data: 'supervisor_detail',
          render(data) {
            return data.full_name;
          },
        },
        {
          data: 'current_stage',
          render(data) {
            if (data) {
              return `
                <a href="/works/stages/${data.id}/detail">
                  ${data.stage_detail.description}
                </a>
              `;
            } else {
              return '--';
            }
          },
        },
        {
          data: null,
          render(data) {
            if (data.current_stage) {
              return badges[data.current_stage.status] || '--';
            } else {
              return '--';
            }
          },
        },
        {
          data: 'completed',
          render(data) {
            if (data === true) {
              return `
                <span class="badge badge-success">
                  Completado
                </span>
              `;
            } else {
              return `
                <span class="badge badge-secondary">
                  Incompleto
                </span>
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
                class="btn btn-sm btn-icon btn-primary ms-1"
                data-bs-toggle="tooltip"
                data-bs-placement="top"
                title="Ver etapas">
                <i class="fas fa-eye"></i>
              </a>
            `;

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
              `;
            }

            return actions;
          },
        },
      ],
      language: dataTableLanguages,
    });

    $(dataTableElement).on('responsive-display.dt', () => {
      handleArchiveButtonActions();
    });
  }


  getElements();
  handleCompletedButtonFilters();
  initFinalWorkDataTable();
}

KTUtil.onDOMContentLoaded(function() {
  FinalWorkList();
});
