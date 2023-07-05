const Calendar = () => {
  let calendar = {
    element: null,
    object: null,
  };

  let todayDate = moment().startOf('day');
  let TODAY = todayDate.format("YYYY-MM-DD");

  let API = {
    stages: {
      list(params) {
        return fetch(`/api/stages/${params}`)
      },
    },
  };


  function getElements() {
    calendar.element = document.getElementById('tcc_calendar');
  }

  function initCalendar() {
    calendar.object = new FullCalendar.Calendar(calendar.element, {
      headerToolbar: {
        left: "prev,next today",
        center: "title",
        right: "dayGridMonth,timeGridWeek,timeGridDay,listMonth"
      },

      height: 800,
      contentHeight: 780,
      aspectRatio: 3,

      nowIndicator: true,
      now: TODAY + "T09:25:00",

      views: {
        dayGridMonth: { buttonText: "month" },
        timeGridWeek: { buttonText: "week" },
        timeGridDay: { buttonText: "day" }
      },

      initialView: "dayGridMonth",
      initialDate: TODAY,

      editable: true,
      dayMaxEvents: true, // allow "more" link when too many events
      navLinks: true,

      events(info, cb) {
        let start = moment(info.startStr).format('YYYY-MM-DD');
        let end = moment(info.endStr).format('YYYY-MM-DD');

        API.stages.list(`?start=${start}&end=${end}&pagination=false`)
          .then(response => response.json())
          .then(response => {
            const events = [];

            response.forEach(event => {
              events.push({
                title: event.description,
                start: event.start_date,
                end: event.send_date,
              });
            });

            cb(events);
          })
      },
    });

    calendar.object.render();
  }


  getElements();
  initCalendar();
}

KTUtil.onDOMContentLoaded(function() {
  Calendar();
});
