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
    searchInputElement = document.getElementById('tcc_datatable_search_input');
  }

  function initTimetablesDataTable() {
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
            return data
          },
        },
        {
          data: 'start',
          render(data) {
            return data
          },
        },
        {
          data: 'end',
          render(data) {
            return data
          },
        },
        {
          data: null,
          orderable: false,
          className: 'text-end',
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
                  href="/activities/update/${data.id}"
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
                title: 'Cronograma arquivado com sucesso.'
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
