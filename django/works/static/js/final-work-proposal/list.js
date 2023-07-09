const FinalWorkProposalList = () => {
  const API = {
    works: {
      reprove(id) {
        return fetch(`/api/final-works/${id}/`, {
          method: 'patch',
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
          method: 'patch',
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

            $(`#tcc_accordion_body_${id}`).remove();
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
}

KTUtil.onDOMContentLoaded(function() {
  FinalWorkProposalList();
});
