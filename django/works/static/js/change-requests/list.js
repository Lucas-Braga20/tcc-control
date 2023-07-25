const ChangeRequestList = () => {
  let dataTableElement = null;
  let dataTableObject = null;

  let searchInputElement = null;


  function getElements() {
    dataTableElement = document.getElementById('tcc_datatable_change_requests');
    searchInputElement = document.getElementById('tcc_datatable_search_input');
  }

  function initChangeRequestsDataTable() {
    dataTableObject = $(dataTableElement).DataTable({
      responsive: true,
      drawCallback(settings) {
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
          className: 'text-end',
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
                class="btn btn-sm btn-icon btn-primary ms-1 tcc_disapprove_button"
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
      ]
    });
  }

  function handleSearchInput() {
    $(searchInputElement).keyup(function() {
      dataTableObject.search($(this).val()).draw();
    });
  }


  getElements();

  initChangeRequestsDataTable();
  handleSearchInput();
}

KTUtil.onDOMContentLoaded(function() {
  ChangeRequestList();
});
