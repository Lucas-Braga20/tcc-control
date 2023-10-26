const TimetablesList = () => {
  let dataTableElement = null;
  let dataTableObject = null;
  let archivedButtonFilters = null;

  let searchInputElement = null;

  let archived = false;

  const API = {
    timetables: {
      archive(id) {
        return fetch(`/api/timetables/${id}/`, {
          method: 'patch',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
          body: JSON.stringify({
            archived: true
          }),
        });
      },
      unarchive(id) {
        return fetch(`/api/timetables/${id}/`, {
          method: 'patch',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
          body: JSON.stringify({
            archived: false
          }),
        });
      },
    },
  };

  function getElements() {
    dataTableElement = document.getElementById('tcc_datatable_timetables');
    archivedButtonFilters = document.getElementById('tcc_archived_button_filters');
    searchInputElement = document.getElementById('tcc_datatable_search_input');
  }

  function initTimetablesDataTable() {
    $.fn.dataTable.ext.errMode = 'none';

    dataTableObject = $(dataTableElement).DataTable({
      responsive: true,
      drawCallback(settings) {
        handleArchiveButtonActions();

        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
          return new bootstrap.Tooltip(tooltipTriggerEl);
        });
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
          data: 'description',
          render(data) {
            return `
              <div>
                <span class="text-gray-700">${data}</span>
              </div>
            `;
          },
        },
        {
          data: 'start',
          render(data) {
            return `
              <div>
                <span class="text-gray-700">${data}</span>
              </div>
            `;
          },
        },
        {
          data: 'end',
          render(data) {
            return `
              <div>
                <span class="text-gray-700">${data}</span>
              </div>
            `;
          },
        },
        {
          data: null,
          orderable: false,
          className: 'end-column',
          render(data) {
            let updateButtonElement = '';
            let archivedButtonElement = '';

            if (!archived) {
              // Archive
              archivedButtonElement = `
                <button
                  type="button"
                  class="btn btn-sm btn-icon btn-primary ms-1 tcc_archive_button"
                  data-bs-toggle="tooltip"
                  data-bs-placement="top"
                  title="Arquivar"
                  data-archive="${true}"
                  data-id="${data.id}">
                  <i class="fas fa-archive"></i>
                </button>
              `;
              updateButtonElement = `
                <a
                  href="/timetables/update/${data.id}"
                  class="btn btn-sm btn-icon btn-primary"
                  data-bs-toggle="tooltip"
                  data-bs-placement="top"
                  title="Atualizar">
                  <i class="fas fa-edit"></i>
                </a>
              `;
            } else {
              // Unarchive
              archivedButtonElement = `
                <button
                  type="button"
                  class="btn btn-sm btn-icon btn-primary ms-1 tcc_archive_button"
                  data-archive="${false}"
                  data-id="${data.id}"
                  data-bs-toggle="tooltip"
                  data-bs-placement="top"
                  title="Desarquivar">
                  <i class="fas fa-box-open"></i>
                </button>
              `;
            }

            return `
              <div>
                ${updateButtonElement}
                ${archivedButtonElement}
                <a
                  href="/timetables/detail/${data.id}"
                  class="btn btn-sm btn-icon btn-primary ms-1"
                  data-bs-toggle="tooltip"
                  data-bs-placement="top"
                  title="Detalhes">
                  <i class="fas fa-eye"></i>
                </a>
              </div>
            `;
          },
        },
      ],
      language: dataTableLanguages,
    });

    $(dataTableElement).on('responsive-display.dt', () => {
      handleArchiveButtonActions();
    });

    $(dataTableElement).on('error.dt', (e, settings, techNote, message) => {
      console.log(message);
    });
  }

  function handleArchiveButtonActions() {
    $('.tcc_archive_button').click(function () {
      const id = $(this).data('id');
      const archive = $(this).data('archive');

      if (archive) {
        Swal.fire({
          title: 'Arquivar cronograma',
          text: 'Tem certeza que deseja arquivar este cronograma?',
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
            let fetchResponse;

            API.timetables.archive(id)
              .then(response => fetchResponse = response)
              .then(response => {
                return response.json().catch(() => {
                  throw new Error('Houve um erro no servidor.');
                })
              })
              .then(response => {
                if (fetchResponse.status >= 300) {
                  throw new Error(response.detail || 'Houve um erro no servidor.');
                } else {
                  dataTableObject.ajax.reload();
                  dataTableObject.draw();
                  Toast.fire({
                    icon: 'success',
                    title: 'Cronograma arquivado com sucesso.'
                  });
                }
              })
              .catch(err => {
                Toast.fire({
                  icon: 'error',
                  title: err.message,
                });
              });
          }
        });
      } else {
        Swal.fire({
          title: 'Desarquivar cronograma',
          text: 'Tem certeza que deseja desarquivar esta cronograma?',
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
            API.timetables.unarchive(id).then(response => {
              if (response.ok === false) {
                throw new Error(response.statusText);
              }

              return response.json();
            }).then(() => {
              dataTableObject.ajax.reload();
              dataTableObject.draw();
              Toast.fire({
                icon: 'success',
                title: 'Cronograma desarquivado com sucesso.'
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

  function handleSearchInput() {
    $(searchInputElement).keyup(function() {
      dataTableObject.search($(this).val()).draw();
    });
  }

  getElements();
  initTimetablesDataTable();
  handleArchivedButtonFilters();
  handleSearchInput();
}

KTUtil.onDOMContentLoaded(function() {
  TimetablesList();
});
