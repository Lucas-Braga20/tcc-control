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
            return data;
          },
        },
        {
          data: 'requester_detail',
          render(data) {
            return data.full_name;
          },
        },
        {
          data: 'final_work',
          render(data) {
            return data;
          },
        },
        {
          data: 'work_stage_detail',
          render(data) {
            return `<span>${data.stage_detail.description}</span>`;
          },
        },
        {
          data: 'created_at_formated',
          render(data) {
            return data;
          },
        },
        {
          data: 'approved',
          render(data) {
            let badge = `
              <span class="badge badge-light">Pendente</span>
            `;

            if (data == true) {
              badge = `
                <span class="badge badge-light-success">Aprovado</span>
              `;
            } else if (data == false) {
              badge = `
                <span class="badge badge-light-danger">Reprovado</span>
              `;
            }

            return badge;
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
                class="btn btn-sm btn-icon btn-primary ms-1 tcc_approve_button"
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
                class="btn btn-sm btn-icon btn-primary ms-1 tcc_approve_button"
                data-approve="${false}"
                data-id="${data.id}"
                data-bs-toggle="tooltip"
                data-bs-placement="top"
                title="Reprovar">
                <i class="far fa-thumbs-down"></i>
              </button>
            `;

            if (data.approved == null) {
              return approvedButton + disapproveButton;
            }

            return '';
          },
        },
      ],
      language: dataTableLanguages,
    });

    $(dataTableElement).on('responsive-display.dt', () => {
      handleApproveButtonActions();
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
