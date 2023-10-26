const ChangeRequestList = () => {
  let dataTableElement = null;
  let dataTableObject = null;

  let searchInputElement = null;

  const API = {
    changeRequests: {
      approve(id) {
        return fetch(`/api/change-requests/${id}/`, {
          method: 'patch',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
          body: JSON.stringify({
            approved: true
          }),
        });
      },
      disapprove(id) {
        return fetch(`/api/change-requests/${id}/`, {
          method: 'patch',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
          body: JSON.stringify({
            approved: false
          }),
        });
      },
    },
  };


  function getElements() {
    dataTableElement = document.getElementById('tcc_datatable_change_requests');
    searchInputElement = document.getElementById('tcc_datatable_search_input');
  }

  function initChangeRequestsDataTable() {
    $.fn.dataTable.ext.errMode = 'none';

    dataTableObject = $(dataTableElement).DataTable({
      responsive: true,
      drawCallback(settings) {
        handleApproveButtonActions();

        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
          return new bootstrap.Tooltip(tooltipTriggerEl);
        });
      },
      ajax: {
        url: $(dataTableElement).data('api'),
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
                <span class="text-gray-700">
                  ${data}
                </span>
              </div>
            `;
          },
        },
        {
          data: 'requester_detail',
          render(data) {
            return `
              <div>
                <span class="text-gray-700">
                  ${data.full_name}
                </span>
              </div>
            `;
          },
        },
        {
          data: null,
          render(data) {
            return `
              <div>
                <span class="text-gray-700">
                  <span class="text-primary fw-bold">
                    ${data.final_work}:
                  </span>
                  ${data.work_stage_detail.stage_detail.description}
                </span>
              </div>
            `;
          },
        },
        {
          data: 'created_at_formated',
          render(data) {
            return `
              <div>
                <span class="text-gray-700">
                  ${data}
                </span>
              </div>
            `;
          },
        },
        {
          data: 'approved',
          render(data) {
            if (data === true) {
              return `
                <div>
                  <i
                    class="far fa-check-circle text-success fs-3"
                    data-bs-toggle="tooltip"
                    data-bs-placement="top"
                    title="Aprovado"></i>
                </div>
              `;
            } else if (data === false) {
              return `
                <div>
                  <i
                    class="far fa-times-circle text-danger fs-3"
                    data-bs-toggle="tooltip"
                    data-bs-placement="top"
                    title="Reprovado"></i>
                </div>
              `;
            } else {
              return `
                <div>
                  <i
                    class="fas fa-exclamation-circle fs-3"
                    data-bs-toggle="tooltip"
                    data-bs-placement="top"
                    title="Pendente"></i>
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
            let approvedButton = `
              <button
                type="button"
                class="btn btn-sm btn-icon btn-primary me-1 tcc_approve_button"
                data-approve="${true}"
                data-id="${data.id}"
                data-bs-toggle="tooltip"
                data-bs-placement="top"
                title="Aprovar">
                <i class="far fa-thumbs-up"></i>
              </button>
            `;

            let disapproveButton = `
              <button
                type="button"
                class="btn btn-sm btn-icon btn-primary tcc_approve_button"
                data-approve="${false}"
                data-id="${data.id}"
                data-bs-toggle="tooltip"
                data-bs-placement="top"
                title="Reprovar">
                <i class="far fa-thumbs-down"></i>
              </button>
            `;

            if (data.approved == null) {
              return `
                <div>
                  ${approvedButton + disapproveButton}
                </div>
              `;
            }

            return '';
          },
        },
      ],
      language: dataTableLanguages,
    });

    $(dataTableElement).on('responsive-display.dt', () => {
      handleApproveButtonActions();

      const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
      tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
      });
    });

    $(dataTableElement).on('error.dt', (e, settings, techNote, message) => {
      console.log(message);
    });
  }

  function handleSearchInput() {
    $(searchInputElement).keyup(function() {
      dataTableObject.search($(this).val()).draw();
    });
  }

  function handleApproveButtonActions() {
    $('.tcc_approve_button').click(function () {
      const id = $(this).data('id');
      const approve = $(this).data('approve');

      if (approve) {
        Swal.fire({
          title: 'Aprovar pedido?',
          text: 'Tem certeza que deseja aprovar este pedido?',
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
            API.changeRequests.approve(id).
              then(response => {
                if (response.ok === false) {
                  throw new Error(response.statusText);
                }

                return response.json();
              }).then(() => {
                dataTableObject.ajax.reload();
                dataTableObject.draw();
                Toast.fire({
                  icon: 'success',
                  title: 'Pedido aprovado com sucesso.'
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
          title: 'Reprovar pedido',
          text: 'Tem certeza que deseja reprovar este pedido?',
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
            API.changeRequests.disapprove(id)
              .then(response => {
                if (response.ok === false) {
                  throw new Error(response.statusText);
                }

                return response.json();
              }).then(() => {
                dataTableObject.ajax.reload();
                dataTableObject.draw();
                Toast.fire({
                  icon: 'success',
                  title: 'Pedido reprovado com sucesso.'
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


  getElements();

  initChangeRequestsDataTable();
  handleSearchInput();
}

KTUtil.onDOMContentLoaded(function() {
  ChangeRequestList();
});
