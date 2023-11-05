const FinalWorkProposalList = () => {
  const API = {
    works: {
      reprove(id) {
        return fetch(`/api/final-works/${id}/`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
          body: JSON.stringify({
            approved: false,
          }),
        });
      },
      approve(id) {
        return fetch(`/api/final-works/${id}/`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
          body: JSON.stringify({
            supervisor: $(`#tcc_accordion_body_${id}`).find('select').val(),
            approved: true,
          }),
        });
      },
      cancel(id) {
        return fetch(`/api/final-works/${id}/`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
          body: JSON.stringify({
            archived: true,
          }),
        });
      },
    },
  };


  function handleReproveButtonEvents() {
    $('.tcc_remove_button').click(function (e) {
      const id = $(this).data('id');

      Swal.fire({
        title: 'Reprovar proposta',
        text: 'Tem certeza que deseja reprovar esta proposta?',
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
          API.works.reprove(id).then(response => {
            if (response.ok === false) {
              throw new Error(response.statusText);
            }

            return response.json();
          }).then(() => {
            Toast.fire({
              icon: 'success',
              title: 'Proposta reprovada com sucesso.'
            });

            $(`#tcc_accordion_item_${id}`).find('.tcc-work-proposal-badges').html(`
              <span class="badge badge-light-danger">Reprovado</span>
            `);

            $('.element-only-requested').remove();
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

  function handleApproveButtonEvents() {
    $('.tcc_save_button').click(function (e) {
      const id = $(this).data('id');

      let supervisor = $(`#tcc_accordion_body_${id}`).find('select').select2('data')[0].text

      Swal.fire({
        title: 'Aprovar proposta',
        text: 'Tem certeza que deseja aprovar esta proposta?',
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
          API.works.approve(id).then(response => {
            if (response.ok === false) {
              throw new Error(response.statusText);
            }

            return response.json();
          }).then(() => {
            Toast.fire({
              icon: 'success',
              title: 'Proposta aprovada com sucesso.'
            });

            $(`#tcc_accordion_item_${id}`).find('.tcc-work-proposal-badges').html(`
              <span class="badge badge-light-success">Aprovado</span>
            `);

            $(`#tcc_accordion_item_${id}`).find('.tcc-work-proposal-supervisor').html(supervisor);

            $('.element-only-requested').remove();
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

  function handleCancelButtonEvents() {
    $('.tcc_cancel_button').click(function (e) {
      const id = $(this).data('id');

      Swal.fire({
        title: 'Cancelar proposta',
        text: 'Tem certeza que deseja cancelar esta proposta?',
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
          API.works.cancel(id).then(response => {
            if (response.ok === false) {
              throw new Error(response.statusText);
            }

            return response.json();
          }).then(() => {
            Toast.fire({
              icon: 'success',
              title: 'Proposta cancelada com sucesso.'
            });

            $(`#tcc_accordion_item_${id}`).remove();

            if ($('#tcc_accordion').children().length === 0) {
              $('#tcc_accordion').html(`
                <div class="accordion-item">
                  <h2 class="accordion-header p-7 fs-7 text-muted fw-light">
                    Sem propostas
                  </h2>
                </div>
              `);

              $('#tcc_work_proposal_create_link').removeClass('d-none');
              $('#tcc_work_proposal_create_link_error').addClass('d-none');
            }
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

  handleReproveButtonEvents();
  handleApproveButtonEvents();
  handleCancelButtonEvents();
}

KTUtil.onDOMContentLoaded(function() {
  FinalWorkProposalList();
});
