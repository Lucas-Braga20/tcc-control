const Notification = () => {
  const API = {
    notification: {
      list(param) {
        return fetch(`/api/notifications/?no_page=true${param}`, {
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
        });
      },
      markAllRead() {
        return fetch(`/api/notifications/mark_all_read/`, {
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
          },
        });
      },
    },
  };


  function addElementsInList(notifications, container) {
    if (notifications.length == 0) {
      $(container).html(`
        <div class="scroll-y mh-325px my-2 mb-5 px-8">
          <div class="border border-gray-300 rounded mt-3">
            <div class="d-flex flex-column p-3">
              <h3 class="fs-7 fw-light text-gray-700 mb-0 text-center">
                Sem notificações
              </h3>
            </div>
          </div>
        </div>
      `);
    } else {
      let elements = '';

      notifications.forEach(notification => {
        elements += `
          <div class="border border-gray-300 rounded mt-3">
            <div class="d-flex flex-column p-3">
              <h3 class="fs-7 fw-semibold text-gray-800 mb-0">
                ${notification.description}
              </h3>
              <p class="fs-7 fw-light text-gray-700 mb-0 text-end">
                ${notification.created_at}
              </p>
            </div>
          </div>
        `;
      });

      if (container === '#kt_topbar_notifications_not_viewed') {
        $(container).html(`
          <div class="scroll-y mh-325px my-2 mb-5 px-8">
            ${elements}
          </div>

          <div class="py-3 text-center border-top">
            <button id="tcc_notification_viewall" class="btn btn-color-gray-600 btn-active-color-primary">
              Marcar como lido
            </button>
          </div>
        `);
      } else {
        $(container).html(`
          <div class="scroll-y mh-325px my-2 mb-5 px-8">
            ${elements}
          </div>
        `);
      }
    }
  }

  function getNotifications() {
    $('#tcc_notification_viewall').html(`
      <div class="spinner-border spinner-border-sm text-primary me-2" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      Marcar como lido
    `);

    $('#tcc_notification_viewall').attr('disabled', true);

    API.notification.list('&visualized=false')
      .then(response => {
        if (response.ok === false) {
          throw new Error(response.statusText);
        }

        return response.json();
      })
      .then(response => {
        addElementsInList(response, '#kt_topbar_notifications_not_viewed')
      })
      .catch(() => {
        Toast.fire({
          icon: 'error',
          title: 'Houve um erro ao buscar as notificações recentes.'
        });
      })
      .finally(() => {
        handleViewAllButtonEvent();
      });

    API.notification.list('&visualized=true')
      .then(response => {
        if (response.ok === false) {
          throw new Error(response.statusText);
        }

        return response.json();
      })
      .then(response => {
        addElementsInList(response, '#kt_topbar_notifications_viewed')
      })
      .catch(() => {
        Toast.fire({
          icon: 'error',
          title: 'Houve um erro ao buscar as notificações visualizadas.'
        });
      });
  }

  function handleViewAllButtonEvent() {
    $('#tcc_notification_viewall').click(function(e) {
      API.notification.markAllRead()
        .then(response => {
          if (response.ok === false) {
            throw new Error(response.statusText);
          }

          return response.json();
        })
        .then(() => {
          getNotifications();
        })
        .catch(() => {
          Toast.fire({
            icon: 'error',
            title: 'Houve um erro ao marcas as notificações como lidas.'
          });
        });
    });
  }

  function handleIntervalNotifications() {
    setInterval(() => {
      getNotifications();
    }, 10000);
  }


  handleViewAllButtonEvent();
  handleIntervalNotifications();
}

KTUtil.onDOMContentLoaded(function() {
  Notification();
});
