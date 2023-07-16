const FinalWorkStageDetail = () => {
  let commentsContainer = null;
  let addCommentButton = null;
  let commentDescriptionTextarea = null;

  const API = {
    works: {
      comments() {
        return fetch(`/api/comments/?no_page=true&work_stage=${$(commentsContainer).data('work-stage')}`, {
          method: 'get',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
        });
      },
      add(workStage, description) {
        return fetch(`/api/comments/`, {
          method: 'post',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
          body: JSON.stringify({
            work_stage: $(addCommentButton).data('work-stage'),
            description: description,
          }),
        });
      },
    },
  };


  function getElements() {
    commentsContainer = $('#tcc_comments_container');
    addCommentButton = $('#tcc_add_comment');
    commentDescriptionTextarea = $('#tcc_comment_textarea');
  }

  function getAllComments() {
    API.works.comments()
      .then(response => response.json())
      .then(response => {
        let comments = '';

        if (response.length == 0) {
          $(commentsContainer).html(`
            <div class="p-4 border rounded">
              <div class="mt-2">
                <p class="mb-0">
                  Sem comentários
                </p>
              </div>
            </div>
          `);

          return;
        }

        response.forEach(comment => {
          comments += `
            <div class="p-4 border rounded mt-2">
              <div class="d-flex justify-content-between text-gray-500">
                <h5 class="mb-0">
                  ${comment.author_detail.full_name}
                </h5>
                <span>
                  ${moment(comment.created_at).format('DD/MM/YYYY HH:mm')}
                </span>
              </div>
              <div class="mt-2">
                <p class="mb-0">
                  ${comment.description}
                </p>
              </div>
            </div>
          `;
        });
        $(commentsContainer).html(comments);
      });
  }

  function initAddCommentEvent() {
    $(addCommentButton).click(e => {
      $(commentDescriptionTextarea).attr('disabled', true);
      $(addCommentButton).attr('disabled', true);

      $(addCommentButton).html(`
        <div class="spinner-border spinner-border-sm text-white me-2" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        Comentar
      `);

      API.works.add($(addCommentButton).data('work-stage'), $(commentDescriptionTextarea).val())
        .then(response => {
          if (response.ok === false) {
            throw new Error(response.statusText);
          }

          return response.json();
        })
        .then(response => {
          getAllComments();

          $(commentDescriptionTextarea).val('');

          Toast.fire({
            icon: 'success',
            title: 'Comentário criado com sucesso.'
          });
        })
        .catch(err => {
          Toast.fire({
            icon: 'error',
            title: 'Houve um erro ao criar o comentário. Tente novamente!'
          });
        })
        .finally(() => {
          $(commentDescriptionTextarea).removeAttr('disabled');
          $(addCommentButton).removeAttr('disabled');

          $(addCommentButton).html(`Comentar`);
        });
    });
  }


  getElements();
  initAddCommentEvent();
}

KTUtil.onDOMContentLoaded(function() {
  FinalWorkStageDetail();
});
