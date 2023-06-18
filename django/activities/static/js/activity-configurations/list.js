const ActivityConfigurationList = () => {
  let dataTableElement = null;
  let dataTableObject = null;
  let archivedButtonFilters = null;

  let archived = false;

  const API = {
    activities: {
      archive(id) {
        return fetch(`/api/activities/${id}/`, {
          method: 'patch',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            archived: true
          }),
        });
      },
      unarchive(id) {
        return fetch(`/api/activities/${id}/`, {
          method: 'patch',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            archived: false
          }),
        });
      },
    },
  };

  const Toast = Swal.mixin({
    toast: true,
    position: 'bottom-end',
    showConfirmButton: false,
    timer: 3000,
  });

  function getElements() {
    dataTableElement = document.getElementById('tcc_datatable_activity_configurations');
    archivedButtonFilters = document.getElementById('tcc_archived_button_filters');
  }

  function initActivityConfigurationsDataTable() {
    dataTableObject = $(dataTableElement).DataTable({
      responsive: true,
      drawCallback(settings) {
        handleArchiveButtonActions();
      },
      ajax: {
        url: $(dataTableElement).data('api'),
        data(data) {
          data.archived = archived;
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
          data: 'name',
          render(data) {
            return data
          },
        },
        {
          data: 'fields_description',
          render(data) {
            return data
          },
        },
        {
          data: 'template_abnt',
          render(data) {
            let element = ''
            if (data === null || data === '') {
              element = `
                <span class="text-muted">
                  Sem template
                </span>
              `
            }
            return element
          },
        },
        {
          data: null,
          orderable: false,
          render(data) {
            const updateButtonElement = `
              <a href="/activities/update/${data.id}" class="btn btn-sm btn-icon btn-primary">
                <i class="fas fa-edit"></i>
              </a>
            `;

            let archivedButtonElement = '';

            if (!archived) {
              // Archive
              archivedButtonElement = `
                <button
                  type="button"
                  class="btn btn-sm btn-icon btn-primary ms-1 tcc_archive_button"
                  data-archive="${true}"
                  data-id="${data.id}">
                  <i class="fas fa-archive"></i>
                </button>
              `;
            } else {
              // Unarchive
              archivedButtonElement = `
                <button
                  type="button"
                  class="btn btn-sm btn-icon btn-primary ms-1 tcc_archive_button"
                  data-archive="${false}"
                  data-id="${data.id}">
                  <i class="fas fa-box-open"></i>
                </button>
              `;
            }

            return `${updateButtonElement}${archivedButtonElement}`;
          },
        },
      ]
    });
  }

  function handleArchiveButtonActions() {
    $('.tcc_archive_button').click(function () {
      const id = $(this).data('id');
      const archive = $(this).data('archive');

      if (archive) {
        Swal.fire({
          title: 'Arquivar atividade',
          text: 'Tem certeza que deseja arquivar esta atividade?',
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
            API.activities.archive(id).then(response => {
              if (response.ok === false) {
                throw new Error(response.statusText);
              }

              return response.json();
            }).then(() => {
              dataTableObject.ajax.reload();
              dataTableObject.draw();
              Toast.fire({
                icon: 'success',
                title: 'Atividade arquivada com sucesso.'
              });
            }).catch(err => {
              Toast.fire({
                icon: 'error',
                title: 'Houve um erro no servidor.'
              });
            });
          }
        });
      } else {
        Swal.fire({
          title: 'Desarquivar atividade',
          text: 'Tem certeza que deseja desarquivar esta atividade?',
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
            API.activities.unarchive(id).then(response => {
              if (response.ok === false) {
                throw new Error(response.statusText);
              }

              return response.json();
            }).then(() => {
              dataTableObject.ajax.reload();
              dataTableObject.draw();
              Toast.fire({
                icon: 'success',
                title: 'Atividade desarquivada com sucesso.'
              });
            }).catch(err => {
              Toast.fire({
                icon: 'error',
                title: 'Houve um erro no servidor.'
              });
            });
          }
        });
      }
    });
  }

  function handleArchivedButtonFilters() {
    $(archivedButtonFilters).find('button').click(function () {
      archived = $(this).data('archived');
      dataTableObject.ajax.reload();
      dataTableObject.draw();
    });
  }

  getElements();
  initActivityConfigurationsDataTable();
  handleArchivedButtonFilters();
}

KTUtil.onDOMContentLoaded(function() {
  ActivityConfigurationList();
});
