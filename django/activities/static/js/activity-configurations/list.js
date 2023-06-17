const ActivityConfigurationList = () => {
  let dataTableElement = null;
  let dataTableObject = null;

  function getElements() {
    dataTableElement = document.getElementById('tcc_datatable_activity_configurations');
  }

  function initActivityConfigurationsDataTable() {
    dataTableObject = $(dataTableElement).DataTable({
      responsive: true,
      ajax: {
        url: $(dataTableElement).data('api'),
      },
      columnDefs: [{
        targets: '_all',
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
            return ''
          },
        },
      ]
    });
  }

  getElements();
  initActivityConfigurationsDataTable();
}

KTUtil.onDOMContentLoaded(function() {
  ActivityConfigurationList();
});
