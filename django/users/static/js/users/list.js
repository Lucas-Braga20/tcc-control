const TimetablesList = () => {
  let dataTableElement = null;
  let dataTableObject = null;
  let isActiveButtonFilters = null;

  let searchInputElement = null;

  let isActive = true;

  let groupsBadges = {
    'Professor da disciplina': `
      <span class="badge badge-light-primary">Professor da disciplina</span>
    `,
    'Orientador': `
      <span class="badge badge-light-success">Orientador</span>
    `,
    'Orientando': `
      <span class="badge badge-light-info">Orientando</span>
    `,
    'Admin': `
      <span class="badge badge-light-dark">Admin</span>
    `,
  };

  const API = {
    users: {
      active(id) {
        return fetch(`/api/users/${id}/`, {
          method: 'patch',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
          body: JSON.stringify({
            is_active: true
          }),
        });
      },
      unactive(id) {
        return fetch(`/api/users/${id}/`, {
          method: 'patch',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
          body: JSON.stringify({
            is_active: false
          }),
        });
      },
      changeRole(id, group) {
        return fetch(`/api/users/${id}/`, {
          method: 'patch',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
          body: JSON.stringify({
            groups: [group]
          }),
        });
      },
    },
  };


  function getElements() {
    dataTableElement = document.getElementById('tcc_datatable_users');
    isActiveButtonFilters = document.getElementById('tcc_active_button_filters');
    searchInputElement = document.getElementById('tcc_datatable_search_input');
  }

  function initUsersDataTable() {
    $.fn.dataTable.ext.errMode = 'none';

    dataTableObject = $(dataTableElement).DataTable({
      responsive: true,
      drawCallback(settings) {
        handleArchiveButtonActions();
        handleRoleButtonActions();

        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
          return new bootstrap.Tooltip(tooltipTriggerEl);
        });
      },
      ajax: {
        url: $(dataTableElement).data('api'),
        data(data) {
          data.is_active = isActive;
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
          data: 'full_name',
          render(data) {
            return `
              <div>
                <span class="text-gray-700">${data}</span>
              </div>
            `;
          },
        },
        {
          data: 'username',
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
          render(data) {
            if (data.groups_detail && data.groups_detail.length == 0) {
              if (data.is_superuser) {
                return `
                  <div>
                    ${groupsBadges['Admin']}
                  </div>
                `;
              }

              return `
                <div>
                  <span class="text-muted fs-6">Sem perfil</span>
                </div>
              `;
            }

            return `
              <div>
                ${groupsBadges[data.groups_detail[0].name]}
              </div>
            `;
          },
        },
        {
          data: null,
          orderable: false,
          className: 'end-column',
          render(data) {
            let activeButtonElement = '';
            let changeRoleElement = '';

            if (!isActive) {
              // Active
              activeButtonElement = `
                <button
                  type="button"
                  class="btn btn-sm btn-icon btn-primary me-1 tcc_active_button"
                  data-bs-toggle="tooltip"
                  data-bs-placement="top"
                  title="Ativar"
                  data-active="${true}"
                  data-id="${data.id}">
                  <i class="fas fa-box-open"></i>
                </button>
              `;
            } else {
              // Unactive
              activeButtonElement = `
                <button
                  type="button"
                  class="btn btn-sm btn-icon btn-primary me-1 tcc_active_button"
                  data-active="${false}"
                  data-id="${data.id}"
                  data-bs-toggle="tooltip"
                  data-bs-placement="top"
                  title="Desativar">
                  <i class="fas fa-archive"></i>
                </button>
              `;
            }

            if (isActive && data.groups_detail[0] && data.groups_detail[0].name == 'Orientando') {
              changeRoleElement = `
                <button
                  type="button"
                  class="btn btn-sm btn-icon btn-primary me-1 tcc_change_role_button"
                  data-bs-toggle="tooltip"
                  data-bs-placement="top"
                  title="Trocar para orientador"
                  data-group="1"
                  data-id="${data.id}">
                  <i class="fas fa-user-tie"></i>
                </button>
              `;
            }

            if (isActive && data.groups_detail[0] && data.groups_detail[0].name == 'Orientador') {
              changeRoleElement = `
                <button
                  type="button"
                  class="btn btn-sm btn-icon btn-primary me-1 tcc_change_role_button"
                  data-bs-toggle="tooltip"
                  data-bs-placement="top"
                  title="Trocar para orientando"
                  data-group="2"
                  data-id="${data.id}">
                  <i class="fas fa-user-graduate"></i>
                </button>
              `;
            }

            if (!data.is_superuser)
              return `<div>${activeButtonElement} ${changeRoleElement}</div>`;

            return '';
          },
        },
      ],
      language: dataTableLanguages,
    });

    $(dataTableElement).on('responsive-display.dt', () => {
      handleArchiveButtonActions();
      handleRoleButtonActions();
    });

    $(dataTableElement).on('error.dt', (e, settings, techNote, message) => {
      console.log(message);
    });
  }

  function handleRoleButtonActions() {
    $('.tcc_change_role_button').click(function () {
      const id = $(this).data('id');
      const group = Number.parseInt($(this).data('group'));

      if (group == 1) {
        Swal.fire({
          title: 'Trocar perfil do usuário',
          text: 'Tem certeza que deseja que deseja alterar o perfil deste usuário para orientador?',
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

            API.users.changeRole(id, '1')
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
                    title: 'Usuário alterado com sucesso.'
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
      }

      if (group == 2) {
        Swal.fire({
          title: 'Trocar perfil do usuário',
          text: 'Tem certeza que deseja que deseja alterar o perfil deste usuário para orientando?',
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

            API.users.changeRole(id, '2')
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
                    title: 'Usuário alterado com sucesso.'
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
      }
    });
  }

  function handleArchiveButtonActions() {
    $('.tcc_active_button').click(function () {
      const id = $(this).data('id');
      const active = $(this).data('active');

      if (active) {
        Swal.fire({
          title: 'Ativar usuário',
          text: 'Tem certeza que deseja ativar este usuário?',
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

            API.users.active(id)
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
                    title: 'Usuário ativado com sucesso.'
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
          title: 'Desativar usuário',
          text: 'Tem certeza que deseja desativar este usuário?',
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
            API.users.unactive(id).then(response => {
              if (response.ok === false) {
                throw new Error(response.statusText);
              }

              return response.json();
            }).then(() => {
              dataTableObject.ajax.reload();
              dataTableObject.draw();
              Toast.fire({
                icon: 'success',
                title: 'Usuário desativado com sucesso.'
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

  function handleActiveButtonFilters() {
    $(isActiveButtonFilters).find('button').click(function () {
      isActive = $(this).data('active');
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
  initUsersDataTable();
  handleActiveButtonFilters();
  handleSearchInput();
}

KTUtil.onDOMContentLoaded(function() {
  TimetablesList();
});
