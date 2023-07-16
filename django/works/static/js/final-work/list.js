const FinalWorkList = () => {
  let dataTableElement = null;
  let dataTableObject = null;

  let searchInputElement = null;

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


  function getElements() {
    dataTableElement = document.getElementById('tcc_datatable_users');
    searchInputElement = document.getElementById('tcc_datatable_search_input');
  }

  function initFinalWorkDataTable() {
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
            return badges[data] || '';
          },
        },
        {
          data: null,
          orderable: false,
          className: 'text-end',
          render(data) {
            return `
              <a
                href="/works/${data.id}/stages/"
                class="btn btn-sm btn-icon btn-primary ms-1"
                data-bs-toggle="tooltip"
                data-bs-placement="top"
                title="Ver etapas">
                <i class="fas fa-eye"></i>
              </a>
            `;
          },
        },
      ]
    });
  }


  getElements();
  initFinalWorkDataTable();
}

KTUtil.onDOMContentLoaded(function() {
  FinalWorkList();
});
